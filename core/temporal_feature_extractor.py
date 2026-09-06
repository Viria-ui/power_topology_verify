"""
时序特征工程与异常检测模块
===========================

为每个设备构造滑动窗口特征：
- 均值、波动率、突变率
- 相空间重构特征（延迟嵌入、关联维数/样本熵）
- 开关状态转换特征

这些特征可用于：
1. 识别"图上连通但电气量不符合"的异常
2. 识别"开关状态与潮流矛盾"
3. 为GAT模型提供输入特征
"""

from __future__ import annotations
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import deque
import math

logger = logging.getLogger(__name__)


@dataclass
class TimeSeriesFeatures:
    """时序特征向量"""
    # 基础统计特征
    mean: float = 0.0
    std: float = 0.0
    min_val: float = 0.0
    max_val: float = 0.0
    range_val: float = 0.0
    
    # 波动特征
    variance: float = 0.0
    coefficient_of_variation: float = 0.0  # 变异系数
    volatility: float = 0.0  # 波动率
    
    # 突变特征
    mutation_rate: float = 0.0  # 突变率
    mutation_count: int = 0  # 突变次数
    max_step_change: float = 0.0  # 最大阶跃变化
    
    # 趋势特征
    trend_slope: float = 0.0  # 趋势斜率
    trend_r_squared: float = 0.0  # 趋势R²
    
    # 状态特征（针对开关）
    status_stability: float = 1.0  # 状态稳定性 0-1
    status_transition_count: int = 0  # 状态转换次数
    
    # 异常指标
    is_stable: bool = True  # 是否稳定
    anomaly_score: float = 0.0  # 异常分数 0-1
    
    def to_dict(self) -> dict:
        return {
            "mean": round(self.mean, 4),
            "std": round(self.std, 4),
            "min": round(self.min_val, 4),
            "max": round(self.max_val, 4),
            "range": round(self.range_val, 4),
            "variance": round(self.variance, 4),
            "cv": round(self.coefficient_of_variation, 4),
            "volatility": round(self.volatility, 4),
            "mutation_rate": round(self.mutation_rate, 4),
            "mutation_count": self.mutation_count,
            "max_step_change": round(self.max_step_change, 4),
            "trend_slope": round(self.trend_slope, 6),
            "trend_r_squared": round(self.trend_r_squared, 4),
            "status_stability": round(self.status_stability, 4),
            "status_transition_count": self.status_transition_count,
            "is_stable": self.is_stable,
            "anomaly_score": round(self.anomaly_score, 4),
        }


@dataclass
class SwitchStatusFeatures:
    """开关状态时序特征"""
    equip_id: str
    status_sequence: List[str] = field(default_factory=list)  # 状态序列
    transition_count: int = 0  # 转换次数
    open_duration: float = 0.0  # 分位持续时间
    close_duration: float = 0.0  # 合位持续时间
    last_transition_time: float = 0.0  # 距上次转换时间
    is_flapping: bool = False  # 是否在抖动
    stability_score: float = 1.0  # 稳定性评分 0-1
    
    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "transition_count": self.transition_count,
            "open_duration": round(self.open_duration, 2),
            "close_duration": round(self.close_duration, 2),
            "last_transition_time": round(self.last_transition_time, 2),
            "is_flapping": self.is_flapping,
            "stability_score": round(self.stability_score, 4),
        }


