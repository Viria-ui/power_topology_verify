import zipfile, re
import sys

# Read path from command line argument
path = sys.argv[1]

with zipfile.ZipFile(path, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

text = re.sub(r'<[^>]+>', '\n', xml)
text = re.sub(r'\n+', '\n', text).strip()
print(text)
