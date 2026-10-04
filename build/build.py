import re, markdown, html
from diagrams2 import D
md=open('guide.md').read()
F=[ "a_j = g( Σ_i w_ij · x_i + b_j )",
 "P(x₁:T, e₁:T) = π(x₁) · b_x₁(e₁) · Π_{t=2..T} a(x_{t−1}, x_t) · b_xt(e_t)",
 "H(S) = − Σ_i p_i log₂ p_i          B(q) = −( q log₂ q + (1−q) log₂(1−q) )",
 "Gain(A) = H(S) − Σ_v ( |S_v| / |S| ) · H(S_v)",
 "Loss(w) = Σ_{j=1..N} ( y_j − (w₁ x_j + w₀) )²",
 "w₁ = ( N Σx_j y_j − Σx_j Σy_j ) / ( N Σx_j² − (Σx_j)² )          w₀ = ( Σy_j − w₁ Σx_j ) / N",
 "Support(X→Y) = (transactions containing X ∪ Y) / N\nConfidence(X→Y) = Support(X ∪ Y) / Support(X)\nLift(X→Y) = Confidence(X→Y) / Support(Y)",
 "Q(s,a) ← Q(s,a) + α [ r + γ · max_a' Q(s',a') − Q(s,a) ]",
 "P(C | x₁…xₙ) = P(C) · Π_i P(x_i | C) / P(x₁…xₙ)          Ĉ = argmax_C  P(C) · Π_i P(x_i | C)",
 "P(A | B) = P(A ∩ B) / P(B)",
 "P(A | B) = P(B | A) · P(A) / P(B)"]
it=iter(F)
md=re.sub(r'```latex\n.*?```',lambda m:'<div class="formula">'+html.escape(next(it))+'</div>',md,flags=re.S)
# split sections
head,*secs=re.split(r'(?m)^(?=## )',md)
keys=[f"Q{i}" for i in range(1,16)]+["SA","SB","SC",None]
out=[]
for s,k in zip(secs,keys):
    out.append(s+("\n\n"+"\n\n".join(D.get(k,[]))+"\n\n" if k else "\n\n"))
body="\n".join(out)
# protect svg/figure/div blocks from markdown processing
blocks=[]
def stash(m): blocks.append(m.group(0)); return f"\n\nXXBLOCK{len(blocks)-1}XX\n\n"
body=re.sub(r'<figure>.*?</figure>|<div class="formula">.*?</div>',stash,body,flags=re.S)
h=markdown.markdown(body,extensions=['tables','fenced_code','sane_lists'])
h=re.sub(r'<p>XXBLOCK(\d+)XX</p>',lambda m:blocks[int(m.group(1))],h)
h=h.replace('<h2>','<h2 class="sec">')
toc="".join(f'<li>{re.sub("<.*?>","",t)}</li>' for t in re.findall(r'<h2 class="sec">(.*?)</h2>',h))
css="""
@page{size:A4;margin:16mm 14mm}
body{font-family:Helvetica,Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#1b1b1b}
h1{font-size:26pt;margin:0 0 4px} h2.sec{font-size:15pt;color:#1a3f8f;border-bottom:2px solid #1a3f8f;padding-bottom:3px;margin-top:26px;page-break-before:always}
h3{font-size:12pt;color:#2b2b6b;margin:16px 0 6px}
table{border-collapse:collapse;width:100%;margin:8px 0 12px;font-size:9.5pt;page-break-inside:auto}
tr{page-break-inside:avoid} th{background:#1a3f8f;color:#fff;text-align:left} th,td{border:1px solid #9aa7c7;padding:4px 6px;vertical-align:top} tr:nth-child(even) td{background:#f3f6fd}
pre{background:#f6f8fa;border:1px solid #d5dbe5;padding:8px;font-size:8.6pt;white-space:pre-wrap;page-break-inside:avoid;border-radius:4px}
code{font-family:Menlo,Consolas,monospace;font-size:9pt}
.formula{background:#fffbea;border-left:4px solid #e0a800;padding:8px 12px;margin:8px 0;font-family:Cambria,Georgia,serif;font-size:11pt;white-space:pre-wrap;page-break-inside:avoid}
figure{margin:12px auto;text-align:center;page-break-inside:avoid;border:1px solid #dde3ef;border-radius:6px;padding:8px;background:#fcfdff}
figcaption{font-size:9pt;color:#444;font-style:italic;margin-top:4px}
.cover{text-align:center;padding:90px 0 30px} .cover p{color:#555}
ol.toc{columns:1;font-size:11pt;line-height:1.7}
"""
doc=f"""<!doctype html><meta charset=utf-8><title>Artificial Intelligence – Exam Answer Guide</title><style>{css}</style>
<div class=cover><h1>Artificial Intelligence</h1><h2 style="border:0;color:#1a3f8f">Exam Answer Guide</h2><p>15 questions with diagrams, tables and worked examples<br>plus supplements from the class notes</p></div>
<h3>Contents</h3><ol class=toc>{toc}</ol>
{h.split('</p>',1)[1] if False else h.replace('<h1>Artificial Intelligence – Exam Answer Guide</h1>','',1)}"""
doc=re.sub(r'<p>Oct 4, 2026.*?</p>','',doc,count=1)
open('guide.html','w').write(doc)