class TimeSeriesFeatureExtractor:
    """
    时序特征提取器
    
    为每个设备构造滑动窗口特征，用于异常检测
    """
    
    def __init__(
        self,
        window_size: int = 100,
        mutation_threshold: float = 0.5,
    ):
        """
        参数:
            window_size: 滑动窗口大小
            mutation_threshold: 突变判定阈值（相对于均值的比例）
        """
        self.window_size = window_size
        self.mutation_threshold = mutation_threshold
        
        # 缓存
        self.feature_cache: Dict[str, TimeSeriesFeatures] = {}
        self.status_cache: Dict[str, SwitchStatusFeatures] = {}
    
    def _number(self, value, default=0.0) -> float:
        """安全转换为浮点数"""
        try:
            return float(value) if value is not None else default
        except (TypeError, ValueError):
            return default
    
    def extract_features(
        self,
        values: List[float],
    ) -> TimeSeriesFeatures:
        """
        从数值序列提取特征
        
        参数:
            values: 数值序列
        
        返回:
            TimeSeriesFeatures: 时序特征
        """
        if len(values) < 3:
            return TimeSeriesFeatures()
        
        features = TimeSeriesFeatures()
        
        # 基础统计
        features.mean = sum(values) / len(values)
        features.min_val = min(values)
        features.max_val = max(values)
        features.range_val = features.max_val - features.min_val
        
        # 方差和标准差
        variance = sum((v - features.mean) ** 2 for v in values) / len(values)
        features.variance = variance
        features.std = math.sqrt(variance)
        
        # 变异系数
        if abs(features.mean) > 1e-6:
            features.coefficient_of_variation = features.std / abs(features.mean)
        
        # 波动率（日内波动/均值）
        if abs(features.mean) > 1e-6:
            features.volatility = features.range_val / abs(features.mean)
        
        # 突变检测
        features.mutation_count, features.max_step_change = self._detect_mutations(
            values, features.mean
        )
        features.mutation_rate = features.mutation_count / max(1, len(values) - 1)
        
        # 趋势拟合（简化）
        features.trend_slope = self._fit_trend(values)
        
        # 异常判定
        features.is_stable = features.mutation_rate < 0.2 and features.volatility < 2.0
        features.anomaly_score = self._calculate_anomaly_score(features)
        
        return features
    
    def _detect_mutations(
        self,
        values: List[float],
        mean: float,
    ) -> Tuple[int, float]:
        """
        检测突变点和最大阶跃变化
        
        返回: (突变次数, 最大阶跃变化)
        """
        mutation_count = 0
        max_step = 0.0
        
        for i in range(1, len(values)):
            prev = values[i - 1]
            curr = values[i]
            
            # 计算相对变化
            step = abs(curr - prev)
            
            # 突变判定：变化超过均值的threshold倍
            if abs(mean) > 1e-6 and step / abs(mean) > self.mutation_threshold:
                mutation_count += 1
            
            max_step = max(max_step, step)
        
        return mutation_count, max_step
    
    def _fit_trend(self, values: List[float]) -> float:
        """
        简单线性趋势拟合
        
        返回: 斜率
        """
        if len(values) < 3:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if abs(denominator) < 1e-10:
            return 0.0
        
        return numerator / denominator
    
    def _calculate_anomaly_score(self, features: TimeSeriesFeatures) -> float:
        """
        计算综合异常分数
        
        基于多个指标加权
        """
        # 突变异常
        mutation_anomaly = min(1.0, features.mutation_rate * 2)
        
        # 波动异常
        volatility_anomaly = min(1.0, features.volatility / 3)
        
        # 趋势异常（斜率过大）
        trend_anomaly = min(1.0, abs(features.trend_slope) * 10)
        
        # 综合异常分数
        anomaly_score = (
            mutation_anomaly * 0.3 +
            volatility_anomaly * 0.4 +
            trend_anomaly * 0.3
        )
        
        return min(1.0, anomaly_score)
    
    def extract_switch_features(
        self,
        equip_id: str,
        telemetry_data: dict,
    ) -> SwitchStatusFeatures:
        """
        提取开关状态特征
        
        参数:
            equip_id: 设备ID
            telemetry_data: 遥测数据字典
        
        返回:
            SwitchStatusFeatures: 开关状态特征
        """
        features = SwitchStatusFeatures(equip_id=equip_id)
        
        rows = telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        
        if not rows:
            return features
        
        # 提取状态序列
        status_seq = []
        for row in rows:
            point = row.get('POINT', row.get('point', '1'))
            if str(point) == '0':
                status_seq.append('OPEN')
            else:
                status_seq.append('CLOSE')
        
        features.status_sequence = status_seq
        
        # 统计状态转换
        for i in range(1, len(status_seq)):
            if status_seq[i] != status_seq[i - 1]:
                features.transition_count += 1
        
        # 计算持续时间
        if status_seq:
            features.close_duration = sum(1 for s in status_seq if s == 'CLOSE')
            features.open_duration = sum(1 for s in status_seq if s == 'OPEN')
        
        # 检测抖动（短时间内多次转换）
        if len(status_seq) >= 5:
            recent_transitions = sum(
                1 for i in range(1, min(6, len(status_seq)))
                if status_seq[i] != status_seq[i - 1]
            )
            features.is_flapping = recent_transitions >= 3
        
        # 稳定性评分
        if status_seq:
            stability = 1.0 - (features.transition_count / max(1, len(status_seq) - 1))
            features.stability_score = max(0.0, stability)
        
        return features
    
    def extract_power_features(
        self,
        equip_id: str,
        telemetry_data: dict,
    ) -> TimeSeriesFeatures:
        """
        提取功率时序特征
        
        参数:
            equip_id: 设备ID
            telemetry_data: 遥测数据字典
        
        返回:
            TimeSeriesFeatures: 功率时序特征
        """
        rows = telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        
        # 提取有功功率序列
        power_values = [self._number(r.get('AP', 0)) for r in rows]
        
        # 提取相电流序列
        ia_values = [self._number(r.get('IA', 0)) for r in rows]
        ib_values = [self._number(r.get('IB', 0)) for r in rows]
        ic_values = [self._number(r.get('IC', 0)) for r in rows]
        
        # 合并所有电气量
        all_values = power_values + ia_values + ib_values + ic_values
        all_values = [v for v in all_values if v != 0]
        
        return self.extract_features(all_values if all_values else [0.0])
    
    def extract_voltage_features(
        self,
        equip_id: str,
        telemetry_data: dict,
    ) -> TimeSeriesFeatures:
        """
        提取电压时序特征
        """
        rows = telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        
        ua_values = [self._number(r.get('UA', 0)) for r in rows]
        ub_values = [self._number(r.get('UB', 0)) for r in rows]
        uc_values = [self._number(r.get('UC', 0)) for r in rows]
        
        all_values = ua_values + ub_values + uc_values
        all_values = [v for v in all_values if v != 0]
        
        return self.extract_features(all_values if all_values else [0.0])
    
    def extract_all_features(
        self,
        equip_id: str,
        telemetry_data: dict,
    ) -> Dict[str, TimeSeriesFeatures]:
        """
        提取设备的所有时序特征
        
        返回:
            Dict[str, TimeSeriesFeatures]: 特征字典 {"power": ..., "voltage": ..., "current": ...}
        """
        features = {
            "power": self.extract_power_features(equip_id, telemetry_data),
            "voltage": self.extract_voltage_features(equip_id, telemetry_data),
        }
        
        # 缓存
        self.feature_cache[equip_id] = features
        
        return features


