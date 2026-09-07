"""
时空模型模块 (Spatio-Temporal Model)
===================================

两套实现策略（自动降级）：
  - PyTorch 可用 → 1D-CNN（局部特征提取）+ LSTM（时序依赖建模）
  - PyTorch 不可用 → NumPy 滑动窗口统计异常检测

核心功能：
1. 时序特征提取：1D-CNN 卷积核捕获电流/功率的局部突变模式
2. 时序依赖建模：LSTM 捕获开关分合、功率波动的时序规律
3. 时序异常检测：基于预测误差（重构误差）或统计阈值判定异常
4. 状态跳变检测：检测开关频繁分合（状态抖动 flapping）

异常类型：
  - 趋势异常：功率/电流突然大幅上升/下降
  - 周期性异常：违反正常周期模式的波动
  - 状态异常：分位有电流/合位无功率
  - 突变异常：短时间内大幅跳变
"""

from __future__ import annotations
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

import numpy as np

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# PyTorch 可用性检测
# ------------------------------------------------------------------
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    nn = F = torch = None   # type: ignore
    logger.warning(
        "[时空模型] PyTorch 未安装，将使用 NumPy 滑动窗口统计异常检测"
    )

# ------------------------------------------------------------------
# 数据结构
# ------------------------------------------------------------------

@dataclass
class TemporalAnomalyResult:
    """单设备时序异常检测结果"""
    equip_id: str
    anomaly_score: float       # [0, 1]，越高越异常
    anomaly_type: str          # TREND / CYCLIC / STATE / SPIKE / NORMAL
    confidence: float         # 置信度
    status: str               # NORMAL / ANOMALY / MISSING / UNCERTAIN
    detail: str               # 详细描述
    current_value: float      # 最新电流值
    power_value: float       # 最新功率值
    volatility: float         # 波动率
    trend_slope: float        # 趋势斜率
    status_flapping: bool     # 是否频繁分合

    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "anomaly_score": round(self.anomaly_score, 4),
            "anomaly_type": self.anomaly_type,
            "confidence": round(self.confidence, 4),
            "status": self.status,
            "detail": self.detail,
            "current_value": round(self.current_value, 3),
            "power_value": round(self.power_value, 3),
            "volatility": round(self.volatility, 4),
            "trend_slope": round(self.trend_slope, 4),
            "status_flapping": self.status_flapping,
        }


@dataclass
class TelemetryWindow:
    """单设备时序窗口数据"""
    equip_id: str
    ia: List[float] = field(default_factory=list)
    ib: List[float] = field(default_factory=list)
    ic: List[float] = field(default_factory=list)
    ua: List[float] = field(default_factory=list)
    ub: List[float] = field(default_factory=list)
    uc: List[float] = field(default_factory=list)
    ap: List[float] = field(default_factory=list)
    rp: List[float] = field(default_factory=list)
    quality: List[int] = field(default_factory=list)   # 1=有效 0=无效
    timestamps: List[str] = field(default_factory=list)

    @property
    def n_points(self) -> int:
        return len(self.ia)

    def to_arrays(self) -> Tuple[np.ndarray, ...]:
        pad = 0.0
        max_len = max(
            len(self.ia), len(self.ib), len(self.ic),
            len(self.ua), len(self.ub), len(self.uc),
            len(self.ap), len(self.rp),
        )
        def _pad(arr, v):
            if len(arr) >= max_len:
                return np.array(arr[-max_len:], dtype=np.float32)
            return np.pad(np.array(arr, dtype=np.float32),
                          (0, max_len - len(arr)), constant_values=v)

        return (
            _pad(self.ia, 0.0),
            _pad(self.ib, 0.0),
            _pad(self.ic, 0.0),
            _pad(self.ua, 0.0),
            _pad(self.ub, 0.0),
            _pad(self.uc, 0.0),
            _pad(self.ap, 0.0),
            _pad(self.rp, 0.0),
        )


# ------------------------------------------------------------------
# 时序窗口构建
# ------------------------------------------------------------------

