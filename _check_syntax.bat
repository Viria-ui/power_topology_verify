@echo off
cd /d C:\Users\Xus\Desktop\power_topology_verify
python -m py_compile svg_io\quality_scorer.py
echo quality_scorer: %ERRORLEVEL%
python -m py_compile svg_io\svg_beautifier.py
echo svg_beautifier: %ERRORLEVEL%
pause
