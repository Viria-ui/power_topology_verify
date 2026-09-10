import sys
sys.path.insert(0, r'D:\挑战杯\tiaozhanbeigit\power_topology_verify')
from svg_io.quality_scorer import evaluate_svg_quality, export_quality_report
from svg_io.quality_scorer import compare_quality
from data_io.svg_reader import SvgParser
import os
import json
from config.settings import TEST_SVG_ROOT

ROOT = r'D:\挑战杯\tiaozhanbeigit\power_topology_verify'

# Find original SVG
orig_svg = os.path.join(TEST_SVG_ROOT, '10kVLINE018.svg')
if not os.path.exists(orig_svg):
    for f in os.listdir(TEST_SVG_ROOT):
        if 'LINE018' in f and f.endswith('.svg'):
            orig_svg = os.path.join(TEST_SVG_ROOT, f)
            break

beautified_svg = os.path.join(ROOT, 'output', 'svg', '10kVLINE018_beautified.svg')

print(f"Original SVG: {orig_svg}")
print(f"Beautified SVG: {beautified_svg}")

doc_before = SvgParser.parse(orig_svg)
doc_after = SvgParser.parse(beautified_svg)

before_defects, before_summary = evaluate_svg_quality(doc_before, stage='美化前')
after_defects, after_summary = evaluate_svg_quality(doc_after, stage='美化后')

print(f"Before: defects={len(before_defects)}, score={before_summary['quality_score']}")
print(f"After: defects={len(after_defects)}, score={after_summary['quality_score']}")

comparison = compare_quality(before_summary, after_summary)
print(f"Comparison: score_change={comparison['score_change']}, defects_reduced={comparison['defects_reduced']}")

# Save report
report = {
    'comparison': comparison,
    'before': before_summary,
    'after': after_summary,
    'before_defects_sample': before_defects[:50],
    'after_defects_sample': after_defects[:50],
    'algorithm_note': 'P2修复后评估：重叠阈值采用MIN_DEVICE_SIZE=15.0绝对尺寸，避免美化SVG缩放误报'
}
out = os.path.join(ROOT, 'output', 'reports', '10kVLINE018_美化质量对比报告.json')
export_quality_report(before_summary, after_summary, before_defects, after_defects, out)
print(f"Report saved: {out}")