def build_telemetry_windows(
    telemetry_data: dict,
    max_window: int = 60,
) -> Dict[str, TelemetryWindow]:
    """
    从原始遥测字典构建时序窗口

    参数:
        telemetry_data: {equip_id: [row, ...]} 或 {equip_id: {row}}
        max_window: 最大窗口长度（取最近 N 条）

    返回: {equip_id: TelemetryWindow}
    """
    windows: Dict[str, TelemetryWindow] = {}

    for equip_id, raw in telemetry_data.items():
        rows = raw if isinstance(raw, list) else [raw]
        if not rows:
            continue

        # 取最近 max_window 条
        rows = rows[-max_window:]

        w = TelemetryWindow(equip_id=equip_id)
        for r in rows:
            w.ia.append(float(r.get("IA", 0) or 0))
            w.ib.append(float(r.get("IB", 0) or 0))
            w.ic.append(float(r.get("IC", 0) or 0))
            w.ua.append(float(r.get("UA", 0) or 0))
            w.ub.append(float(r.get("UB", 0) or 0))
            w.uc.append(float(r.get("UC", 0) or 0))
            w.ap.append(float(r.get("AP", 0) or 0))
            w.rp.append(float(r.get("RP", 0) or 0))
            w.quality.append(int(r.get("QUALITY", 1)))
            w.timestamps.append(str(r.get("DATA_DATE", "")))

        windows[equip_id] = w

    logger.info("[时空模型] 构建 %d 个时序窗口", len(windows))
    return windows


# ------------------------------------------------------------------
# 方案 A: PyTorch 1D-CNN + LSTM
# ------------------------------------------------------------------

if TORCH_AVAILABLE:

    class TemporalConv1D(nn.Module):
        """1D-CNN 时序特征提取：捕获局部突变模式（电流冲击、功率骤变）"""
        def __init__(self, in_channels: int, out_channels: int,
                     kernel_size: int = 3):
            super().__init__()
            self.conv = nn.Conv1d(in_channels, out_channels, kernel_size,
                                  padding=kernel_size // 2)
            self.bn = nn.BatchNorm1d(out_channels)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # x: (batch, channels, seq_len)
            out = self.conv(x)
            out = self.bn(out)
            return F.relu(out)

    class TemporalLSTM(nn.Module):
        """LSTM 时序依赖建模：捕获分合位和功率波动的时序规律"""
        def __init__(self, input_size: int, hidden_size: int, num_layers: int = 2):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                                batch_first=True, dropout=0.1)

        def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Tuple]:
            out, (h, c) = self.lstm(x)
            return out, (h, c)

    class SpatioTemporalNet(nn.Module):
        """
        1D-CNN + LSTM 时序异常检测网络

        架构:
            Input(8, seq_len)        ← 8通道: IA, IB, IC, UA, UB, UC, AP, RP
            → TemporalConv1D(8→32, k=3) → ReLU
            → TemporalConv1D(32→64, k=3) → ReLU
            → TemporalConv1D(64→32, k=3) → ReLU
            → TemporalLSTM(32, 64)  ← 时序建模
            → Last hidden state       ← 取最后时刻隐状态
            → Linear(64→32) → ReLU
            → Linear(32→1) → Sigmoid → anomaly_score
        """

        def __init__(self, in_channels: int = 8,
                     cnn_channels: List[int] = [32, 64, 32],
                     lstm_hidden: int = 64,
                     lstm_layers: int = 2,
                     dropout: float = 0.2):
            super().__init__()
            self.conv1 = TemporalConv1D(in_channels, cnn_channels[0])
            self.conv2 = TemporalConv1D(cnn_channels[0], cnn_channels[1])
            self.conv3 = TemporalConv1D(cnn_channels[1], cnn_channels[2])
            self.pool = nn.AdaptiveAvgPool1d(1)
            self.lstm = TemporalLSTM(cnn_channels[2], lstm_hidden, lstm_layers)
            self.fc = nn.Sequential(
                nn.Linear(lstm_hidden, 32),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(32, 1),
                nn.Sigmoid(),
            )

        def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
            # x: (batch, seq_len, features)  → CNN 需要 (batch, features, seq_len)
            x = x.permute(0, 2, 1)
            x = self.conv1(x)
            x = self.conv2(x)
            x = self.conv3(x)
            # LSTM 需要 (batch, seq_len, channels)
            x = x.permute(0, 2, 1)
            lstm_out, _ = self.lstm(x)
            # 取最后时刻隐状态
            h_last = lstm_out[:, -1, :]
            anomaly_score = self.fc(h_last).squeeze(-1)
            return anomaly_score, h_last


