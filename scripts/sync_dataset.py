# -*- coding: utf-8 -*-
"""同步比赛数据集到 input/sql_gbk，并叠加 8/21 增量补丁。

数据源：
  - 基础：数据集更新版20260729/sql形式数据集
  - 补丁：数据集更新版20260821/数据库更新脚本20260821.txt

用法:
  python scripts/sync_dataset.py
  python scripts/sync_dataset.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    DATASET_PATCH_821,
    DATASET_SQL_729,
    DATASET_UPDATE_NOTE_729,
    INPUT_SQL_DIR,
)


def detect_and_decode(raw: bytes) -> tuple[str, str]:
    for enc in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def copy_sql_base(src_dir: Path, dst_dir: Path, dry_run: bool = False) -> list[str]:
    """将 7/29 SQL 基础包复制到 input/sql_gbk（GBK 编码）。"""
    copied = []
    dst_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted(src_dir.glob("*.sql")):
        text, _ = detect_and_decode(src.read_bytes())
        dst = dst_dir / src.name
        if not dry_run:
            dst.write_bytes(text.encode("gbk", errors="replace"))
        copied.append(src.name)
    return copied


def patch_zwequipinfo(text: str) -> tuple[str, int]:
    """821: 主网设备类型 1312 → 1321。"""
    new_text, n = re.subn(r"(,'1312',)", r",'1321',", text)
    return new_text, n


def patch_pwterminal(text: str) -> tuple[str, int]:
    """821: 删除指定端点记录。"""
    remove_ids = {"TMP00062787", "TMP00063385"}
    lines = []
    removed = 0
    for line in text.splitlines(keepends=True):
        drop = False
        for rid in remove_ids:
            if f"'{rid}'" in line and "JBS_PWTERMINAL" in line.upper():
                drop = True
                break
        if drop:
            removed += 1
        else:
            lines.append(line)
    return "".join(lines), removed


def patch_zwterminal(text: str) -> tuple[str, int]:
    """821: 修正 TMP00048726 的连接节点。"""
    old = "'TMP00129617','TMP00048726','109000054006019'"
    new = "'TMP00129617','TMP00048726','109000054006023'"
    if old in text:
        return text.replace(old, new), 1
    # 兜底：按 EQUIP_ID 替换 CONNECTIVITYNODE_ID
    pattern = re.compile(
        r"(INSERT INTO \"EQUIP\"\.\"JBS_ZWTERMINAL\".*?VALUES\('TMP00129617','TMP00048726',')(\d+)('\);)"
    )
    new_text, n = pattern.subn(r"\g<1>109000054006023\g<3>", text)
    return new_text, n


def patch_pwreal(text: str) -> tuple[str, int]:
    """821: 按 (TRAN_ID, DATA_DATE) 去重，保留首条。"""
    seen: set[tuple[str, str]] = set()
    kept_lines = []
    removed = 0
    key_re = re.compile(
        r"INSERT INTO \"EQUIP\"\.\"JBS_PWREAL\".*?VALUES\('.*?','(.*?)','(.*?)',"
    )
    for line in text.splitlines(keepends=True):
        m = key_re.search(line)
        if m:
            key = (m.group(1), m.group(2))
            if key in seen:
                removed += 1
                continue
            seen.add(key)
        kept_lines.append(line)
    return "".join(kept_lines), removed


PATCHERS = {
    "EQUIP_JBS_ZWEQUIPINFO.sql": patch_zwequipinfo,
    "EQUIP_JBS_PWTERMINAL.sql": patch_pwterminal,
    "EQUIP_JBS_ZWTERMINAL.sql": patch_zwterminal,
    "EQUIP_JBS_PWREAL.sql": patch_pwreal,
}


def apply_patches_821(sql_dir: Path, dry_run: bool = False) -> dict[str, int]:
    """对 sql_gbk 目录应用 8/21 增量补丁。"""
    stats: dict[str, int] = {}
    for fname, patcher in PATCHERS.items():
        fpath = sql_dir / fname
        if not fpath.exists():
            continue
        text, _ = detect_and_decode(fpath.read_bytes())
        new_text, n = patcher(text)
        stats[fname] = n
        if n and not dry_run:
            fpath.write_bytes(new_text.encode("gbk", errors="replace"))
    return stats


def main():
    parser = argparse.ArgumentParser(description="同步 7/29 数据集并应用 8/21 SQL 补丁")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不写文件")
    args = parser.parse_args()

    src = Path(DATASET_SQL_729)
    dst = Path(INPUT_SQL_DIR)
    patch_file = Path(DATASET_PATCH_821)

    if not src.is_dir():
        print(f"❌ 未找到 7/29 SQL 目录: {src}")
        sys.exit(1)

    print("=" * 60)
    print("数据集同步：7/29 基础 + 8/21 补丁")
    print("=" * 60)
    if Path(DATASET_UPDATE_NOTE_729).is_file():
        print(f"📄 7/29 说明: {DATASET_UPDATE_NOTE_729}")
    if patch_file.is_file():
        print(f"📄 8/21 补丁: {patch_file}")
    print(f"源目录: {src}")
    print(f"目标目录: {dst}")
    if args.dry_run:
        print("模式: dry-run（不写入）")

    copied = copy_sql_base(src, dst, dry_run=args.dry_run)
    print(f"\n✅ 已复制 {len(copied)} 个 SQL 文件")

    stats = apply_patches_821(dst, dry_run=args.dry_run)
    print("\n📌 8/21 补丁应用结果:")
    for fname, n in stats.items():
        print(f"  • {fname}: {n} 处变更")

    if not args.dry_run:
        print(f"\n🎉 同步完成，运行时 SQL 路径: {dst}")
    else:
        print("\n(dry-run 完成，未写入文件)")


if __name__ == "__main__":
    main()
