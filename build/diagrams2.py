from svg import *
import diagrams as old
D={k:list(v) for k,v in old.D.items()}
def add(k,f): D.setdefault(k,[]).append(f)

# ---------- generic tree layout ----------
def N(t,c=None,**kw):
    d=dict(t=t,c=c or [],**kw); return d
def draw_tree(root,dx=64,dy=78,pad=34,top=46):
    cnt=[0]
    def lay(n,depth):
        n["y"]=top+depth*dy
        if not n["c"]:
            n["x"]=pad+cnt[0]*dx; cnt[0]+=1
        else:
            for _,ch in n["c"]: lay(ch,depth+1)
            xs=[ch["x"] for _,ch in n["c"]]; n["x"]=sum(xs)/len(xs)
    lay(root,0)
    maxd=[0]
    def md(n,d): maxd[0]=max(maxd[0],d); [md(ch,d+1) for _,ch in n["c"]]
    md(root,0)
    W=pad*2+(cnt[0]-1)*dx; H=top+maxd[0]*dy+top
    edges="";nodes=""
    def rec(n):
        nonlocal edges,nodes
        for e,ch in n["c"]:
            ch["px"]=n["x"]
            cut=ch.get("cut")
            edges+=line(n["x"],n["y"],ch["x"],ch["y"],color="#c9302c" if cut else "#777",w=1.8,dash=bool(cut))
            if e:
                lx=n["x"]+0.62*(ch["x"]-n["x"]); ly=n["y"]+0.62*(ch["y"]-n["y"])
                off=-8 if ch["x"]<n["x"] else 8 if ch["x"]>n["x"] else 8
                edges+=text(lx+off,ly,e,fs=12,color="#333",anchor="end" if off<0 else "start")
            rec(ch)
        t=n["t"]; fill=n.get("fill","#e8f0fe"); st=n.get("stroke","#3b6fd4"); sh=n.get("shape","c")
        if sh=="box":
            w=max(44,len(t)*8+18)
            nodes+=f'<rect x="{n["x"]-w/2}" y="{n["y"]-16}" width="{w}" height="32" rx="8" fill="{fill}" stroke="{st}" stroke-width="1.6"/>'+text(n["x"],n["y"]+5,t,fs=14,bold=n.get("bold",False))
        else:
            nodes+=node(n["x"],n["y"],t,r=19,fill=fill,stroke=st,fs=14,shape=sh)
        if n.get("val") is not None:
            left=n.get("px") is not None and n["px"]>n["x"]
            dxv=(28 if sh!="box" else max(44,len(t)*8+18)/2+8)
            nodes+=text(n["x"]+(-dxv if left else dxv),n["y"]-10,str(n["val"]),fs=15,color="#c9302c",bold=True,anchor="end" if left else "start")
        if n.get("order"):
            px=n.get("px")
            if px is None: nodes+=text(n["x"],n["y"]-26,f'#{n["order"]}',fs=12,color="#c9302c",bold=True)
            else:
                sd=-1 if px>=n["x"] else 1
                nodes+=text(n["x"]+sd*22,n["y"]-18,f'#{n["order"]}',fs=12,color="#c9302c",bold=True,anchor="end" if sd<0 else "start")
        if n.get("sub"): nodes+=text(n["x"]+26,n["y"]+5,n["sub"],fs=12,color="#555",anchor="start")
    rec(root)
    return edges+nodes,W,H+10

def tree_fig(title,root,**kw):
    body,W,H=draw_tree(root,**kw); return fig(title,body,W,H)

# ---------- Q1 ----------
b=box(220,10,240,50,"ENVIRONMENT",fill="#f1f1f1",stroke="#888",fs=16,bold=True)
b+=box(20,140,170,56,"SENSORS",fill="#e0f4e8",stroke="#2a8a55",fs=15,bold=True)+box(255,140,170,56,"AGENT\n(decides)",fill="#ede7f6",stroke="#6a4cc2",fs=15,bold=True)+box(490,140,170,56,"ACTUATORS",fill="#fde9e0",stroke="#c9602a",fs=15,bold=True)
b+=arrow(160,60,110,140,"perceives",lx=-28)+arrow(190,168,255,168,"percept")+arrow(425,168,490,168,"action")+arrow(570,140,520,60,"acts on",lx=30)
D["Q1"]=[fig("Figure 1. Agent–environment loop (sense → decide → act)",b,680,215)]
# ---------- Q2 ----------
def st(x,t,sub,goal=False): return box(x,25,130,60,t+"\n"+sub,fill="#d8efdf" if goal else "#e8f0fe",stroke="#2a8a55" if goal else "#3b6fd4",fs=14)
b=st(10,"(D, D, A)","start: both dirty")+st(190,"(C, D, A)","A cleaned")+st(370,"(C, D, B)","moved right")+st(550,"(C, C, B)","GOAL",True)
b+=arrow(140,55,190,55,"Suck",ly=-8)+arrow(320,55,370,55,"Right",ly=-8)+arrow(500,55,550,55,"Suck",ly=-8)
b+=text(340,115,"State = (Room A, Room B, vacuum position); C = clean, D = dirty. Total 2 × 2 × 2 = 8 states.",fs=13,italic=True)
D["Q2"]=[fig("Figure 2a. Vacuum world: one solution path (step cost 1 each, path cost 3)",b,700,130)]
def grid(x,y,vals):
    o=""
    for i,v in enumerate(vals):
        r,c=divmod(i,3); o+=f'<rect x="{x+c*44}" y="{y+r*44}" width="44" height="44" fill="{"#fff" if v else "#ddd"}" stroke="#333"/>'+(text(x+c*44+22,y+r*44+29,str(v),fs=18,bold=True) if v else "")
    return o
