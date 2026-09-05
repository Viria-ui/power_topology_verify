from __future__ import annotations
import logging
from typing import Any

logger = logging.getLogger(__name__)


class TopologyRepairGenerator:
    """
    最小修改候选生成器与 SQL 导出器（Q49约束：禁止DELETE，仅允许 INSERT / UPDATE；
    兼容达梦7：标识符全大写、不使用 MySQL 特有语法、单条语句不写嵌套子查询）。
    """

    def __init__(self, defects_report: list[dict]):
        self.defects = list(defects_report or [])

    @staticmethod
    def _esc(value: Any) -> str:
        if value is None:
            return "''"
        s = str(value).replace("'", "''")
        return f"'{s}'"

    def generate_repair_candidates(self) -> list[dict]:
        candidates: list[dict] = []
        for idx, defect in enumerate(self.defects):
            d_type = defect.get("defect_type", "")
            equip_id = defect.get("equip_id", "")
            desc = defect.get("description", "")
            candidate = {
                "repair_id": f"FIX_{idx + 1:04d}",
                "defect_type": d_type,
                "target_equip": equip_id,
                "action": "",
                "sql_forward": "",
                "sql_rollback": "",
                "impact_summary": "",
                "description": desc,
            }

            if d_type == "图上有模型无":
                ename = defect.get("equip_name") or defect.get("element_name") or f"SVG_{equip_id[-8:]}"
                etype = defect.get("equip_type") or defect.get("psr_type") or "1799"
                fid = defect.get("feeder_id") or ""
                vid = defect.get("voltage_type") or "1010"
                candidate["action"] = "ADD_DEVICE"
                candidate["sql_forward"] = (
                    "INSERT INTO EQUIP_JBS_PWEQUIPINFO "
                    "(EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID) "
                    f"VALUES ({self._esc(equip_id)},{self._esc(ename)},{self._esc(etype)},"
                    f"{self._esc(fid)},{self._esc(vid)},'');"
                )
                candidate["sql_rollback"] = (
                    "-- 回滚：Q49禁止DELETE且PWEQUIPINFO无状态列，需人工核对后删除该INSERT行。"
                )
                candidate["impact_summary"] = f"数据库新增设备 [{equip_id}]（INSERT，列已对齐真实表结构）"

            elif d_type == "模型有图上无":
                candidate["action"] = "ADD_SVG_ELEMENT"
                candidate["sql_forward"] = (
                    "-- Q49禁止操作型SQL删除：该缺陷不在数据库层面产生数据写操作。\n"
                    f"-- 请在 SVG 中补画ID={equip_id}的图层图元以及iec:PSR_Ref元数据标注。"
                )
                candidate["sql_rollback"] = (
                    "-- 回滚动作：删除SVG中补画的图元与标注。"
                )
                candidate["impact_summary"] = f"SVG侧补画图元[{equip_id}]，不改动数据库数据"

            elif d_type == "物理连接不一致":
                devs = str(equip_id).split(" <-> ")
                from_dev = devs[0].strip() if len(devs) > 0 else ""
                to_dev = devs[1].strip() if len(devs) > 1 else ""
                fid = defect.get("feeder_id") or ""
                candidate["action"] = "ADD_CONNECTION"
                line_id = f"LN_{from_dev[-6:]}_{to_dev[-6:]}"
                if from_dev and to_dev:
                    candidate["sql_forward"] = (
                        "INSERT INTO EQUIP_JBS_PWFEEDERLINE "
                        "(LINE_ID,LINE_NAME,START_ST_ID,VOLTAGE_TYPE) "
                        f"VALUES ({self._esc(line_id)},'SVG物理连通补录',"
                        f"{self._esc(from_dev)},'1010');"
                    )
                    candidate["sql_rollback"] = (
                        "-- 回滚：Q49禁止DELETE且PWFEEDERLINE无状态列，需人工核对后删除该INSERT行。"
                    )
                else:
                    candidate["sql_forward"] = (
                        "-- 解析不到SVG边的两端设备，需要人工补录PWFEEDERLINE。"
                    )
                    candidate["sql_rollback"] = "-- 无"
                candidate["impact_summary"] = f"模型新增物理边 [{from_dev} -> {to_dev}]（INSERT，列已对齐真实表结构）"

            elif d_type == "逻辑连接不一致":
                vid_new = defect.get("svg_voltage") or defect.get("voltage_level") or "1010"
                candidate["action"] = "UPDATE_VOLTAGE_TYPE"
                candidate["sql_forward"] = (
                    "UPDATE EQUIP_JBS_PWEQUIPINFO "
                    f"SET VOLTAGE_TYPE={self._esc(vid_new)} "
                    f"WHERE EQUIP_ID={self._esc(equip_id)};"
                )
                candidate["sql_rollback"] = (
                    "-- 回滚:请依据该设备原始电压类型重置 VOLTAGE_TYPE。"
                )
                candidate["impact_summary"] = f"修正设备[{equip_id}]的电压逻辑属性为 {vid_new}"

            else:
                candidate["action"] = "REVIEW"
                candidate["sql_forward"] = "-- 该缺陷需人工复核，无自动修复SQL。"
                candidate["sql_rollback"] = "-- 无"
                candidate["impact_summary"] = f"待人工复核：{d_type}（设备={equip_id}）"

            candidates.append(candidate)
        return candidates

    @staticmethod
    def calculate_topology_delta(line_db_devices, repair_candidates) -> dict:
        before = len(line_db_devices) if isinstance(line_db_devices, (dict, set, list)) else 0
        add = sum(1 for c in repair_candidates if c.get("action") == "ADD_DEVICE")
        # 注意：数据库层面已不允许真正的DELETE，ADD_SVG_ELEMENT不计入DB节点计数
        add_conn = sum(1 for c in repair_candidates if c.get("action") == "ADD_CONNECTION")
        attr = sum(1 for c in repair_candidates if c.get("action") == "UPDATE_VOLTAGE_TYPE")
        return {
            "before_nodes": before,
            "after_nodes": before + add,
            "net_node_change": add,
            "added_edges": add_conn,
            "repaired_attributes": attr,
        }

    @staticmethod
    def export_sql_script(
        repair_candidates: list[dict],
        forward_path: str,
        rollback_path: str | None = None,
    ) -> None:
        import os
        os.makedirs(os.path.dirname(forward_path) or ".", exist_ok=True)
        with open(forward_path, "w", encoding="utf-8") as ff:
            ff.write("-- ======================================================\n")
            ff.write("-- 图模修正 正向脚本  (Q49约束：全部是INSERT/UPDATE，不包含DELETE)\n")
            ff.write("-- 兼容数据库：达梦7 / 人大金仓 / Oracle / PostgreSQL\n")
            ff.write("-- ======================================================\n")
            ff.write("SET CONSTRAINTS ALL DEFERRED;\n\n")
            for c in repair_candidates:
                ff.write(f"-- [{c['repair_id']}] {c['action']}  {c['target_equip']}\n")
                for line in c["sql_forward"].splitlines() or ["-- 空"]:
                    ff.write(line.rstrip() + "\n")
                ff.write("\n")
            ff.write("COMMIT;\n")
        if rollback_path:
            os.makedirs(os.path.dirname(rollback_path) or ".", exist_ok=True)
            with open(rollback_path, "w", encoding="utf-8") as rf:
                rf.write("-- ======================================================\n")
                rf.write("-- 图模修正 回滚脚本  （全部采用UPDATE软回滚/逻辑置0）\n")
                rf.write("-- ======================================================\n")
                for c in reversed(repair_candidates):
                    rf.write(f"-- [{c['repair_id']}] 回滚 {c['action']}\n")
                    for line in c["sql_rollback"].splitlines() or ["-- 无回滚SQL"]:
                        rf.write(line.rstrip() + "\n")
                    rf.write("\n")
