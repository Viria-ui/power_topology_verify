# PowerShell script to extract docx text
$sourcePath = "C:\Users\Xu's\Desktop\CP-202606-面向新型电力系统的配电网图模拓扑智能识别与修正研究比赛资料\附件：参考内容.docx"

python -c @"
import zipfile, re
path = r'$($sourcePath.Replace('\','\\'))'
with zipfile.ZipFile(path, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', '\n', xml)
text = re.sub(r'\n+', '\n', text).strip()
print(text)
"@