b=grid(40,20,[2,8,3,1,6,4,7,0,5])+grid(300,20,[1,2,3,4,5,6,7,8,0])+arrow(185,86,290,86,"slide tiles")+text(105,172,"Initial state",bold=True,fs=14)+text(365,172,"Goal state",bold=True,fs=14)
D["Q2"].append(fig("Figure 2b. 8-puzzle: actions move the blank Up / Down / Left / Right; 181,440 reachable states",b,440,185))
# 8-queens
b=""
sol=[0,4,7,5,2,6,1,3]
for r in range(8):
    for c in range(8):
        b+=f'<rect x="{20+c*36}" y="{10+r*36}" width="36" height="36" fill="{"#e9d8b4" if (r+c)%2==0 else "#b58863"}"/>'
for c,r in enumerate(sol): b+=text(20+c*36+18,10+r*36+26,"♛",fs=26,color="#111")
D["Q2"].append(fig("Figure 2c. 8-queens: one goal state (no queen attacks another)",b,330,305))

# ---------- Q3 search trees ----------
def bfs_tree(order):
    mk=lambda t:N(t,order=order.index(t)+1)
    A,B,C,Dn,E,F,G=[mk(x) for x in "ABCDEFG"]
    A["c"]=[("",B),("",C)];B["c"]=[("",Dn),("",E)];C["c"]=[("",F),("",G)]
    return A
D["Q3"]=[tree_fig("Figure 3a. Breadth-First Search – visit level by level (FIFO queue): A B C D E F G",bfs_tree(list("ABCDEFG")),dx=80),
         tree_fig("Figure 3b. Depth-First Search – go deep, then backtrack (LIFO stack): A B D E C F G",bfs_tree(list("ABDECFG")),dx=80)]
Gv1=N("G",fill="#fff3cd",sub="f=1+5=6");Gv2=N("G",fill="#fff3cd",sub="f=4+2=6")
A=N("A",[("cost 5",Gv1)],sub="g=1,h=3,f=4");B=N("B",[("cost 2",Gv2)],sub="g=4,h=1,f=5")
S=N("S",[("cost 1",A),("cost 4",B)],sub="h=5")
D["Q3"].append(tree_fig("Figure 3c. A* (f = g + h) expands A (f=4) before B (f=5); Greedy (f = h) would pick B first (h=1)",S,dx=230,dy=90,pad=100))
D["Q3"][-1]=D["Q3"][-1].replace('viewBox="0 0 ','viewBox="0 0 ')
# ---------- Q4 agent chains ----------
def chain(title,items,note=""):
    x=10;b=""
    for i,(t,col) in enumerate(items):
        w=150 if "\n" in t or len(t)>10 else 110
        b+=box(x,20,w,56,t,fill=col[0],stroke=col[1],fs=14)
        if i<len(items)-1: b+=arrow(x+w,48,x+w+34,48)
        x+=w+34
    b+=text((x-34)/2+5,105,note,fs=13,italic=True,color="#444")
    return fig(title,b,x-24,118)
P=("#f1f1f1","#888");R=("#ede7f6","#6a4cc2");S_=("#fff3cd","#c99a00");G_=("#e4f3d6","#5a9a2a");A_=("#e0f4e8","#2a8a55");U=("#fde9e0","#c9602a")
D["Q4"]=[chain("Figure 4a. Simple reflex agent",[("Percept",P),("IF–THEN\nrules",R),("Action",A_)],"uses only the current percept – e.g. thermostat"),
 chain("Figure 4b. Model-based reflex agent",[("Percept",P),("Internal state\n(world model)",S_),("IF–THEN\nrules",R),("Action",A_)],"remembers the world – e.g. robot vacuum with a room map"),
 chain("Figure 4c. Goal-based agent",[("Percept",P),("Internal state\n(world model)",S_),("Search / plan\ntowards GOAL",G_),("Action",A_)],"asks 'which actions reach the goal?' – e.g. GPS navigation"),
 chain("Figure 4d. Utility-based agent",[("Percept",P),("Internal state\n(world model)",S_),("Maximise\nexpected UTILITY",U),("Action",A_)],"picks the best way, not just any way – e.g. ride-booking app")]+[old.D["Q4"][4]]
