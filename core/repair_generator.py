import json

class TopologyRepairGenerator:
    """最小修改候选生成器与 SQL 导出器"""
    
    def __init__(self, defects_report):
        self.defects = defects_report

    def generate_repair_candidates(self):
        """为每类缺陷生成包含正向 SQL、回滚 SQL 及修补动作的候选对象"""
        candidates = []
        
        for idx, defect in enumerate(self.defects):
            d_type = defect.get("defect_type")
            equip_id = defect.get("equip_id")
            desc = defect.get("description", "")
            
            candidate = {
                "repair_id": f"FIX_{idx + 1:04d}",
                "defect_type": d_type,
                "target_equip": equip_id,
                "action": "",
                "sql_forward": "",
                "sql_rollback": "",
                "impact_summary": ""
            }
            
            # 分类 1：图上有模型无 -> 动作：补设备
            if d_type == "图上有模型无":
                candidate["action"] = "ADD_DEVICE"
                candidate["sql_forward"] = (
                    f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME, STATUS) "
                    f"VALUES ('{equip_id}', 'AUTO_FIX_{equip_id}', '1');"
                )
                candidate["sql_rollback"] = (
                    f"DELETE FROM EQUIP_JBS_PWEQUIPINFO WHERE EQUIP_ID = '{equip_id}';"
                )
                candidate["impact_summary"] = f"模型新增节点 [{equip_id}]"

            # 分类 2：模型有图上无 -> 动作：删/软删除设备
            elif d_type == "模型有图上无":
                candidate["action"] = "DELETE_DEVICE"
                candidate["sql_forward"] = (
                    f"UPDATE EQUIP_JBS_PWEQUIPINFO SET STATUS = '0' WHERE EQUIP_ID = '{equip_id}';"
                )
                candidate["sql_rollback"] = (
                    f"UPDATE EQUIP_JBS_PWEQUIPINFO SET STATUS = '1' WHERE EQUIP_ID = '{equip_id}';"
                )
                candidate["impact_summary"] = f"模型逻辑停用设备 [{equip_id}]"

            # 分类 3：物理连接不一致 -> 动作：新增物理连接
            elif d_type == "物理连接不一致":
                candidate["action"] = "ADD_CONNECTION"
                # equip_id 格式为 "devA <-> devB"
                devs = equip_id.split(" <-> ")
                from_dev = devs[0] if len(devs) > 0 else "UNKNOWN"
                to_dev = devs[1] if len(devs) > 1 else "UNKNOWN"
                
                candidate["sql_forward"] = (
                    f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (START_EQUIP, END_EQUIP) "
                    f"VALUES ('{from_dev}', '{to_dev}');"
                )
                candidate["sql_rollback"] = (
                    f"DELETE FROM EQUIP_JBS_PWFEEDERLINE "
                    f"WHERE START_EQUIP = '{from_dev}' AND END_EQUIP = '{to_dev}';"
                )
                candidate["impact_summary"] = f"模型新增物理连接边 [{from_dev} -> {to_dev}]"

            # 分类 4：逻辑连接不一致 -> 动作：修正接口/属性
            elif d_type == "逻辑连接不一致":
                candidate["action"] = "UPDATE_PORT"
                candidate["sql_forward"] = (
                    f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE = '10kV' WHERE EQUIP_ID = '{equip_id}';"
                )
                candidate["sql_rollback"] = (
                    f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE = 'ORIGINAL_VAL' WHERE EQUIP_ID = '{equip_id}';"
                )
                candidate["impact_summary"] = f"修正设备 [{equip_id}] 的逻辑接口属性"

            candidates.append(candidate)
            
        return candidates

    @staticmethod
    def calculate_topology_delta(before_topo, repair_candidates):
        """计算修正前后的拓扑差异"""
        before_node_count = len(before_topo.device_map) if hasattr(before_topo, 'device_map') else 0
        
        # 统计修补意图带来的增量
        added_nodes = sum(1 for c in repair_candidates if c["action"] == "ADD_DEVICE")
        deleted_nodes = sum(1 for c in repair_candidates if c["action"] == "DELETE_DEVICE")
        added_edges = sum(1 for c in repair_candidates if c["action"] == "ADD_CONNECTION")
        
        after_node_count = before_node_count + added_nodes - deleted_nodes
        
        return {
            "before_nodes": before_node_count,
            "after_nodes": after_node_count,
            "net_node_change": added_nodes - deleted_nodes,
            "added_edges": added_edges,
            "repaired_attributes": sum(1 for c in repair_candidates if c["action"] == "UPDATE_PORT")
        }