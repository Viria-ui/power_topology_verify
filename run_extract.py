import subprocess
import tempfile
import os

script = '''
import zipfile, re
path = r"C:\\Users\\Xu's\\Desktop\\CP-202606-面向新型电力系统的配电网图模拓扑智能识别与修正研究比赛资料\\附件：参考内容.docx"
with zipfile.ZipFile(path, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', '\n', xml)
text = re.sub(r'\n+', '\n', text).strip()
print(text)
'''

# Write script to temp file in the project directory (no apostrophe in path)
temp_script = r"c:\Users\Xu's\Desktop\power_topology_verify\temp_extract.py"
with open(temp_script, 'w', encoding='utf-8') as f:
    f.write(script)

# Now execute it
result = subprocess.run(['python', temp_script], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