# ---------- Q5 environment classification tree ----------
root=N("Task environment",[("",N("Observable",[("",N("Fully\n",shape="box")),("",N("Partially",shape="box"))],shape="box",fill="#fff3cd")),
 ("",N("Deterministic?",[("",N("Deterministic",shape="box")),("",N("Stochastic",shape="box"))],shape="box",fill="#fff3cd")),
 ("",N("Episodic?",[("",N("Episodic",shape="box")),("",N("Sequential",shape="box"))],shape="box",fill="#fff3cd")),
 ("",N("Agents",[("",N("Single",shape="box")),("",N("Multi",shape="box"))],shape="box",fill="#fff3cd"))],shape="box",fill="#ede7f6",stroke="#6a4cc2",bold=True)
root["c"][0][1]["c"][0][1]["t"]="Fully"
D["Q5"]=[tree_fig("Figure 5. Four ways to classify a task environment (chess = fully, deterministic, sequential, multi; taxi = partially, stochastic, sequential, multi)",root,dx=112,dy=70,pad=50)]
# ---------- Q9 decision tree ----------
Y=lambda:N("Yes",shape="box",fill="#d8efdf",stroke="#2a8a55");No=lambda:N("No",shape="box",fill="#fde9e0",stroke="#c9602a")
typ=N("Type?",[("French",Y()),("Italian",No()),("Thai",N("Fri/Sat?",[("No",No()),("Yes",Y())],shape="box",fill="#ede7f6",stroke="#6a4cc2")),("Burger",Y())],shape="box",fill="#ede7f6",stroke="#6a4cc2")
hung=N("Hungry?",[("No",No()),("Yes",typ)],shape="box",fill="#ede7f6",stroke="#6a4cc2")
root=N("Patrons?",[("None",No()),("Some",Y()),("Full",hung)],shape="box",fill="#ede7f6",stroke="#6a4cc2",bold=True)
D["Q9"]=[tree_fig("Figure 9. Decision tree for the restaurant problem: 'Will we wait?' (root chosen by highest information gain)",root,dx=100,dy=84,pad=50)]
# ---------- Q11 Apriori flow ----------
def pill(x,y,w,t,fill="#e8f0fe",stroke="#3b6fd4"): return box(x,y,w,64,t,fill=fill,stroke=stroke,fs=13)
b=pill(5,10,150,"C1: all items\nBread 4, Milk 4, Diaper 4\nBeer 3, Coke 2, Eggs 1")+pill(200,10,130,"L1 (support ≥ 3)\nBread, Milk,\nDiaper, Beer",fill="#d8efdf",stroke="#2a8a55")
b+=pill(375,10,170,"C2 → count\nB,M=3  B,D=3  M,D=3\nD,Beer=3  B,Beer=2  M,Beer=2")+pill(590,10,130,"L2\nB,M  B,D\nM,D  D,Beer",fill="#d8efdf",stroke="#2a8a55")
b+=pill(765,10,130,"C3 = {B,M,D}\ncount = 2 < 3\nL3 = empty → stop",fill="#fde9e0",stroke="#c9602a")
for a,c in ((155,200),(330,375),(545,590),(720,765)): b+=arrow(a,42,c,42)
b+=text(450,105,"Apriori: keep only frequent itemsets (support ≥ 60%), build bigger candidates from them, stop when none survive",fs=13,italic=True)
D["Q11"]=[fig("Figure 11. Apriori steps for the worked example (B = Bread, M = Milk, D = Diaper)",b,900,118)]
# ---------- Supplement B trees ----------
def mm():
    def leaf(v): return N(str(v),shape="s",fill="#f1f1f1",stroke="#888")
    def mx(t,val,ch): return N(t,[("",c) for c in ch],shape="tri_up",fill="#fde9e0",stroke="#c9602a",val=val)
    def mn(t,val,ch): return N(t,[("",c) for c in ch],shape="tri_dn",fill="#dbe6fb",stroke="#3b6fd4",val=val)
    d=mx("D",4,[leaf(-1),leaf(4)]);e=mx("E",6,[leaf(2),leaf(6)]);f=mx("F",-3,[leaf(-3),leaf(-5)]);g=mx("G",7,[leaf(0),leaf(7)])
    return mx("A",4,[mn("B",4,[d,e]),mn("C",-3,[f,g])])
