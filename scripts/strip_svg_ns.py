"""把 output/svg 下所有带 ns0: 命名空间前缀的 SVG 转成浏览器友好版本。

策略（更稳）：
  1) 找到 `xmlns:ns0="..."` 这一段，删掉它（连同前后空格）。
  2) 把所有 ns0: 前缀（元素名/属性名前）替换成空串。
  3) 同样的处理对 ns1: / ns2: / nsN:（按 N 升序，避免 ns10 错位）。
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "output" / "svg"


def fix(svg_text: str) -> str:
    text = svg_text
    # 1) 删掉 xmlns:nsN="..." 的前缀声明
    text = re.sub(r'\s+xmlns:ns\d+="[^"]*"', "", text)
    # 2) 把所有 nsN: 前缀（不论前面是 <、空白、/>、还是别的）替换成空串
    text = re.sub(r"ns\d+:", "", text)
    return text


def main() -> None:
    changed = []
    for path in sorted(SVG_DIR.glob("*.svg")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "ns0:" not in raw and "ns1:" not in raw and "ns2:" not in raw:
            continue
        new = fix(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed.append((path.name, len(raw), len(new)))
    print(f"修复 {len(changed)} 个 SVG：")
    for name, old, new in changed:
        print(f"  - {name}: {old} -> {new} 字节")


if __name__ == "__main__":
    main()