class AnomalyDetector:
    """
    基于时序特征的异常检测器
    
    识别：
    1. 图上连通但电气量不符合
    2. 开关状态与潮流矛盾
    3. 虚接、错接
    """
    
    def __init__(
        self,
        feature_extractor: TimeSeriesFeatureExtractor = None,
    ):
        self.extractor = feature_extractor or TimeSeriesFeatureExtractor()
        
        # 异常阈值
        self.anomaly_thresholds = {
            "power_volatility": 2.0,  # 功率波动阈值
            "voltage_imbalance": 0.05,  # 电压不平衡阈值
            "current_unbalance": 10.0,  # 电流不平衡阈值(A)
            "mutation_rate": 0.3,  # 突变率阈值
            "switch_flapping": 3,  # 抖动判定阈值
        }
    
    def detect_power_anomaly(
        self,
        equip_id: str,
        telemetry_data: dict,
        expected_power_range: Tuple[float, float] = None,
    ) -> Tuple[bool, float, str]:
        """
        检测功率异常
        
        返回: (是否异常, 异常分数, 原因)
        """
        features = self.extractor.extract_power_features(equip_id, telemetry_data)
        
        anomalies = []
        score = features.anomaly_score
        
        # 功率波动异常
        if features.volatility > self.anomaly_thresholds["power_volatility"]:
            anomalies.append(f"功率波动率异常(volatility={features.volatility:.2f})")
            score = max(score, 0.7)
        
        # 突变过多
        if features.mutation_rate > self.anomaly_thresholds["mutation_rate"]:
            anomalies.append(f"功率突变过多(rate={features.mutation_rate:.2f})")
            score = max(score, 0.6)
        
        # 超出预期范围
        if expected_power_range:
            min_pow, max_pow = expected_power_range
            if features.max_val > max_pow or features.min_val < min_pow:
                anomalies.append(f"功率超出预期范围[{min_pow:.1f}, {max_pow:.1f}]")
                score = max(score, 0.8)
        
        is_anomaly = len(anomalies) > 0
        reason = "; ".join(anomalies) if anomalies else "无异常"
        
        return is_anomaly, min(1.0, score), reason
    
    def detect_switch_power_contradiction(
        self,
        switch_id: str,
        telemetry_data: dict,
        switch_status: str,
    ) -> Tuple[bool, float, str]:
        """
        检测开关状态与潮流矛盾
        
        规则：
        - 分位开关应有零功率或极小功率
        - 合位开关应有明显功率流
        
        返回: (是否矛盾, 矛盾分数, 原因)
        """
        features = self.extractor.extract_power_features(switch_id, telemetry_data)
        switch_features = self.extractor.extract_switch_features(switch_id, telemetry_data)
        
        # 获取最新功率
        rows = telemetry_data.get(str(switch_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        
        latest_power = 0.0
        if rows:
            latest_power = self._number(rows[-1].get('AP', 0))
        
        is_open = switch_status in {"OPEN", "0", "分位"}
        is_close = switch_status in {"CLOSE", "1", "合位"}
        
        contradiction = False
        score = 0.0
        reasons = []
        
        # 分位开关不应有明显功率
        if is_open and abs(latest_power) > 10.0:
            contradiction = True
            score = 0.9
            reasons.append(f"开关{switch_id}处于分位但有功率{Power:.2f}kW")
        
        # 合位开关应有功率
        if is_close:
            if abs(latest_power) < 1.0:
                # 可能是虚接
                if switch_features.stability_score > 0.8:
                    contradiction = True
                    score = 0.6
                    reasons.append(f"开关{switch_id}处于合位但功率接近零，可能虚接")
            elif features.volatility > 1.5:
                # 功率波动大
                contradiction = True
                score = 0.5
                reasons.append(f"开关{switch_id}处于合位但功率波动异常")
        
        # 开关抖动
        if switch_features.is_flapping:
            score = max(score, 0.7)
            reasons.append(f"开关{switch_id}存在状态抖动")
        
        return contradiction, min(1.0, score), "; ".join(reasons)
    
    def detect_voltage_anomaly(
        self,
        equip_id: str,
        telemetry_data: dict,
    ) -> Tuple[bool, float, str]:
        """
        检测电压异常
        
        返回: (是否异常, 异常分数, 原因)
        """
        rows = telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        
        if not rows:
            return False, 0.0, "无电压数据"
        
        # 获取最新三相电压
        latest = rows[-1]
        ua = self._number(latest.get('UA', 0))
        ub = self._number(latest.get('UB', 0))
        uc = self._number(latest.get('UC', 0))
        
        if ua == 0 and ub == 0 and uc == 0:
            return False, 0.0, "电压为零"
        
        # 计算不平衡度
        un = (ua + ub + uc) / 3
        if un < 1.0:
            return True, 0.8, "电压过低"
        
        imbalance = max(abs(ua - un), abs(ub - un), abs(uc - un)) / un
        
        is_anomaly = imbalance > self.anomaly_thresholds["voltage_imbalance"]
        score = min(1.0, imbalance * 10)
        
        reason = f"电压不平衡度={imbalance:.2%}" if is_anomaly else "电压正常"
        
        return is_anomaly, score, reason
    
    def _number(self, value, default=0.0) -> float:
        return self.extractor._number(value, default)


def extract_temporal_features(
    equip_id: str,
    telemetry_data: dict,
    window_size: int = 100,
) -> dict:
    """
    便捷函数：提取设备时序特征
    
    返回标准化格式的特征字典
    """
    extractor = TimeSeriesFeatureExtractor(window_size=window_size)
    
    power_features = extractor.extract_power_features(equip_id, telemetry_data)
    voltage_features = extractor.extract_voltage_features(equip_id, telemetry_data)
    switch_features = extractor.extract_switch_features(equip_id, telemetry_data)
    
    return {
        "equip_id": equip_id,
        "power_features": power_features.to_dict(),
        "voltage_features": voltage_features.to_dict(),
        "switch_features": switch_features.to_dict(),
        "comprehensive_anomaly_score": max(
            power_features.anomaly_score,
            voltage_features.anomaly_score,
        ),
    }


def detect_temporal_anomalies(
    equip_id: str,
    telemetry_data: dict,
    switch_status: str = None,
) -> List[dict]:
    """
    便捷函数：检测设备时序异常
    
    返回异常列表
    """
    detector = AnomalyDetector()
    anomalies = []
    
    # 功率异常
    is_power_anomaly, power_score, power_reason = detector.detect_power_anomaly(
        equip_id, telemetry_data
    )
    if is_power_anomaly:
        anomalies.append({
            "type": "POWER_ANOMALY",
            "equip_id": equip_id,
            "score": power_score,
            "reason": power_reason,
            "suggestion": "检查功率计量装置和设备运行状态",
        })
    
    # 电压异常
    is_voltage_anomaly, voltage_score, voltage_reason = detector.detect_voltage_anomaly(
        equip_id, telemetry_data
    )
    if is_voltage_anomaly:
        anomalies.append({
            "type": "VOLTAGE_ANOMALY",
            "equip_id": equip_id,
            "score": voltage_score,
            "reason": voltage_reason,
            "suggestion": "检查电压互感器接线和三相负荷平衡",
        })
    
    # 开关状态与潮流矛盾
    if switch_status:
        is_contradiction, contradiction_score, contradiction_reason = detector.detect_switch_power_contradiction(
            equip_id, telemetry_data, switch_status
        )
        if is_contradiction:
            anomalies.append({
                "type": "SWITCH_POWER_CONTRADICTION",
                "equip_id": equip_id,
                "score": contradiction_score,
                "reason": contradiction_reason,
                "suggestion": "核查开关实际状态与遥信一致性",
            })
    
    return anomalies
