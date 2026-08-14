"""SVG 处理流程 - 闭环：解析 → 中间模型 → 修改/美化 → 重新生成 → 再解析验证。

任务：
1. 美化 LINE215.svg 和 LINE216.svg
2. LINE215：在开关00104（TMP00044018）和开关00102（TMP00044016）之间插入站房000300，含3个开关
3. LINE216：删除开关00024（TMP00043912），两侧设备直接连接
4. 每步生成中间模型（device.json、graph.json、topology.json）并验证闭环
"""
import os
import sys
import json
from pathlib import Path

from data_io.svg_reader import SvgDocument
from svg_io.svg_beautifier import beautify_svg_file
from svg_io.svg_editor import SvgEditor


class PipelineRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.svg_source_dir = self.project_root / "数据集更新版20260729" / "配网 svg"
        self.output_dir = self.project_root / "output"
        self.svg_output_dir = self.output_dir / "svg"
        self.ir_output_dir = self.output_dir / "intermediate"  # device/graph/topology
        self.svg_output_dir.mkdir(parents=True, exist_ok=True)
        self.ir_output_dir.mkdir(parents=True, exist_ok=True)

        self.results = {}

    # ------------------------------------------------------------------
    # 主流程
    # ------------------------------------------------------------------
    def run(self):
        print("=" * 70)
        print("SVG 处理闭环流程")
        print("=" * 70)

        # Step 1: 美化两个原始 SVG
        for fname in ["LINE215.svg", "LINE216.svg"]:
            src = str(self.svg_source_dir / fname)
            beautified = self._beautify(fname)
            self.results[fname] = {
                "beautified": beautified,
            }

        # Step 2: LINE215 插入站房
        line215_beautified = self.results["LINE215.svg"]["beautified"]
        line215_edited = self._add_station(line215_beautified)
        self.results["LINE215.svg"]["edited"] = line215_edited

        # Step 3: LINE216 删除开关
        line216_beautified = self.results["LINE216.svg"]["beautified"]
        line216_edited = self._delete_switch(line216_beautified)
        self.results["LINE216.svg"]["edited"] = line216_edited

        # Step 4: 导出中间模型并闭环验证
        final_files = {
            "LINE215_beautified": line215_beautified,
            "LINE215_with_000300": line215_edited,
            "LINE216_beautified": line216_beautified,
            "LINE216_del_switch": line216_edited,
        }
        print("\n" + "=" * 70)
        print("闭环验证与中间模型导出")
        print("=" * 70)
        all_pass = True
        for label, svg_path in final_files.items():
            ok = self._verify_and_export(label, svg_path)
            if not ok:
                all_pass = False

        self._generate_preview(final_files)

        print("\n" + "=" * 70)
        if all_pass:
            print("全部 SVG 闭环验证通过")
        else:
            print("部分 SVG 闭环验证失败，请检查日志")
        print("=" * 70)
        return all_pass

    # ------------------------------------------------------------------
    # 步骤实现
    # ------------------------------------------------------------------
    def _beautify(self, fname: str) -> str:
        print(f"\n>>> Step 1: 美化 {fname}")
        src = str(self.svg_source_dir / fname)
        dest = str(self.svg_output_dir / f"{Path(fname).stem}_beautified.svg")
        out = beautify_svg_file(src, output_path=dest)
        print(f"    输出: {out}")
        return out

    def _add_station(self, svg_path: str) -> str:
        print(f"\n>>> Step 2: LINE215 插入站房 000300")
        editor = SvgEditor(svg_path)
        editor.load()
        dest = str(self.svg_output_dir / "LINE215_with_000300.svg")
        edited_path = editor.add_station_with_switches(
            upstream_switch_id="TMP00044018",
            downstream_switch_id="TMP00044016",
            station_id="000300",
            switch_ids=["00301", "00302", "00303"],
            output_path=dest,
        )
        print(f"    编辑输出: {edited_path}")
        # 编辑后再按规范美化一次
        beautified_path = beautify_svg_file(edited_path, output_path=edited_path)
        print(f"    美化输出: {beautified_path}")
        return beautified_path

    def _delete_switch(self, svg_path: str) -> str:
        print(f"\n>>> Step 3: LINE216 删除开关 00024")
        editor = SvgEditor(svg_path)
        editor.load()
        dest = str(self.svg_output_dir / "LINE216_del_switch.svg")
        edited_path = editor.delete_switch("TMP00043912", output_path=dest)
        print(f"    编辑输出: {edited_path}")
        # 编辑后再按规范美化一次
        beautified_path = beautify_svg_file(edited_path, output_path=edited_path)
        print(f"    美化输出: {beautified_path}")
        return beautified_path

    # ------------------------------------------------------------------
    # 验证与导出
    # ------------------------------------------------------------------
    def _verify_and_export(self, label: str, svg_path: str) -> bool:
        print(f"\n--- 验证 [{label}] ---")
        doc = SvgDocument(svg_path)
        if not doc.parse():
            print(f"    [FAIL] 重新解析失败: {svg_path}")
            return False

        print(f"    重新解析成功: {len(doc.elements)} 设备, {len(doc.connections)} 连接, {len(doc.texts)} 文字")

        # 任务特定校验
        ok = True
        if "LINE215_with_000300" in label:
            ok = self._verify_line215_station(doc)
        elif "LINE216_del_switch" in label:
            ok = self._verify_line216_delete(doc)

        if not ok:
            return False

        # 导出中间模型
        base = self.ir_output_dir / label
        doc.export_elements_json(str(base / "device.json"))
        doc.export_connections_json(str(base / "graph.json"))
        topology = self._build_topology_json(doc)
        self._write_json(str(base / "topology.json"), topology)

        print(f"    [PASS] {label}")
        return True

    def _verify_line215_station(self, doc: SvgDocument) -> bool:
        station = doc.get_device_by_id("TMP000300")
        if station is None:
            print("    [FAIL] 站房 TMP000300 不存在")
            return False
        print(f"    站房 TMP000300: {station.element_name} at ({station.x:.2f}, {station.y:.2f})")

        for sw_id in ["TMP00301", "TMP00302", "TMP00303"]:
            sw = doc.get_device_by_id(sw_id)
            if sw is None:
                print(f"    [FAIL] 开关 {sw_id} 不存在")
                return False
            connected = doc.get_connected_devices(sw_id)
            print(f"    开关 {sw_id}: 连接 {connected}")

        # 检查 00301 与上游 00104 相连，00303 与下游 00102 相连
        up_connected = doc.get_connected_devices("TMP00301")
        if "TMP00044018" not in up_connected:
            print("    [FAIL] 00301 未连接到上游开关 TMP00044018")
            return False
        down_connected = doc.get_connected_devices("TMP00303")
        if "TMP00044016" not in down_connected:
            print("    [FAIL] 00303 未连接到下游开关 TMP00044016")
            return False
        if "TMP00301" not in doc.get_connected_devices("TMP00303"):
            print("    [FAIL] 00301 与 00303 未连接")
            return False
        return True

    def _verify_line216_delete(self, doc: SvgDocument) -> bool:
        if doc.get_device_by_id("TMP00043912") is not None:
            print("    [FAIL] 开关 TMP00043912 仍存在")
            return False
        # 检查是否有连接仍引用已删除开关
        for conn in doc.connections:
            if "TMP00043912" in conn.glink_refs:
                print(f"    [FAIL] 连接 {conn.connection_id} 仍引用 TMP00043912")
                return False
        for elem in doc.elements:
            if "TMP00043912" in elem.glink_refs:
                print(f"    [FAIL] 设备 {elem.element_id} 仍引用 TMP00043912")
                return False
        print("    开关 TMP00043912 已彻底删除，无残留引用")
        return True

    def _build_topology_json(self, doc: SvgDocument) -> dict:
        nodes = []
        for elem in doc.elements:
            nodes.append({
                "id": elem.element_id,
                "name": elem.element_name,
                "type": elem.element_type,
                "layer": elem.layer_name,
                "x": elem.x,
                "y": elem.y,
            })

        edges = []
        seen = set()
        for conn in doc.connections:
            if conn.start_device_id and conn.end_device_id:
                a, b = conn.start_device_id, conn.end_device_id
                if (a, b) not in seen and (b, a) not in seen:
                    edges.append({"source": a, "target": b, "id": conn.connection_id})
                    seen.add((a, b))

        return {
            "feeder_id": doc.feeder_id,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
        }

    @staticmethod
    def _write_json(path: str, data: dict):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # 预览
    # ------------------------------------------------------------------
    def _generate_preview(self, final_files: dict):
        html_path = self.svg_output_dir / "preview.html"
        html = ["<!DOCTYPE html><html><head><meta charset='UTF-8'><title>SVG Preview</title></head><body>"]
        html.append("<h1>SVG 闭环处理结果预览</h1>")
        for label, svg_path in final_files.items():
            fname = os.path.basename(svg_path)
            html.append(f"<h2>{label}</h2>")
            html.append(f'<object data="{fname}" type="image/svg+xml" width="1000" height="700"></object><br/>')
        html.append("</body></html>")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
        print(f"\n预览页面: {html_path}")


def main():
    runner = PipelineRunner()
    success = runner.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