D["SB"]=[tree_fig("Figure B1. Minimax: ▲ = MAX picks the larger value, ▼ = MIN picks the smaller; red numbers are backed-up values; root = 4",mm(),dx=70,dy=82,pad=70)]
def ab():
    def leaf(v,cut=False): return N(str(v),shape="s",fill="#fff" if cut else "#f1f1f1",stroke="#c9302c" if cut else "#888",cut=cut)
    def mx(t,val,ch,**k): return N(t,[("",c) for c in ch],shape="tri_up",fill="#fde9e0",stroke="#c9602a",val=val,**k)
    def mn(t,val,ch,**k): return N(t,[("",c) for c in ch],shape="tri_dn",fill="#dbe6fb",stroke="#3b6fd4",val=val,**k)
    d=mx("D",3,[leaf(2),leaf(3)]);e=mx("E",5,[leaf(5),leaf(9,True)],sub="α=5 ≥ β=3")
    f=mx("F",1,[leaf(0),leaf(1)]);g=mx("G","pruned",[leaf(7,True),leaf(5,True)],cut=True)
    return mx("A",3,[mn("B",3,[d,e]),mn("C",1,[f,g],sub="α=3 ≥ β=1")])
D["SB"].append(tree_fig("Figure B2. Alpha-beta pruning: dashed red branches are never examined; the answer (3) is the same as minimax",ab(),dx=70,dy=82,pad=70))
D["Q8"]=D["Q8"][:1]

# ---------- fixes ----------
b=box(120,10,440,50,"ENVIRONMENT",fill="#f1f1f1",stroke="#888",fs=16,bold=True)
b+=box(20,140,170,56,"SENSORS",fill="#e0f4e8",stroke="#2a8a55",fs=15,bold=True)+box(255,140,170,56,"AGENT\n(decides)",fill="#ede7f6",stroke="#6a4cc2",fs=15,bold=True)+box(490,140,170,56,"ACTUATORS",fill="#fde9e0",stroke="#c9602a",fs=15,bold=True)
b+=arrow(160,60,105,140,"percepts in",lx=-40)+arrow(190,168,255,168,"percept",ly=-8)+arrow(425,168,490,168,"action",ly=-8)+arrow(575,140,520,60,"changes it",lx=40)
D["Q1"]=[fig("Figure 1. Agent–environment loop (sense → decide → act → repeat)",b,680,215)]

b=box(40,20,130,48,"Environment",fill="#f1f1f1",stroke="#888")+box(240,20,140,48,"Performance\nelement",fill="#ede7f6",stroke="#6a4cc2")+box(450,20,130,48,"Actuators",fill="#e0f4e8",stroke="#2a8a55")
b+=box(40,140,130,48,"Problem\ngenerator",fill="#fde9e0",stroke="#c9602a")+box(240,140,140,48,"Learning\nelement",fill="#e4f3d6",stroke="#5a9a2a")+box(450,140,130,48,"Critic",fill="#fff3cd",stroke="#c99a00")+box(450,240,130,48,"Performance\nstandard",fill="#f1f1f1",stroke="#888")
b+=arrow(170,44,240,44,"percept",ly=-8)+arrow(380,44,450,44,"action",ly=-8)+arrow(515,68,515,140,"outcome",lx=34)+arrow(515,240,515,188,"compare",lx=34)
b+=arrow(450,164,380,164,"feedback",ly=-8)+arrow(310,140,310,68,"improves",lx=36)+arrow(240,164,170,164,"goals",ly=-8)+arrow(105,140,105,68,"experiments",lx=-46,dash=True)
D["Q4"][4]=fig("Figure 4e. Learning agent: the critic compares outcomes with a standard; the learning element improves the performance element",b,640,300)

steps=[("Step 1  C1 → L1","Counts: Bread 4, Milk 4, Diaper 4, Beer 3, Coke 2 ✗, Eggs 1 ✗\nL1 = {Bread, Milk, Diaper, Beer}"),
("Step 2  C2 → L2","Pairs: B,M = 3   B,D = 3   M,D = 3   D,Beer = 3   B,Beer = 2 ✗   M,Beer = 2 ✗\nL2 = {B,M}, {B,D}, {M,D}, {D,Beer}"),
("Step 3  C3 → L3","Only candidate {B, M, D}: count 2 < 3  →  L3 empty, STOP"),
("Step 4  Rules","Beer → Diaper: confidence 1.00, lift 1.25\nDiaper → Beer: confidence 0.75, lift 1.25")]
b=""
for i,(h,t) in enumerate(steps):
    y=10+i*78
    b+=box(10,y,150,52,h,fill="#ede7f6",stroke="#6a4cc2",fs=14,bold=True)+box(175,y,615,52,t,fill="#d8efdf" if i==3 else "#e8f0fe",stroke="#2a8a55" if i==3 else "#3b6fd4",fs=13)
    if i<3: b+=arrow(85,y+52,85,y+78)
D["Q11"]=[fig("Figure 11. Apriori steps for the worked example (min support = 3 of 5; B = Bread, M = Milk, D = Diaper)",b,800,330)]

