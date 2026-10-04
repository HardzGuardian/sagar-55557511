# Small SVG helpers for exam-guide diagrams
BW=' font-weight="bold"'
IT=' font-style="italic"'
F='font-family="Helvetica,Arial,sans-serif"'
def svg(w,h,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" {F} font-size="13">{body}</svg>'
DEFS='<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#444"/></marker></defs>'
def box(x,y,w,h,t,fill="#e8f0fe",stroke="#3b6fd4",fs=13,bold=False):
    lines=t.split("\n"); n=len(lines); out=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
    for i,l in enumerate(lines):
        yy=y+h/2+(i-(n-1)/2)*(fs+3)+4
        out+=f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-size="{fs}" {BW if bold else ""}>{l}</text>'
    return out
def arrow(x1,y1,x2,y2,label="",dash=False,lx=0,ly=-5,color="#444"):
    d=' stroke-dasharray="5,3"' if dash else ''
    o=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5"{d} marker-end="url(#a)"/>'
    if label: o+=f'<text x="{(x1+x2)/2+lx}" y="{(y1+y2)/2+ly}" text-anchor="middle" font-size="11" fill="#333">{label}</text>'
    return o
def line(x1,y1,x2,y2,color="#555",w=1.5,dash=False):
    d=' stroke-dasharray="5,3"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d}/>'
def node(x,y,t,r=17,fill="#e8f0fe",stroke="#3b6fd4",fs=13,shape="c"):
    if shape=="s": o=f'<rect x="{x-r}" y="{y-r+3}" width="{2*r}" height="{2*r-6}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
    elif shape=="tri_up": o=f'<polygon points="{x},{y-r} {x-r},{y+r-3} {x+r},{y+r-3}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
    elif shape=="tri_dn": o=f'<polygon points="{x},{y+r} {x-r},{y-r+3} {x+r},{y-r+3}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
    else: o=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
    return o+f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="{fs}">{t}</text>'
def text(x,y,t,fs=12,anchor="middle",color="#222",bold=False,italic=False):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{color}"{BW if bold else ""}{IT if italic else ""}>{t}</text>'
def fig(title,body,w,h):
    return f'<figure>{svg(w,h,DEFS+body)}<figcaption>{title}</figcaption></figure>'
