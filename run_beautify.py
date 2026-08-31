
import os
import sys
import traceback
# Add project root to path
sys.path.append(os.getcwd())

from svg_io.svg_beautifier import beautify_svg_file
from config.settings import TEST_SVG_ROOT

project_root = os.getcwd()
svg_dir = TEST_SVG_ROOT
output_dir = os.path.join(project_root, "output", "svg")
os.makedirs(output_dir, exist_ok=True)

for fname in ["LINE215.svg", "LINE216.svg"]:
    fpath = os.path.join(svg_dir, fname)
    if os.path.exists(fpath):
        try:
            print(f"Beautifying {fname}...")
            out_path = os.path.join(output_dir, f"{os.path.splitext(fname)[0]}_beautified.svg")
            beautify_svg_file(fpath, out_path)
            print(f"Finished {fname}")
        except Exception as e:
            print(f"Error beautifying {fname}:")
            traceback.print_exc()
    else:
        print(f"File not found: {fpath}")