b='<rect x="20" y="10" width="320" height="220" fill="#fafafa" stroke="#ccc"/>'
b+=line(70,230,290,10,color="#222",w=2.4)+line(28,230,248,10,color="#888",dash=True)+line(112,230,332,10,color="#888",dash=True)
for x,y in ((60,100),(90,60),(140,40),(50,170),(80,140)): b+=f'<circle cx="{x}" cy="{y}" r="7" fill="#3b6fd4"/>'
for x,y in ((130,128),(190,68)): b+=f'<circle cx="{x}" cy="{y}" r="7" fill="#3b6fd4"/><circle cx="{x}" cy="{y}" r="12" fill="none" stroke="#2a7a3a" stroke-width="2.2"/>'
for x,y in ((260,180),(300,120),(220,210),(310,200),(290,60)): b+=f'<rect x="{x-7}" y="{y-7}" width="14" height="14" fill="#c9602a"/>'
for x,y in ((170,172),(230,112)): b+=f'<rect x="{x-7}" y="{y-7}" width="14" height="14" fill="#c9602a"/><circle cx="{x}" cy="{y}" r="13" fill="none" stroke="#2a7a3a" stroke-width="2.2"/>'
b+=f'<line x1="150" y1="108" x2="180" y2="138" stroke="#2a7a3a" stroke-width="1.6" marker-end="url(#a)"/><line x1="180" y1="138" x2="150" y2="108" stroke="#2a7a3a" stroke-width="1.6" marker-end="url(#a)"/>'
b+=text(360,40,"● Class +1",anchor="start",color="#3b6fd4",bold=True,fs=13)+text(360,62,"■ Class −1",anchor="start",color="#c9602a",bold=True,fs=13)
b+=text(360,96,"—— hyperplane w·x + b = 0",anchor="start",fs=12)+text(360,118,"- - - margins w·x + b = ±1",anchor="start",fs=12)+text(360,140,"◯ support vectors",anchor="start",fs=12,color="#2a7a3a")+text(360,162,"↔ margin width = 2 / ‖w‖",anchor="start",fs=12,color="#2a7a3a")
D["Q13"]=[fig("Figure 13. SVM: the widest 'street' between the two classes; only the support vectors fix its position",b,560,240)]

