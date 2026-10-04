import re, markdown
from stqa_diagrams import D

md = open('stqa.md').read()
# python-markdown needs 4-space nesting and a blank line before a list that follows a paragraph
md = re.sub(r'(?m)^ {2,3}(?=[-*] |\d+\. )', '    ', md)
md = re.sub(r'(?m)^(?![ \t]*([-*] |\d+\. |\|))([^\n]+)\n(?=[-*] |\d+\. )', r'\2\n\n', md)
secs = re.split(r'(?m)^(?=## )', md)[1:]
out = []
for i, s in enumerate(secs, 1):
    k = f"Q{i}"
    s = re.sub(r'FIG:(\w+):(\d+)', lambda m: D[m.group(1)][int(m.group(2))], s)
    out.append(s)
body = "\n\n".join(out)
blocks = []
def stash(m):
    blocks.append(m.group(0)); return f"\n\nXXBLOCK{len(blocks)-1}XX\n\n"
body = re.sub(r'<figure>.*?</figure>', stash, body, flags=re.S)
h = markdown.markdown(body, extensions=['tables', 'fenced_code', 'sane_lists'])
h = re.sub(r'<p>XXBLOCK(\d+)XX</p>', lambda m: blocks[int(m.group(1))], h)
h = h.replace('<h2>', '<h2 class="sec">')
toc = "".join(f'<li>{re.sub("<.*?>", "", t)}</li>' for t in re.findall(r'<h2 class="sec">(.*?)</h2>', h))
css = """
@page{size:A4;margin:16mm 14mm}
body{font-family:Helvetica,Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#1b1b1b}
h1{font-size:26pt;margin:0 0 4px} h2.sec{font-size:15pt;color:#1a3f8f;border-bottom:2px solid #1a3f8f;padding-bottom:3px;margin-top:26px;page-break-before:always}
h3{font-size:12pt;color:#2b2b6b;margin:16px 0 6px}
table{border-collapse:collapse;width:100%;margin:8px 0 12px;font-size:9.5pt;page-break-inside:auto}
tr{page-break-inside:avoid} th{background:#1a3f8f;color:#fff;text-align:left} th,td{border:1px solid #9aa7c7;padding:4px 6px;vertical-align:top} tr:nth-child(even) td{background:#f3f6fd}
pre{background:#f6f8fa;border:1px solid #d5dbe5;padding:8px;font-size:9pt;white-space:pre-wrap;page-break-inside:avoid;border-radius:4px}
code{font-family:Menlo,Consolas,monospace;font-size:9pt}
figure{margin:12px auto;text-align:center;page-break-inside:avoid;border:1px solid #dde3ef;border-radius:6px;padding:8px;background:#fcfdff}
figcaption{font-size:9pt;color:#444;font-style:italic;margin-top:4px}
.cover{text-align:center;padding:90px 0 30px} .cover p{color:#555}
ol.toc{font-size:11pt;line-height:1.7}
"""
doc = f"""<!doctype html><meta charset=utf-8><title>Software Testing and Quality Assurance – Exam Answer Guide</title><style>{css}</style>
<div class=cover><h1>Software Testing and Quality Assurance</h1><h2 style="border:0;color:#1a3f8f">Exam Answer Guide</h2><p>Mumbai University · BSc CS · Semester 5<br>15 most frequently asked questions, with diagrams, tables and worked examples</p></div>
<h3>Contents</h3><ol class=toc>{toc}</ol>
{h}"""
open('stqa_guide.html', 'w').write(doc)
