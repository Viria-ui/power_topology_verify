class TelemetryEvaluator:
    """遥信遥测与主配接口规则评估器"""

    def __init__(self, telemetry_data=None, main_substation_data=None):
        # 遥信 (Switch Status), 遥测 (Current/Active Power)
        self.telemetry_data = telemetry_data or {}
        self.main_substation_data = main_substation_data or {}

    def evaluate_switch_status(self, equip_id, svg_is_open):
        """校验遥信与图纸开关逻辑状态"""
        tele_status = self.telemetry_data.get(equip_id, {}).get("switch_status")
        if tele_status is None:
            return True, 0.5, "缺乏遥信实时数据，使用默认概率"
        
        # tele_status: 1 为合闸(闭合)，0 为分闸(打开)
        tele_is_open = (tele_status == 0)
        if tele_is_open != svg_is_open:
            return False, 0.95, f"遥信实测状态({tele_status})与图纸标记不一致"
        return True, 0.99, "遥信实测与图纸一致"

    def evaluate_kcl_conservation(self, node_id, connected_lines):
        """根据遥测电流/功率进行 KCL 守恒判断 (物理连接置信度加权)"""
        if not connected_lines:
            return True, 0.5, "无遥测线路"
        
        total_current = 0
        has_telemetry = False
        for line_id in connected_lines:
            i_val = self.telemetry_data.get(line_id, {}).get("current")
            if i_val is not None:
                has_telemetry = True
                total_current += i_val
        
        if not has_telemetry:
            return True, 0.6, "未配置遥测表计"
        
        # 若总电流不守恒 (大于阈值)
        if abs(total_current) > 10.0:  # 10A 容差
            return False, 0.90, f"节点 KCL 电流不守恒，残差为 {total_current:.2f}A，可能存在隐形物理断线"
        return True, 0.95, "节点遥测 KCL 电流平衡"

    def verify_main_substation_interface(self, feeder_id, dsubstation_id):
        """校验主配网接口一致性规则"""
        if not dsubstation_id or dsubstation_id == "UNKNOWN":
            return False, 0.85, "配网馈线缺失主网变电站间隔挂接信息"
        return True, 0.95, f"主配网变电站接口 [{dsubstation_id}] 校验通过"