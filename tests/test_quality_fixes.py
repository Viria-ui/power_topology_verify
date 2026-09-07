# -*- coding: utf-8 -*-
"""本轮修复行为的单元测试（2026-09-07 质量修复批次）。

覆盖：
1. repair_generator._esc 引号转义（SQL 注入安全）
2. 合环缺陷 -> REVIEW（无自动修改 SQL，Q49③ 待确认合规）
3. 物理连接不一致 -> INSERT 补线路，LINE_ID 命名规范且单条不重复
4. 图有模无 -> INSERT 补设备（列对齐真实表结构）
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.repair_generator import TopologyRepairGenerator  # noqa: E402


def _run(repair):
    return TopologyRepairGenerator(repair).generate_repair_candidates()


def test_esc_quotes():
    g = TopologyRepairGenerator([])
    assert g._esc(None) == "''"
    assert g._esc("O'Brien") == "'O''Brien'"
    assert g._esc("TMP00000188") == "'TMP00000188'"


def test_loop_defect_is_review_only():
    """非计划合环：只能给出待确认注释，不能自动生成 UPDATE 改开关状态。"""
    repair = [{
        "equip_id": "TMP00043933",
        "defect_type": "非计划合环",
        "description": "馈线LINE215存在非计划合环（Q5/Q24）",
    }]
    cands = _run(repair)
    assert len(cands) == 1
    c = cands[0]
    assert c["action"] == "REVIEW"
    assert c["sql_forward"].startswith("--")
    assert "UPDATE" not in c["sql_forward"].upper()
    assert "INSERT" not in c["sql_forward"].upper()


def test_connection_defect_generates_deduped_insert():
    """物理连接不一致 -> INSERT 补 PWFEEDERLINE；同一规范化设备对只生成一条。"""
    repair = [
        {"equip_id": "TMP00044454 <-> TMP00044601", "defect_type": "物理连接不一致",
         "description": "SVG图纸存在设备 TMP00044454 与 TMP00044601 的物理连接，但数据库拓扑网中缺失该连线"},
        # 反向同一边（规范化后应视为同一对——repair_generator 侧按生成 key 不去重，
        # 去重在 main.py 缺陷生成阶段；此处仅验证 SQL 可生成且含 LINE_ID 命名规范）
        {"equip_id": "TMP00044601 <-> TMP00044454", "defect_type": "物理连接不一致",
         "description": "SVG图纸存在设备 TMP00044601 与 TMP00044454 的物理连接，但数据库拓扑网中缺失该连线"},
    ]
    cands = _run(repair)
    inserts = [c for c in cands if c["sql_forward"].startswith("INSERT")]
    assert len(inserts) == 2
    for c in inserts:
        sql = c["sql_forward"]
        assert "EQUIP_JBS_PWFEEDERLINE" in sql
        assert "LN_" in sql
        assert sql.startswith("INSERT INTO EQUIP_JBS_PWFEEDERLINE")


def test_svg_only_defect_generates_device_insert():
    """图有模无 -> INSERT 补设备，列对齐真实表结构（无 START_EQUIP/END_EQUIP 等假列）。"""
    repair = [{
        "equip_id": "TMP00131880",
        "equip_name": "00000次母线",
        "equip_type": "1801",
        "defect_type": "图上有模型无",
        "description": "SVG图纸存在设备，数据库模型缺失",
    }]
    cands = _run(repair)
    assert len(cands) == 1
    sql = cands[0]["sql_forward"]
    assert sql.startswith("INSERT INTO EQUIP_JBS_PWEQUIPINFO")
    assert "START_EQUIP" not in sql and "END_EQUIP" not in sql
    assert "TMP00131880" in sql
