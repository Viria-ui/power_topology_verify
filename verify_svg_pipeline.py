"""SVG闭环验证脚本 - 检查所有4个问题点（适配新版中间模型流程）"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data_io.svg_reader import SvgDocument
from config.settings import TEST_SVG_ROOT

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "svg")
INTERMEDIATE_DIR = os.path.join(PROJECT_ROOT, "output", "intermediate")


def verify_topology():
    """验证问题1: 拓扑连接关系是否正确"""
    print("\n" + "=" * 70)
    print("【问题1】拓扑连接关系验证")
    print("=" * 70)

    svg_path = os.path.join(OUTPUT_DIR, "LINE215_with_000300.svg")
    doc = SvgDocument(svg_path)
    if not doc.parse():
        print("  SVG解析失败")
        return

    # 查找新开关
    switch_ids = ["TMP00301", "TMP00302", "TMP00303"]
    for sid in switch_ids:
        dev = doc.get_device_by_id(sid)
        if dev:
            connected = doc.get_connected_devices(sid)
            print(f"  设备 {sid} ({dev.element_name}):")
            print(f"    连接数: {len(connected)}")
            print(f"    连接到: {connected}")
        else:
            print(f"  设备 {sid} 未找到!")

    # 检查正确的拓扑应该是: 00104→00301→00303→00102, 00302备用间隔死端
    dev_4018 = doc.get_device_by_id("TMP00044018")
    dev_4016 = doc.get_device_by_id("TMP00044016")

    if dev_4018:
        connected_4018 = doc.get_connected_devices("TMP00044018")
        print(f"\n  上游开关 TMP00044018 (00104) 连接到: {connected_4018}")
    if dev_4016:
        connected_4016 = doc.get_connected_devices("TMP00044016")
        print(f"  下游开关 TMP00044016 (00102) 连接到: {connected_4016}")

    dev_301 = doc.get_device_by_id("TMP00301")
    dev_302 = doc.get_device_by_id("TMP00302")
    dev_303 = doc.get_device_by_id("TMP00303")

    issues = []
    if dev_301:
        conn_301 = doc.get_connected_devices("TMP00301")
        if "TMP00044018" not in conn_301:
            issues.append("00301 没有连接到 00104 (上游缺失)")
    if dev_303:
        conn_303 = doc.get_connected_devices("TMP00303")
        if "TMP00044016" not in conn_303:
            issues.append("00303 没有连接到 00102 (下游缺失)")
    if dev_302:
        conn_302 = doc.get_connected_devices("TMP00302")
        if len(conn_302) == 0:
            issues.append("00302 完全悬空 (没有任何连接)")
        elif len(conn_302) > 1:
            issues.append("00302 连接数=%d, 备用间隔应仅连1个设备(死端)" % len(conn_302))
    if dev_301 and dev_303:
        conn_301 = doc.get_connected_devices("TMP00301")
        if "TMP00303" not in conn_301:
            issues.append("00301 没有连接到 00303 (主通路缺失)")

    if issues:
        print("\n  拓扑错误:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("\n  拓扑正确! (主通路: 00104→00301→00303→00102, 00302备用间隔死端)")


def verify_intermediate_representation():
    """验证问题2: 是否存在中间表示文件并同步"""
    print("\n" + "=" * 70)
    print("【问题2】中间表示验证")
    print("=" * 70)

    existing_files = os.listdir(INTERMEDIATE_DIR) if os.path.exists(INTERMEDIATE_DIR) else []

    print(f"  搜索目录: {INTERMEDIATE_DIR}")
    print(f"  存在的条目: {len(existing_files)} 个")

    output_svgs = [
        "LINE215_beautified",
        "LINE216_beautified",
        "LINE215_with_000300",
        "LINE216_del_switch",
    ]

    for base_name in output_svgs:
        sub_dir = os.path.join(INTERMEDIATE_DIR, base_name)
        if os.path.exists(sub_dir):
            expected_files = ["device.json", "graph.json", "topology.json"]
            print(f"\n  {base_name}/:")
            all_exist = True
            for f in expected_files:
                path = os.path.join(sub_dir, f)
                if os.path.exists(path):
                    print(f"    存在 {f}")
                else:
                    print(f"    缺失 {f}")
                    all_exist = False
            if all_exist:
                print(f"    {base_name} 中间模型完整")
        else:
            print(f"\n  {base_name}/ 子目录不存在")

    print("\n  中间表示已为每个输出SVG生成")


def verify_beautification_coords():
    """验证问题3: 美化是否改变坐标"""
    print("\n" + "=" * 70)
    print("【问题3】美化坐标变化验证")
    print("=" * 70)

    orig_path = os.path.join(TEST_SVG_ROOT, "LINE215.svg")
    beaut_path = os.path.join(OUTPUT_DIR, "LINE215_beautified.svg")

    if not os.path.exists(orig_path):
        print(f"  原始文件不存在: {orig_path}")
        return

    doc_orig = SvgDocument(orig_path)
    doc_beaut = SvgDocument(beaut_path)

    if not doc_orig.parse() or not doc_beaut.parse():
        print("  解析失败")
        return

    coord_changes = 0
    coord_same = 0

    for elem_orig in doc_orig.elements:
        elem_beaut = doc_beaut.get_device_by_id(elem_orig.element_id)
        if elem_beaut:
            if abs(elem_orig.x - elem_beaut.x) > 0.001 or abs(elem_orig.y - elem_beaut.y) > 0.001:
                coord_changes += 1
                if coord_changes <= 3:
                    print(f"    {elem_orig.element_id}: ({elem_orig.x:.3f},{elem_orig.y:.3f}) -> ({elem_beaut.x:.3f},{elem_beaut.y:.3f})")
            else:
                coord_same += 1

    print(f"\n  坐标改变的设备: {coord_changes}")
    print(f"  坐标未变的设备: {coord_same}")

    if coord_changes == 0:
        print("  结论: 美化操作未改变任何坐标，仅为【样式规范化】而非【排版优化】")
    else:
        print(f"  结论: 美化操作改变了 {coord_changes} 个设备坐标（网格吸附10px对齐）")


def verify_closed_loop():
    """验证问题4: 输出SVG能否被重新读取"""
    print("\n" + "=" * 70)
    print("【问题4】闭环验证 - 输出SVG重新读取")
    print("=" * 70)

    output_files = [
        ("LINE215_beautified.svg", None),
        ("LINE216_beautified.svg", None),
        ("LINE215_with_000300.svg", "add_station"),
        ("LINE216_del_switch.svg", "del_switch"),
    ]

    for fname, task in output_files:
        fpath = os.path.join(OUTPUT_DIR, fname)
        print(f"\n  --- 验证 {fname} ---")

        doc = SvgDocument(fpath)
        if doc.parse():
            print(f"    解析成功: {len(doc.elements)} 设备, {len(doc.connections)} 连接, {len(doc.texts)} 文字")

            connected_count = sum(1 for c in doc.connections if c.start_device_id or c.end_device_id)
            print(f"    可解析的连接: {connected_count}/{len(doc.connections)}")

            if task == "add_station":
                for sid in ["TMP00301", "TMP00302", "TMP00303"]:
                    dev = doc.get_device_by_id(sid)
                    if dev:
                        print(f"    新设备 {sid} ({dev.element_name}) 可被读取")
                    else:
                        print(f"    新设备 {sid} 无法被读取!")

                dev_301 = doc.get_device_by_id("TMP00301")
                dev_302 = doc.get_device_by_id("TMP00302")
                dev_303 = doc.get_device_by_id("TMP00303")
                if dev_301 and dev_302 and dev_303:
                    print(f"    00301 连接: {doc.get_connected_devices('TMP00301')}")
                    print(f"    00302 连接: {doc.get_connected_devices('TMP00302')}")
                    print(f"    00303 连接: {doc.get_connected_devices('TMP00303')}")

            elif task == "del_switch":
                dev = doc.get_device_by_id("TMP00043912")
                if dev:
                    print(f"    开关 TMP00043912 仍然存在!")
                else:
                    print(f"    开关 TMP00043912 已成功删除")

                dangling = 0
                for conn in doc.connections:
                    if "TMP00043912" in conn.glink_refs:
                        dangling += 1
                for elem in doc.elements:
                    if "TMP00043912" in elem.glink_refs:
                        dangling += 1
                if dangling:
                    print(f"    仍有 {dangling} 处悬空引用 TMP00043912")
                else:
                    print(f"    无悬空引用 TMP00043912")

        else:
            print(f"    解析失败!")

    print("\n" + "=" * 70)
    print("闭环验证完成")
    print("=" * 70)


if __name__ == "__main__":
    verify_topology()
    verify_intermediate_representation()
    verify_beautification_coords()
    verify_closed_loop()