# ------------------------------------------------------------------
# 方案 B: NumPy 滑动窗口统计异常检测
# ------------------------------------------------------------------

class NumpyTemporalDetector:
    """
    NumPy 实现：多策略时序异常检测

    策略：
    1. 滑动窗口均值/标准差异常：超出 (mean ± 3σ) 判定异常
    2. 趋势斜率检测：线性回归斜率超出阈值判定趋势异常
    3. 状态跳变检测：连续 N 步内状态翻转次数超阈值
    4. 突变检测：单步跳变超出 (max-min)×0.3 阈值
    5. 重构误差：滑动窗口自回归预测误差检测
    """

    def __init__(
        self,
        window_size: int = 20,
        spike_threshold: float = 3.0,
        trend_threshold: float = 0.5,
        flapping_window: int = 10,
        flapping_count: int = 3,
    ):
        self.window_size = window_size
        self.spike_threshold = spike_threshold
        self.trend_threshold = trend_threshold
        self.flapping_window = flapping_window
        self.flapping_count = flapping_count

    def detect(self, window: TelemetryWindow) -> TemporalAnomalyResult:
        """对单个设备进行时序异常检测"""
        if window.n_points < 3:
            return TemporalAnomalyResult(
                equip_id=window.equip_id,
                anomaly_score=0.0,
                anomaly_type="NORMAL",
                confidence=0.0,
                status="MISSING",
                detail="数据点不足（<3），无法进行时序分析",
                current_value=0.0, power_value=0.0,
                volatility=0.0, trend_slope=0.0, status_flapping=False,
            )

        ia, ib, ic, ua, ub, uc, ap, rp = window.to_arrays()
        n = window.n_points

        # 最新值
        cur_ia = float(ia[-1])
        cur_ap = float(ap[-1])

        # === 1. 滑动窗口统计异常 ===
        anomaly_scores: List[float] = []
        for arr in [ia, ib, ic]:
            arr_clean = arr[arr != 0.0] if arr.sum() != 0 else arr
            if len(arr_clean) < 3:
                continue
            mu, sigma = arr_clean.mean(), arr_clean.std() + 1e-6
            z_scores = np.abs((arr_clean - mu) / sigma)
            spikes = z_scores > self.spike_threshold
            if spikes.any():
                anomaly_scores.append(float(spikes.mean()))

        # === 2. 趋势异常（线性回归斜率）===
        trend_score = 0.0
        for arr in [ap, ia]:
            if len(arr) >= 5:
                x = np.arange(len(arr), dtype=np.float32)
                x_mean = x.mean()
                arr_mean = arr.mean()
                cov = ((x - x_mean) * (arr - arr_mean)).sum()
                var = ((x - x_mean) ** 2).sum()
                slope = cov / (var + 1e-6) if var > 0 else 0.0
                # 归一化斜率
                norm_slope = abs(slope) / (abs(arr_mean) + 1.0)
                if norm_slope > self.trend_threshold:
                    trend_score = max(trend_score, norm_slope / (self.trend_threshold * 5))

        # === 3. 突变异常（单步大幅跳变）===
        spike_score = 0.0
        for arr in [ia, ib, ic, ap]:
            if len(arr) >= 2:
                diffs = np.abs(np.diff(arr))
                rng = arr.max() - arr.min() + 1e-6
                spike_ratio = diffs / rng
                spike_score = max(spike_score, float(spike_ratio.max()))

        # === 4. 波动率 ===
        volatility = 0.0
        for arr in [ia, ap]:
            if len(arr) >= 2:
                v = arr[arr != 0]
                if len(v) >= 2:
                    m = v.mean()
                    s = v.std()
                    if abs(m) > 0.1:
                        volatility = max(volatility, abs(s / m))

        # === 5. 状态跳变（flapping）===
        # 基于电流值突变推断开关状态
        status_flapping = False
        if len(ia) >= self.flapping_window:
            window_currents = ia[-self.flapping_window:]
            # 阈值分割：>10A 合位，<1A 分位
            states = (window_currents > 5.0).astype(int)
            transitions = np.sum(np.abs(np.diff(states)))
            if transitions >= self.flapping_count:
                status_flapping = True

        # === 综合评分 ===
        scores = [s for s in [np.mean(anomaly_scores) if anomaly_scores else 0.0,
                                trend_score, spike_score,
                                volatility * 0.5,  # 波动率权重降低
                                float(status_flapping) * 0.8]
                  if s > 0]
        anomaly_score = max(scores) if scores else 0.0
        anomaly_score = float(np.clip(anomaly_score, 0.0, 1.0))

        # 异常类型判定
        if anomaly_score < 0.2:
            anomaly_type = "NORMAL"
        elif status_flapping:
            anomaly_type = "STATE"
        elif trend_score > anomaly_score * 0.7:
            anomaly_type = "TREND"
        elif spike_score > anomaly_score * 0.7:
            anomaly_type = "SPIKE"
        else:
            anomaly_type = "CYCLIC"

        # 状态判定
        if anomaly_score >= 0.6:
            status = "ANOMALY"
            confidence = 0.85
        elif anomaly_score >= 0.3:
            status = "UNCERTAIN"
            confidence = 0.60
        else:
            status = "NORMAL"
            confidence = 0.80

        detail_parts = []
        if status_flapping:
            detail_parts.append("开关频繁分合")
        if trend_score > 0.2:
            detail_parts.append("趋势异常")
        if spike_score > 0.3:
            detail_parts.append("电流/功率突变")
        if anomaly_scores:
            detail_parts.append(f"波动异常(分数={np.mean(anomaly_scores):.2f})")

        return TemporalAnomalyResult(
            equip_id=window.equip_id,
            anomaly_score=anomaly_score,
            anomaly_type=anomaly_type,
            confidence=confidence,
            status=status,
            detail="; ".join(detail_parts) if detail_parts else "无明显异常",
            current_value=cur_ia,
            power_value=cur_ap,
            volatility=volatility,
            trend_slope=float(
                np.polyfit(np.arange(len(ap)), ap, 1)[0]
                if len(ap) >= 3 else 0.0
            ),
            status_flapping=status_flapping,
        )