DB='<defs><marker id="s" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8,0 L0,4 L8,8 z" fill="#444"/></marker></defs>'
def both(x1,y1,x2,y2,l): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444" stroke-width="1.6" marker-start="url(#s)" marker-end="url(#a)"/>'+text(x1+0.3*(x2-x1),y1+0.3*(y2-y1)-8,l,fs=12)
b=DB+box(20,62,150,56,"Interrogator\n(human judge)",fill="#fff3cd",stroke="#c99a00",fs=14)+box(400,10,140,48,"Human",fill="#e0f4e8",stroke="#2a8a55",fs=14)+box(400,122,140,48,"Computer",fill="#fde9e0",stroke="#c9602a",fs=14)
b+=f'<line x1="310" y1="0" x2="310" y2="180" stroke="#999" stroke-width="3" stroke-dasharray="8,5"/>'+text(310,198,"hidden from judge",fs=12,color="#777")
b+=both(170,80,400,34,"typed chat")+both(170,100,400,146,"typed chat")
b+=text(280,222,"The machine passes if the judge cannot tell which one is the computer",fs=13,italic=True)
D["Q14"][1]=fig("Figure 14b. The Turing Test",b,560,232)

b=box(10,40,100,50,"Crisp\ninput",fill="#f1f1f1",stroke="#888",fs=14)+box(160,40,130,50,"1. Fuzzi-\nfication",fill="#e8f0fe",fs=14)+box(340,40,130,50,"3. Inference\nengine",fill="#ede7f6",stroke="#6a4cc2",fs=14)+box(520,40,130,50,"4. Defuzzi-\nfication",fill="#e8f0fe",fs=14)+box(700,40,100,50,"Crisp\noutput",fill="#f1f1f1",stroke="#888",fs=14)
b+=arrow(110,65,160,65)+arrow(290,65,340,65)+arrow(470,65,520,65)+arrow(650,65,700,65)
b+=text(315,30,"fuzzy",fs=11)+text(495,30,"fuzzy",fs=11)
b+=box(275,140,260,56,"2. Knowledge base\nmembership functions + IF–THEN rules",fill="#fff3cd",stroke="#c99a00",fs=13)+arrow(405,140,405,90)
b+=text(135,30,"e.g. 28 °C",fs=11,color="#555")+text(675,30,"e.g. fan 55 %",fs=11,color="#555")
D["Q15"][0]=fig("Figure 15a. Fuzzy logic system: fuzzify → apply rules → defuzzify",b,810,210)

b='<rect x="40" y="10" width="420" height="130" fill="#fafafa" stroke="#ccc"/>'
X=lambda v:40+v*420/45
Y=lambda m:140-m*120
def poly(pts,c,n,lx):
    return f'<polygon points="{" ".join(f"{X(a):.1f},{Y(m):.1f}" for a,m in pts)}" fill="{c}" fill-opacity=".22" stroke="{c}" stroke-width="2.2"/>'+text(X(lx),Y(1)-0+(-4),n,bold=True,color=c,fs=13)
b+=poly([(0,0),(0,1),(10,1),(20,0)],"#3b6fd4","Cold",5)+poly([(12,0),(22,1),(42,0)],"#c99a00","Warm",22)+poly([(25.5,0),(38,1),(45,1),(45,0)],"#c9302c","Hot",41.5)
x=28
b+=f'<line x1="{X(x)}" y1="10" x2="{X(x)}" y2="140" stroke="#222" stroke-dasharray="4,3"/>'
for m,c in ((0.7,"#c99a00"),(0.03,"#c9302c")): pass
b+=f'<circle cx="{X(x)}" cy="{Y(0.7)}" r="4" fill="#c99a00"/>'+text(X(x)-6,Y(0.7)-4,"Warm 0.7",fs=12,anchor="end",bold=True,color="#8a6d00")+f'<circle cx="{X(x)}" cy="{Y(0.2)}" r="4" fill="#c9302c"/>'+text(X(x)+6,Y(0.2)+4,"Hot 0.2",fs=12,anchor="start",bold=True,color="#c9302c")
for v in (0,10,20,30,40): b+=text(X(v),156,f"{v}",fs=11,color="#555")
b+=text(250,174,"temperature (°C)",fs=12)+text(32,20,"1",fs=11,anchor="end")+text(32,140,"0",fs=11,anchor="end")+text(18,80,"μ",fs=13,anchor="end")
D["Q15"][1]=fig("Figure 15b. Membership functions: 28 °C is Warm to degree 0.7 and Hot to degree 0.2",b,480,182)

b=""
for y,t in ((30,"x₁"),(80,"x₂"),(130,"x₃")): b+=node(40,y,t)+arrow(58,y,184,80)+text(110,y+(-6 if y<80 else 14 if y>80 else -6),t.replace("x","w"),fs=12,color="#3b6fd4",bold=True)
b+=node(210,80,"Σ",r=26,fill="#fff3cd")+box(270,58,110,44,"activation\ng(Σ w·x + b)",fill="#ede7f6",stroke="#6a4cc2",fs=12)+arrow(236,80,270,80)+arrow(380,80,440,80)+text(450,85,"ŷ",fs=15,anchor="start",bold=True)
D["Q7"][1]=fig("Figure 7b. A single neuron (perceptron): weighted sum, then activation",b,470,160)

# ---------- IDDFS: three iterations ----------
def idtree(limit):
    order={0:["A"],1:["A","B","C"],2:list("ABDECFG")}[limit]
    def mk(t,d):
        on=t in order
        return N(t,fill="#e8f0fe" if on else "#f4f4f4",stroke="#3b6fd4" if on else "#bbb")
    A=mk("A",0);B=mk("B",1);C=mk("C",1);Dn=mk("D",2);E_=mk("E",2);F=mk("F",2);G=mk("G",2)
    A["c"]=[("",B),("",C)];B["c"]=[("",Dn),("",E_)];C["c"]=[("",F),("",G)]
    body,W,H=draw_tree(A,dx=50,dy=70,pad=30)
    return body,W,H
parts=[idtree(l) for l in (0,1,2)]
b="";x=0
for l,(body,W,H) in enumerate(parts):
    b+=f'<g transform="translate({x},28)">{body}</g>'+text(x+W/2,18,f"Limit = {l}",bold=True,fs=14,color="#6a4cc2")
    if l<2: b+=f'<line x1="{x+W+8}" y1="30" x2="{x+W+8}" y2="{H+20}" stroke="#ddd" stroke-width="2"/>'
    x+=W+16
idd=fig("Figure 3c. Iterative deepening: DFS is repeated with limit 0, 1, 2 …; blue = visited in that round (numbers = visit order), grey = not reached yet",b,x,parts[0][2]+40)
# ---------- Greedy best-first tree ----------
GR="#d8efdf";GS="#2a8a55"
g=N("G",fill="#fff3cd",stroke="#c99a00",sub="h=0 GOAL",order=4)
F=N("F",[("",g)],fill=GR,stroke=GS,sub="h=1",order=3);E_=N("E",sub="h=3")
B=N("B",[("",E_),("",F)],fill=GR,stroke=GS,sub="h=2",order=2);C=N("C",sub="h=3");A=N("A",[("",C)],sub="h=4")
S=N("S",[("",A),("",B)],fill=GR,stroke=GS,sub="h=6",order=1)
body,W,H=draw_tree(S,dx=110,dy=80,pad=60)
greedy=fig("Figure 3d. Greedy best-first: always expand the child with the smallest h → path S → B → F → G (green). Fast, but not guaranteed optimal",body,W+40,H)
D["Q3"]=[D["Q3"][0],D["Q3"][1],D["Q3"][2].replace("Figure 3c.","Figure 3e."),idd,greedy]

# ===== notes-based figures =====
# Figure 1: interaction flow as in notes
b=box(10,30,120,60,"Environment\n(signals)",fill="#f1f1f1",stroke="#888",fs=14)+box(165,30,120,60,"Sensors\n(percepts)",fill="#e0f4e8",stroke="#2a8a55",fs=14)
b+=box(320,14,170,92,"AGENT\nagent program\non architecture\n→ agent function",fill="#ede7f6",stroke="#6a4cc2",fs=13)
b+=box(525,30,120,60,"Actuators\n(actions)",fill="#fde9e0",stroke="#c9602a",fs=14)+box(680,30,120,60,"Effects on\nenvironment",fill="#fff3cd",stroke="#c99a00",fs=14)
b+=arrow(130,60,165,60)+arrow(285,60,320,60)+arrow(490,60,525,60)+arrow(645,60,680,60)
b+=f'<path d="M740,90 L740,140 L70,140 L70,92" fill="none" stroke="#444" stroke-width="1.6" marker-end="url(#a)"/>'+text(405,158,"the cycle repeats",fs=13,italic=True,color="#555")
D["Q1"]=[fig("Figure 1. Agent–environment interaction flow",b,810,170)]

# Figure 2a: full vacuum state space
def vac(x,y):
    return f'<rect x="{x-11}" y="{y-7}" width="22" height="13" rx="4" fill="#1a3f8f"/><line x1="{x+9}" y1="{y-6}" x2="{x+16}" y2="{y-20}" stroke="#1a3f8f" stroke-width="2.5"/><circle cx="{x-6}" cy="{y+8}" r="3" fill="#1a3f8f"/><circle cx="{x+6}" cy="{y+8}" r="3" fill="#1a3f8f"/>'
def dirt(x,y):
    return "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="2.6" fill="#8a5a1a"/>' for dx,dy in ((-8,0),(0,-4),(8,0),(-4,5),(4,5),(0,1)))
W_=60;H_=48
def vroom(x,y,a,b_,p):
    o=f'<rect x="{x}" y="{y}" width="{W_}" height="{H_}" fill="#fff" stroke="#1a3f8f" stroke-width="2"/><rect x="{x+W_}" y="{y}" width="{W_}" height="{H_}" fill="#fff" stroke="#1a3f8f" stroke-width="2"/>'
    if a: o+=dirt(x+30,y+34)
    if b_: o+=dirt(x+W_+30,y+34)
    o+=vac(x+(22 if p=="A" else W_+22),y+16)
    lab="("+("D" if a else "C")+", "+("D" if b_ else "C")+", "+p+")"
    return o, lab
P={"DDA":(265,30),"DDB":(495,30),"CDA":(50,190),"CDB":(260,190),"DCA":(500,190),"DCB":(710,190),"CCA":(265,360),"CCB":(495,360)}
b=""
for k,(x,y) in P.items():
    o,lab=vroom(x,y,k[0]=="D",k[1]=="D",k[2]); b+=o
    goal=k.startswith("CC")
    b+=text(x+60,y-8,lab+("  GOAL" if goal else ""),fs=13,bold=goal,color="#2a7a3a" if goal else "#333")
def lr(a,c):
    (xa,ya),(xc,yc)=P[a],P[c]
    return arrow(xa+120,ya+16,xc,yc+16,"R",ly=-5)+arrow(xc,ya+34,xa+120,ya+34,"L",ly=14)
b+=lr("DDA","DDB")+lr("CDA","CDB")+lr("DCA","DCB")+lr("CCA","CCB")
def S_(a,c,lx):
    (xa,ya),(xc,yc)=P[a],P[c]
    return arrow(xa+60,ya+48,xc+60,yc-22,"S",lx=lx)
b+=S_("DDA","CDA",-12)+S_("DDB","DCB",12)+S_("CDB","CCB",22)+S_("DCA","CCA",-22)
def loop(k,side,lab):
    x,y=P[k]
    if side=="L": d=f'M{x},{y+14} C{x-34},{y+2} {x-34},{y+46} {x},{y+36}'; t=text(x-36,y+28,lab,fs=12,anchor="end")
    elif side=="R": d=f'M{x+120},{y+14} C{x+154},{y+2} {x+154},{y+46} {x+120},{y+36}'; t=text(x+156,y+28,lab,fs=12,anchor="start")
    else:
        cx=x+(30 if side=="BA" else 90); d=f'M{cx-10},{y+48} C{cx-26},{y+80} {cx+26},{y+80} {cx+10},{y+48}'; t=text(cx,y+90,lab,fs=12)
    return f'<path d="{d}" fill="none" stroke="#444" stroke-width="1.5" marker-end="url(#a)"/>'+t
b+=loop("DDA","L","L")+loop("DDB","R","R")+loop("CDA","L","L")+loop("CDA","BA","S")+loop("CDB","R","R")+loop("DCA","L","L")+loop("DCB","R","R")+loop("DCB","BB","S")
b+=loop("CCA","L","L")+loop("CCA","BA","S")+loop("CCB","R","R")+loop("CCB","BB","S")
full=fig("Figure 2a. State space of the vacuum cleaner world: 8 states; L = Left, R = Right, S = Suck; loops = action has no effect",b,880,460)
D["Q2"]=[full,D["Q2"][0].replace("Figure 2a.","Figure 2b."),D["Q2"][1].replace("Figure 2b.","Figure 2c."),D["Q2"][2].replace("Figure 2c.","Figure 2d.")]

# A* graph (notes example)
Pg={"S":(60,185),"A":(200,105),"B":(350,55),"C":(350,185),"D":(500,105),"G":(500,265)}
hv={"S":5,"A":3,"B":4,"C":2,"D":6,"G":0}
E_=[("S","A",1),("S","G",10),("A","B",2),("A","C",1),("B","D",5),("C","D",3),("C","G",4)]
path={("S","A"),("A","C"),("C","G")}
b=""
for a,c,w in E_:
    on=(a,c) in path
    b+=line(*Pg[a],*Pg[c],color="#2a8a55" if on else "#999",w=3.2 if on else 1.6)
    mx=(Pg[a][0]+Pg[c][0])/2; my=(Pg[a][1]+Pg[c][1])/2
    b+=f'<circle cx="{mx}" cy="{my}" r="11" fill="#fff" stroke="#ccc"/>'+text(mx,my+5,str(w),fs=13,bold=True)
for n,(x,y) in Pg.items():
    b+=node(x,y,n,r=20,fs=15,fill="#fff3cd" if n=="G" else ("#d8efdf" if n in "SAC" else "#e8f0fe"),stroke="#c99a00" if n=="G" else ("#2a8a55" if n in "SAC" else "#3b6fd4"))
    b+=text(x,y-27,f"h={hv[n]}",fs=12,color="#6a4cc2",bold=True)
b+=text(290,315,"Edge numbers = step cost g; purple = heuristic h; green = path found by A* (cost 6)",fs=12,italic=True)
astar_graph=fig("Figure 3e. A* example graph (S = start, G = goal)",b,580,325)
# A* search tree with f values
G1=N("G",fill="#f4f4f4",stroke="#bbb",sub="f=10+0=10")
B_=N("B",sub="f=3+4=7",fill="#f4f4f4",stroke="#bbb");D_=N("D",sub="f=5+6=11",fill="#f4f4f4",stroke="#bbb")
G2=N("G",fill="#fff3cd",stroke="#c99a00",sub="f=6+0=6 GOAL")
C_=N("C",[("3",D_),("4",G2)],fill="#d8efdf",stroke="#2a8a55",sub="f=2+2=4")
A_=N("A",[("2",B_),("1",C_)],fill="#d8efdf",stroke="#2a8a55",sub="f=1+3=4")
S_n=N("S",[("1",A_),("10",G1)],fill="#d8efdf",stroke="#2a8a55",sub="f=0+5=5")
body,W,H=draw_tree(S_n,dx=130,dy=85,pad=70)
astar_tree=fig("Figure 3f. A* search tree: at each step expand the node with the smallest f; green path S → A → C → G (f = 6)",body,W+60,H)
D["Q3"][2]=astar_graph
D["Q3"].append(astar_tree)
D["Q3"]=[D["Q3"][0].replace("Figure 3a. Breadth-First Search – visit level by level (FIFO queue): A B C D E F G","Figure 3a. BFS – level by level: A, B, C, D, E, F, G (numbers = visit order)"),
         D["Q3"][1].replace("Figure 3b. Depth-First Search – go deep, then backtrack (LIFO stack): A B D E C F G","Figure 3b. DFS – go deep, then backtrack: A, B, D, E, C, F, G (numbers = visit order)"),
         D["Q3"][2].replace("Figure 3e. A* example graph (S = start, G = goal)","Figure 3e. A* example graph: numbers on lines = cost, h = heuristic, green = path found").replace(">Edge numbers = step cost g; purple = heuristic h; green = path found by A* (cost 6)<","><"),
         D["Q3"][3].replace("Figure 3c. Iterative deepening: DFS is repeated with limit 0, 1, 2 …; blue = visited in that round (numbers = visit order), grey = not reached yet","Figure 3c. IDS – DFS with limit 0, then 1, then 2 (blue = visited, grey = not yet)"),
         D["Q3"][4].replace("Figure 3d. Greedy best-first: always expand the child with the smallest h → path S → B → F → G (green). Fast, but not guaranteed optimal","Figure 3d. Greedy – always go to the smallest h: S → B → F → G")]
