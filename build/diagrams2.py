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
            cut=ch.get("cut")
            edges+=line(n["x"],n["y"],ch["x"],ch["y"],color="#c9302c" if cut else "#777",w=1.8,dash=bool(cut))
            if e: edges+=text((n["x"]+ch["x"])/2+(-10 if ch["x"]<n["x"] else 10 if ch["x"]>n["x"] else 12),(n["y"]+ch["y"])/2,e,fs=12,color="#333",anchor="middle")
            rec(ch)
        t=n["t"]; fill=n.get("fill","#e8f0fe"); st=n.get("stroke","#3b6fd4"); sh=n.get("shape","c")
        if sh=="box":
            w=max(44,len(t)*8+18)
            nodes+=f'<rect x="{n["x"]-w/2}" y="{n["y"]-16}" width="{w}" height="32" rx="8" fill="{fill}" stroke="{st}" stroke-width="1.6"/>'+text(n["x"],n["y"]+5,t,fs=14,bold=n.get("bold",False))
        else:
            nodes+=node(n["x"],n["y"],t,r=19,fill=fill,stroke=st,fs=14,shape=sh)
        if n.get("val") is not None: nodes+=text(n["x"]+(24 if sh!="box" else max(44,len(t)*8+18)/2+8),n["y"]-14,str(n["val"]),fs=14,color="#c9302c",bold=True,anchor="start")
        if n.get("order"): nodes+=text(n["x"],n["y"]-26,f'#{n["order"]}',fs=12,color="#c9302c",bold=True)
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
D["SB"]=[tree_fig("Figure B1. Minimax: ▲ = MAX picks the larger value, ▼ = MIN picks the smaller; red numbers are backed-up values; root = 4",mm(),dx=70,dy=82,pad=50)]
def ab():
    def leaf(v,cut=False): return N(str(v),shape="s",fill="#fff" if cut else "#f1f1f1",stroke="#c9302c" if cut else "#888",cut=cut)
    def mx(t,val,ch,**k): return N(t,[("",c) for c in ch],shape="tri_up",fill="#fde9e0",stroke="#c9602a",val=val,**k)
    def mn(t,val,ch,**k): return N(t,[("",c) for c in ch],shape="tri_dn",fill="#dbe6fb",stroke="#3b6fd4",val=val,**k)
    d=mx("D",3,[leaf(2),leaf(3)]);e=mx("E",5,[leaf(5),leaf(9,True)],sub="α=5≥β=3: prune 9")
    f=mx("F",1,[leaf(0),leaf(1)]);g=mx("G","✂ pruned",[leaf(7,True),leaf(5,True)],cut=True)
    return mx("A",3,[mn("B",3,[d,e]),mn("C",1,[f,g],sub="α=3≥β=1: prune G")])
D["SB"].append(tree_fig("Figure B2. Alpha-beta pruning: dashed red branches are never examined; the answer (3) is the same as minimax",ab(),dx=70,dy=82,pad=50))
D["Q8"]=D["Q8"][:1]