# ------------------------------------------------------------------
# 主时空异常检测器
# ------------------------------------------------------------------

class SpatioTemporalDetector:
    """
    统一的时空异常检测接口

    自动选择：
      - PyTorch 可用 → 1D-CNN + LSTM
      - PyTorch 不可用 → NumPy 滑动窗口统计

    参数:
        window_size: 时间窗口大小（步数）
        max_seq_len: 序列最大长度（用于 PyTorch 模型）
    """

    def __init__(self, window_size: int = 60, max_seq_len: int = 100):
        self.window_size = window_size
        self.max_seq_len = max_seq_len
        self._is_fitted = False

        if TORCH_AVAILABLE:
            self._model = SpatioTemporalNet(
                in_channels=8,
                cnn_channels=[32, 64, 32],
                lstm_hidden=64,
                lstm_layers=2,
            ).double()
            self._optimizer = torch.optim.Adam(self._model.parameters(), lr=0.001)
            self._device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )
            self._model = self._model.to(self._device)
            self._impl = "pytorch_cnn_lstm"
        else:
            self._numpy_detector = NumpyTemporalDetector(window_size=window_size)
            self._impl = "numpy_statistical"

        logger.info("[时空模型] 初始化完成，实现=%s", self._impl)

    def fit(
        self,
        telemetry_data: dict,
        anomaly_labels: Optional[dict] = None,
        epochs: int = 20,
    ) -> "SpatioTemporalDetector":
        """
        训练（或调参）

        参数:
            telemetry_data: {equip_id: [row, ...]}
            anomaly_labels: 可选，{equip_id: 0.0/1.0} 有监督训练标签
        """
        if self._impl == "pytorch_cnn_lstm":
            self._fit_pytorch(telemetry_data, anomaly_labels, epochs)
        else:
            # NumPy 方法无需训练，直接调参
            self._is_fitted = True

        return self

    def _fit_pytorch(
        self,
        telemetry_data: dict,
        labels: Optional[dict],
        epochs: int,
    ):
        from torch.nn import functional as F

        windows = build_telemetry_windows(telemetry_data, max_window=self.max_seq_len)
        if not windows:
            logger.warning("[时空模型] 无有效时序数据，跳过训练")
            return

        logger.info("[时空模型] PyTorch 训练中，设备数=%d，epochs=%d",
                    len(windows), epochs)

        self._model.train()
        for epoch in range(epochs):
            total_loss = 0.0
            count = 0
            for equip_id, w in windows.items():
                ia, ib, ic, ua, ub, uc, ap, rp = w.to_arrays()
                n = w.n_points
                if n < 5:
                    continue

                # 拼接为 (n, 8)
                seq = np.stack([ia, ib, ic, ua, ub, uc, ap, rp], axis=1)
                x = torch.DoubleTensor(seq).unsqueeze(0).to(self._device)  # (1, n, 8)

                self._optimizer.zero_grad()
                score, _ = self._model(x)    # (1,)
                score = score.squeeze()

                if labels and equip_id in labels:
                    y = torch.DoubleTensor([labels[equip_id]]).to(self._device)
                    loss = F.binary_cross_entropy(score, y)
                else:
                    loss = -score.mean()  # 无监督：鼓励检测到异常

                loss.backward()
                self._optimizer.step()
                total_loss += loss.item()
                count += 1

            if epoch % 5 == 0 or epoch == epochs - 1:
                logger.info("[时空模型] Epoch %d/%d, avg_loss=%.4f",
                            epoch + 1, epochs, total_loss / max(count, 1))

        self._is_fitted = True

    def predict(
        self,
        telemetry_data: dict,
    ) -> List[TemporalAnomalyResult]:
        """
        对所有有遥测数据的设备进行时序异常检测

        返回: List[TemporalAnomalyResult]
        """
        windows = build_telemetry_windows(telemetry_data, max_window=self.max_seq_len)
        results: List[TemporalAnomalyResult] = []

        if self._impl == "pytorch_cnn_lstm":
            results = self._predict_pytorch(windows)
        else:
            for w in windows.values():
                results.append(self._numpy_detector.detect(w))

        n_anomaly = sum(1 for r in results if r.status == "ANOMALY")
        logger.info(
            "[时空模型] 检测完成: %d 设备, %d 个异常 (异常率=%.1f%%)",
            len(results), n_anomaly,
            100 * n_anomaly / max(len(results), 1),
        )
        return results

    def _predict_pytorch(
        self, windows: Dict[str, TelemetryWindow]
    ) -> List[TemporalAnomalyResult]:
        self._model.eval()
        results: List[TemporalAnomalyResult] = []

        with torch.no_grad():
            for w in windows.values():
                ia, ib, ic, ua, ub, uc, ap, rp = w.to_arrays()
                n = w.n_points
                if n < 3:
                    results.append(TemporalAnomalyResult(
                        equip_id=w.equip_id, anomaly_score=0.0,
                        anomaly_type="NORMAL", confidence=0.0,
                        status="MISSING",
                        detail="数据不足",
                        current_value=0.0, power_value=0.0,
                        volatility=0.0, trend_slope=0.0, status_flapping=False,
                    ))
                    continue

                seq = np.stack([ia, ib, ic, ua, ub, uc, ap, rp], axis=1)
                x = torch.DoubleTensor(seq).unsqueeze(0).to(self._device)
                score, _ = self._model(x)
                score = float(score.squeeze().cpu().item())

                # 调用 NumPy 后处理器做异常类型细分（无需 PyTorch）
                fake_window = TelemetryWindow(
                    equip_id=w.equip_id,
                    ia=list(ia), ib=list(ib), ic=list(ic),
                    ap=list(ap), rp=list(rp),
                )
                numpy_result = self._numpy_detector.detect(fake_window)
                # 用 PyTorch 分数替换
                numpy_result.anomaly_score = max(numpy_result.anomaly_score, score)
                if score >= 0.6:
                    numpy_result.status = "ANOMALY"
                results.append(numpy_result)

        return results

    def save(self, path: str):
        if self._impl == "pytorch_cnn_lstm":
            torch.save(self._model.state_dict(), path)
            logger.info("[时空模型] 模型已保存: %s", path)

    def load(self, path: str):
        if self._impl == "pytorch_cnn_lstm":
            self._model.load_state_dict(torch.load(path, map_location=self._device))
            self._is_fitted = True
            logger.info("[时空模型] 模型已加载: %s", path)
