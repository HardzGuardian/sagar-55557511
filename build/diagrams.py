from svg import *
D={}
def add(k,f): D.setdefault(k,[]).append(f)

# Q1 agent-environment loop
b=box(250,40,170,60,"AGENT\nagent function f: P* → A",fill="#ede7f6",stroke="#6a4cc2",bold=True)
b+=box(30,50,120,40,"Sensors",fill="#e0f4e8",stroke="#2a8a55")+box(520,50,120,40,"Actuators",fill="#fde9e0",stroke="#c9602a")
b+=arrow(150,70,250,70,"percepts")+arrow(420,70,520,70,"actions")
b+=f'<rect x="10" y="20" width="650" height="170" rx="12" fill="none" stroke="#888" stroke-dasharray="6,4"/>'+text(335,38,"ENVIRONMENT",bold=True,color="#555")
b+=arrow(90,170,90,90,"signals",lx=-26)+arrow(580,90,580,170,"effects on environment",lx=-70,ly=30)
b+=line(90,170,580,170,dash=True)+text(335,160,"cycle repeats",italic=True,color="#555")
add("Q1",fig("Figure 1. Agent–environment interaction loop",b,670,200))

# Q2 vacuum world (8 states)
S={"DDA":(150,25),"DDB":(430,25),"CDA":(20,120),"CDB":(210,120),"DCA":(370,120),"DCB":(560,120),"CCA":(150,215),"CCB":(430,215)}
desc={"DDA":"both dirty, vac in A","DDB":"both dirty, vac in B","CDA":"A clean, B dirty, vac A","CDB":"A clean, B dirty, vac B","DCA":"A dirty, B clean, vac A","DCB":"A dirty, B clean, vac B","CCA":"GOAL – both clean","CCB":"GOAL – both clean"}
b=""
for k,(x,y) in S.items():
    goal=k.startswith("CC")
    t="("+",".join(k)+")"
    b+=box(x,y,120,46,t+"\n"+desc[k],fill="#d8efdf" if goal else "#e8f0fe",stroke="#2a8a55" if goal else "#3b6fd4",fs=11,bold=False)
def mid(k): x,y=S[k]; return x+60,y+23
# horizontal bidirectional pairs
def pair(a,c,y):
    xa,ya=S[a]; xc,yc=S[c]
    return arrow(xa+120,ya+14,xc,yc+14,"R",ly=-4)+arrow(xc,yc+32,xa+120,ya+32,"L",ly=12)
b+=pair("DDA","DDB",0)+pair("CDA","CDB",0)+pair("DCA","DCB",0)+pair("CCA","CCB",0)
b+=arrow(180,71,110,120,"Suck",lx=-16)+arrow(490,71,600,120,"Suck",lx=16)
b+=arrow(290,166,450,215,"Suck",lx=-30,ly=-2)+arrow(410,166,250,215,"Suck",lx=30,ly=-2)
add("Q2",fig("Figure 2. Vacuum-world state space: 8 states; actions Left (L), Right (R), Suck; self-loops omitted",b,700,275))

# Q3 trees for BFS / DFS
def tree7(order,title,labels):
    pos={"A":(210,30),"B":(110,100),"C":(310,100),"D":(60,170),"E":(160,170),"F":(260,170),"G":(360,170)}
    o=""
    for p,c in (("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G")): o+=line(*pos[p],*pos[c])
    for n,(x,y) in pos.items(): o+=node(x,y,n)+text(x+22,y-12,f"{order.index(n)+1}",fs=11,color="#c9302c",bold=True)
    o+=text(210,215,labels,fs=12,italic=True)
    return fig(title,o,420,230)
add("Q3",tree7(list("ABCDEFG"),"Figure 3a. BFS expands level by level (FIFO queue): A, B, C, D, E, F, G","Level 1 → Level 2 → Level 3"))
add("Q3",tree7(list("ABDECFG"),"Figure 3b. DFS goes deep first and backtracks (LIFO stack): A, B, D, E, C, F, G","numbers = order of visit"))
# A* / greedy weighted graph
b=""
P={"S":(60,100),"A":(190,40),"B":(190,160),"G":(340,100)}
for a,c,w in (("S","A",1),("S","B",4),("A","G",5),("B","G",2)):
    b+=line(*P[a],*P[c])+text((P[a][0]+P[c][0])/2+(-8 if a=="S" and c=="A" else 8),(P[a][1]+P[c][1])/2-4,f"cost {w}",fs=11,color="#444")
for n,(x,y) in P.items(): b+=node(x,y,n,fill="#fff3cd" if n=="G" else "#e8f0fe")
for n,h in (("S",5),("A",3),("B",1),("G",0)): b+=text(P[n][0],P[n][1]-24 if n!="B" else P[n][1]+36,f"h={h}",fs=11,color="#2a7a3a",bold=True)
b+=text(210,205,"A*: f(A)=1+3=4, f(B)=4+1=5 → expand A, then B; optimal cost 6",fs=11,italic=True)
add("Q3",fig("Figure 3c. Example graph for A* (f = g + h) and greedy search (f = h)",b,430,215))

# Q4 agent architectures
def blk(items,arrows,w=720,h=110,title=""):
    o=""
    for it in items: o+=box(*it)
    for a in arrows: o+=arrow(*a)
    return o
b=box(10,20,120,44,"Environment\nsends percept",fill="#f1f1f1",stroke="#888")+box(190,15,170,54,"Condition–action rules\nIF dirt THEN suck",fill="#ede7f6",stroke="#6a4cc2")+box(420,20,110,44,"Actuators",fill="#e0f4e8",stroke="#2a8a55")
b+=arrow(130,42,190,42,"percept",ly=-6)+arrow(360,42,420,42,"action",ly=-6)+text(270,100,"No internal state – reacts only to the current percept (thermostat, smoke alarm)",fs=11,italic=True)
add("Q4",fig("Figure 4a. Simple reflex agent",b,560,115))
b=box(10,20,110,44,"Environment\n(partial view)",fill="#f1f1f1",stroke="#888")+box(170,10,150,66,"Internal state\nworld model:\nhow world evolves",fill="#fff3cd",stroke="#c99a00")+box(370,20,130,44,"Condition–\naction rules",fill="#ede7f6",stroke="#6a4cc2")+box(550,20,100,44,"Actuators",fill="#e0f4e8",stroke="#2a8a55")
b+=arrow(120,42,170,42,"percept",ly=-6)+arrow(320,42,370,42,"state",ly=-6)+arrow(500,42,550,42,"action",ly=-6)
b+=f'<path d="M600,64 L600,100 L245,100 L245,76" fill="none" stroke="#2a8a55" stroke-dasharray="5,3" stroke-width="1.5" marker-end="url(#a)"/>'+text(420,95,"action updates internal state",fs=11,color="#2a8a55")
add("Q4",fig("Figure 4b. Model-based reflex agent",b,670,115))
b=box(230,5,110,34,"Goal",fill="#e0f4e8",stroke="#2a8a55")+box(10,60,110,44,"Environment",fill="#f1f1f1",stroke="#888")+box(160,60,120,44,"Internal state\n(world model)",fill="#fff3cd",stroke="#c99a00")+box(330,52,150,60,"Search & planning\nwhat sequence\nreaches the goal?",fill="#e4f3d6",stroke="#5a9a2a")+box(530,60,110,44,"Actuators",fill="#e0f4e8",stroke="#2a8a55")
b+=arrow(120,82,160,82)+arrow(280,82,330,82)+arrow(480,82,530,82,"action",ly=-6)+arrow(335,39,380,52,"desired state",dash=True,lx=-40,ly=-2)
add("Q4",fig("Figure 4c. Goal-based agent",b,660,125))
b=box(160,5,140,40,"Utility function\nscores each outcome",fill="#fde9e0",stroke="#c9602a")+box(10,75,110,44,"Environment",fill="#f1f1f1",stroke="#888")+box(150,75,120,44,"Internal state",fill="#fff3cd",stroke="#c99a00")+box(320,65,170,64,"Search & planning\nevaluates options\nvia utility (max EU)",fill="#e4f3d6",stroke="#5a9a2a")+box(540,75,110,44,"Actuators",fill="#e0f4e8",stroke="#2a8a55")
b+=arrow(120,97,150,97)+arrow(270,97,320,97)+arrow(490,97,540,97,"best action",ly=-6)+arrow(280,45,380,65,"max utility",dash=True,lx=-25)
add("Q4",fig("Figure 4d. Utility-based agent",b,660,140))
b=box(470,5,150,32,"Performance standard",fill="#f1f1f1",stroke="#888")+box(10,70,110,44,"Environment",fill="#f1f1f1",stroke="#888")+box(160,70,140,44,"Performance\nelement",fill="#ede7f6",stroke="#6a4cc2")+box(350,70,110,44,"Actuators",fill="#e0f4e8",stroke="#2a8a55")
b+=box(160,150,140,44,"Learning element",fill="#e4f3d6",stroke="#5a9a2a")+box(480,150,130,44,"Critic",fill="#fff3cd",stroke="#c99a00")+box(10,150,110,44,"Problem\ngenerator",fill="#fde9e0",stroke="#c9602a")
b+=arrow(120,92,160,92)+arrow(300,92,350,92)+arrow(545,37,545,150,"standard",dash=True,lx=30)+arrow(480,172,300,172,"feedback",ly=-6)+arrow(230,150,230,114,"changes",lx=28)+arrow(120,172,160,172)+arrow(65,150,65,114,"explore",lx=-28,dash=True)
add("Q4",fig("Figure 4e. Learning agent (performance element, critic, learning element, problem generator)",b,640,205))

# Q6 ML hierarchy
b=box(190,10,180,36,"Machine Learning",fill="#2a8a55",stroke="#1c6b40",bold=True).replace('<text','<text fill="#fff"')
for x,t in ((20,"Supervised\nLearning"),(210,"Unsupervised\nLearning"),(400,"Reinforcement\nLearning")): b+=box(x,85,140,44,t,fill="#d8efdf",stroke="#2a8a55",bold=True)+line(280,46,x+70,85)
for i,t in enumerate(("Classification","Regression")): b+=text(30,155+i*18,"→ "+t,fs=12,anchor="start")
for i,t in enumerate(("Clustering","Dimension reduction","Association rules")): b+=text(220,155+i*18,"→ "+t,fs=12,anchor="start")
for i,t in enumerate(("Q-learning","SARSA","Deep Q-learning")): b+=text(410,155+i*18,"→ "+t,fs=12,anchor="start")
b+=text(280,215,"Semi-supervised and self-supervised learning combine labelled and unlabelled data",fs=11,italic=True,color="#555")
add("Q6",fig("Figure 6a. Types of machine learning",b,560,225))
b=box(230,10,100,40,"Agent",fill="#ede7f6",stroke="#6a4cc2",bold=True)+box(440,85,100,40,"Action",fill="#fff3cd",stroke="#c99a00")+box(230,150,100,40,"Environment",fill="#f1f1f1",stroke="#888")+box(20,85,100,40,"Reward\n+ state",fill="#e0f4e8",stroke="#2a8a55")
b+=arrow(330,30,490,85)+arrow(490,125,330,170)+arrow(230,170,70,125)+arrow(70,85,230,30)
add("Q6",fig("Figure 6b. Reinforcement-learning loop: action → environment → reward and new state → agent",b,560,200))

# Q7 MLP
b=""; L=[(60,[60,120,180]),(220,[40,100,140,200]),(380,[80,160])]
for x,ys in L:
    pass
for (x1,y1s),(x2,y2s) in zip(L,L[1:]):
    for a in y1s:
        for c in y2s: b+=line(x1,a,x2,c,color="#bbb",w=1)
for x,ys in L:
    for i,y in enumerate(ys): b+=node(x,y,"",r=14,fill=("#e0f4e8","#fff3cd","#fde9e0")[L.index((x,ys))])
for y,t in zip(L[0][1],("x₁","x₂","x₃")): b+=text(60,y+4,t,fs=12)
for y,t in zip(L[2][1],("ŷ₁","ŷ₂")): b+=text(380,y+4,t,fs=12)
b+=text(60,240,"Input layer",bold=True)+text(220,240,"Hidden layer",bold=True)+text(380,240,"Output layer",bold=True)
b+=arrow(430,120,540,120,"forward pass →",ly=-8)+arrow(540,150,430,150,"← error back-propagated",ly=14,color="#c9302c")
add("Q7",fig("Figure 7. Multi-layer feed-forward network trained by back-propagation",b,560,255))
# perceptron
b=""
for y,t in ((30,"x₁"),(80,"x₂"),(130,"x₃")): b+=node(40,y,t)+arrow(58,y,185,80,f"w{t[-1]}",ly=-2)
b+=node(210,80,"Σ",r=26,fill="#fff3cd")+box(270,60,90,40,"g(Σ w·x + b)\nactivation",fill="#ede7f6",stroke="#6a4cc2",fs=11)+arrow(236,80,270,80)+arrow(360,80,420,80,"ŷ")
add("Q7",fig("Figure 7b. A single neuron / perceptron: weighted sum, then activation function",b,470,160))

# Q8 HMM
b=""
for i,x in enumerate((70,200,330)):
    b+=node(x,40,f"X{i+1}",r=22,fill="#fff3cd",shape="c")+node(x,140,f"E{i+1}",r=22,fill="#e8f0fe",shape="s")+arrow(x,62,x,118,"b",lx=12)
    if i<2: b+=arrow(x+22,40,x+108,40,"a")
b+=text(420,45,"hidden states",anchor="start",bold=True,color="#8a6d00")+text(420,145,"observations",anchor="start",bold=True,color="#3b6fd4")
b+=text(235,195,"Transitions A = P(X_t | X_t−1), emissions B = P(E_t | X_t), initial π",fs=12,italic=True)
add("Q8",fig("Figure 8. Hidden Markov model: hidden state chain emitting visible observations",b,560,205))
# trellis with example
b=text(60,22,"t=1",bold=True)+text(210,22,"t=2",bold=True)+text(360,22,"t=3",bold=True)
for t,x in enumerate((60,210,360)):
    b+=node(x,70,"Rainy",r=26,fill="#dbe6fb")+node(x,150,"Sunny",r=26,fill="#fff3cd")
    if t<2:
        for y1 in (70,150):
            for y2 in (70,150): b+=line(x+26,y1,x+124,y2,color="#aaa",w=1)
add("Q8",fig("Figure 8b. Trellis: every state at time t connects to every state at t+1 (used by Forward and Viterbi)",b,440,195))

# Q9 decision tree restaurant
b=box(190,5,120,34,"Patrons?",fill="#ede7f6",stroke="#6a4cc2",bold=True)
b+=box(40,100,90,32,"No",fill="#fde9e0",stroke="#c9602a",bold=True)+box(210,100,80,32,"Yes",fill="#d8efdf",stroke="#2a8a55",bold=True)+box(350,70,110,34,"Hungry?",fill="#ede7f6",stroke="#6a4cc2",bold=True)
b+=line(230,39,85,100)+line(250,39,250,100)+line(280,39,405,70)+text(130,62,"None",fs=11)+text(262,76,"Some",fs=11)+text(360,52,"Full",fs=11)
b+=box(330,140,70,30,"Type? …",fs=11)+box(430,140,60,30,"No",fill="#fde9e0",stroke="#c9602a")+line(380,104,365,140)+line(430,104,460,140)+text(358,125,"Yes",fs=11)+text(458,125,"No",fs=11)
b+=text(250,200,"Root = attribute with highest information gain (Patrons 0.541 bits, Type 0 bits)",fs=11,italic=True)
add("Q9",fig("Figure 9. Decision tree for the restaurant waiting problem (leaf = WillWait yes/no)",b,520,212))

# Q10 over/under fitting
import math
def curve(f,x0,x1,n=60,sx=lambda x:x,sy=lambda y:y):
    pts=[(sx(x0+(x1-x0)*i/n),sy(f(x0+(x1-x0)*i/n))) for i in range(n+1)]
    return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
pts=[(0.1,0.28),(0.2,0.45),(0.3,0.55),(0.4,0.62),(0.5,0.78),(0.6,0.75),(0.7,0.9),(0.8,0.82),(0.9,0.95)]
def panel(ox,title,fn):
    o=f'<rect x="{ox}" y="25" width="170" height="130" fill="#fafafa" stroke="#ccc"/>'+text(ox+85,16,title,bold=True)
    for x,y in pts: o+=f'<circle cx="{ox+10+x*150:.1f}" cy="{150-y*115:.1f}" r="3.5" fill="#3b6fd4"/>'
    o+=f'<path d="{fn(ox)}" fill="none" stroke="#c9302c" stroke-width="2"/>'
    return o
under=lambda ox:f"M{ox+10},{150-0.35*115} L{ox+160},{150-0.62*115}"
good=lambda ox:curve(lambda x:0.15+1.25*x-0.5*x*x,0.05,0.95,sx=lambda x:ox+10+x*150,sy=lambda y:150-min(y,1)*115)
def over(ox):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    def f(x):
        s=0
        for i,(xi,yi) in enumerate(pts):
            t=yi
            for j,(xj,_) in enumerate(pts):
                if i!=j: t*= (x-xj)/(xi-xj)
            s+=t
        return s
    return curve(f,0.1,0.9,n=120,sx=lambda x:ox+10+x*150,sy=lambda y:150-max(min(y,1.15),-0.1)*115)
b=panel(10,"Underfitting (high bias)",under)+panel(210,"Good fit",good)+panel(410,"Overfitting (high variance)",over)
b+=text(95,175,"too simple: high train & test error",fs=11,italic=True)+text(295,175,"balanced: low train & test error",fs=11,italic=True)+text(495,175,"memorises noise: train≈0, test high",fs=11,italic=True)
add("Q10",fig("Figure 10. Underfitting, good fit and overfitting on the same data",b,600,190))

# Q12 passive vs active? agent loop with Q table
b=box(20,30,100,40,"State s",fill="#e8f0fe")+box(180,30,130,40,"Choose a\n(ε-greedy)",fill="#ede7f6",stroke="#6a4cc2")+box(370,30,120,40,"Take a →\nreward r, s'",fill="#fff3cd",stroke="#c99a00")+box(180,120,330,44,"Q(s,a) ← Q(s,a) + α[ r + γ max Q(s',a') − Q(s,a) ]",fill="#e4f3d6",stroke="#5a9a2a",fs=12)
b+=arrow(120,50,180,50)+arrow(310,50,370,50)+arrow(430,70,430,120)+f'<path d="M180,142 L70,142 L70,70" fill="none" stroke="#444" stroke-width="1.5" marker-end="url(#a)"/>'+text(120,136,"s ← s'",fs=11)
add("Q12",fig("Figure 12. Q-learning cycle",b,520,180))

# Q13 SVM
b='<rect x="10" y="10" width="360" height="200" fill="#fafafa" stroke="#ccc"/>'
b+='<line x1="60" y1="190" x2="320" y2="30" stroke="#222" stroke-width="2"/><line x1="40" y1="170" x2="300" y2="10" stroke="#888" stroke-dasharray="5,3"/><line x1="80" y1="210" x2="340" y2="50" stroke="#888" stroke-dasharray="5,3"/>'
for x,y in ((70,100),(110,70),(150,50),(100,130),(60,60),(200,35)): b+=f'<circle cx="{x}" cy="{y}" r="6" fill="#3b6fd4"/>'
for x,y in ((250,190),(300,160),(330,120),(210,180),(180,150),(340,180)): b+=f'<rect x="{x-6}" y="{y-6}" width="12" height="12" fill="#c9602a"/>'
b+='<circle cx="150" cy="50" r="10" fill="none" stroke="#2a7a3a" stroke-width="2"/><circle cx="180" cy="150" r="0" /><rect x="168" y="138" width="24" height="24" fill="none" stroke="#2a7a3a" stroke-width="2"/>'
b+=text(190,230,"solid line: hyperplane w·x + b = 0; dashed lines: margin (width 2/‖w‖); circled points: support vectors",fs=11,italic=True)
b+=text(270,25,"w·x+b=+1",fs=10,color="#666")+text(330,75,"w·x+b=−1",fs=10,color="#666")
add("Q13",fig("Figure 13. SVM maximum-margin hyperplane",b,380,242))

# Q14 four approaches 2x2
b=""
cells=[(10,10,"Thinking humanly","Cognitive modelling\n(GPS, SOAR)"),(250,10,"Thinking rationally","'Laws of thought', logic\n(Prolog, expert systems)"),(10,100,"Acting humanly","Turing Test\n(chatbots, humanoid robots)"),(250,100,"Acting rationally","Rational agent – most widely used\n(self-driving car, chess engine)")]
for x,y,h,t in cells: b+=box(x,y,230,80,h+"\n"+t,fill="#e8f0fe" if "rationally" not in h else "#d8efdf",fs=12)
b+=text(125,198,"HUMAN-LIKE",bold=True,color="#555")+text(365,198,"RATIONAL (IDEAL)",bold=True,color="#555")
add("Q14",fig("Figure 14a. The four approaches to defining AI",b,490,210))
b=box(10,20,120,40,"Interrogator\n(human)",fill="#fff3cd",stroke="#c99a00")+box(260,0,120,40,"Human",fill="#e0f4e8",stroke="#2a8a55")+box(260,60,120,40,"Computer",fill="#fde9e0",stroke="#c9602a")
b+=arrow(130,35,260,20,"typed questions",lx=-5,ly=-6)+arrow(260,32,130,50,"answers",ly=14)+arrow(130,50,260,80)+arrow(260,88,130,58)
b+=text(195,125,"Passes if the interrogator cannot tell which is the machine",fs=11,italic=True)
add("Q14",fig("Figure 14b. The Turing Test set-up",b,400,135))

# Q15 fuzzy
b=box(10,35,95,50,"Crisp\ninput",fill="#f1f1f1",stroke="#888")+box(135,35,110,50,"1. Fuzzification",fill="#e8f0fe")+box(275,35,130,50,"3. Inference\nengine",fill="#ede7f6",stroke="#6a4cc2")+box(435,35,125,50,"4. Defuzzification",fill="#e8f0fe")+box(590,35,95,50,"Crisp\noutput",fill="#f1f1f1",stroke="#888")
b+=arrow(105,60,135,60)+arrow(245,60,275,60,"fuzzy sets",ly=-6)+arrow(405,60,435,60,"fuzzy output",ly=-6)+arrow(560,60,590,60)
b+=box(255,130,170,44,"2. Knowledge base\nmembership functions + IF–THEN rules",fill="#fff3cd",stroke="#c99a00",fs=11)+arrow(340,130,340,85)
add("Q15",fig("Figure 15a. Architecture of a fuzzy logic system (Mamdani)",b,700,190))
# membership functions
b='<rect x="20" y="10" width="420" height="130" fill="#fafafa" stroke="#ccc"/>'
def tri(x0,x1,x2,c,n): return f'<polyline points="{x0},140 {x1},20 {x2},140" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="2"/>'+text(x1,160,n,bold=True,color=c)
b+=tri(20,80,200,"#3b6fd4","Cold")+tri(120,230,340,"#c99a00","Warm")+tri(260,380,440,"#c9302c","Hot")
b+=f'<line x1="300" y1="10" x2="300" y2="140" stroke="#222" stroke-dasharray="4,3"/>'+text(300,175,"x = 28 °C → Warm 0.7, Hot 0.2",fs=11,italic=True)
b+=text(10,20,"1",fs=10,anchor="end")+text(10,140,"0",fs=10,anchor="end")+text(5,80,"μ",fs=11,anchor="end")
add("Q15",fig("Figure 15b. Triangular membership functions for temperature",b,460,185))

# Supplement A UCS
b=""; P={"A":(40,100),"B":(150,50),"C":(150,160),"D":(270,50),"E":(270,130),"F":(270,200),"G":(380,100)}
for a,c,w in (("A","B",1),("A","C",4),("B","D",1),("B","E",3),("C","F",5),("D","G",2),("E","G",1),("F","G",2)):
    red = (a,c) in (("A","B"),("B","D"),("D","G"))
    b+=line(*P[a],*P[c],color="#c9302c" if red else "#999",w=3 if red else 1.5)+text((P[a][0]+P[c][0])/2+6,(P[a][1]+P[c][1])/2-4,str(w),fs=12,bold=True,color="#333")
for n,(x,y) in P.items(): b+=node(x,y,n,fill="#fff3cd" if n=="G" else "#e8f0fe")
b+=text(220,235,"Least-cost path A → B → D → G (red), cost 4",fs=12,bold=True,color="#c9302c")
add("SA",fig("Figure A. Uniform-cost search example graph",b,440,245))

# Supplement B minimax tree
def minimax():
    P={"A":(260,25),"B":(140,90),"C":(380,90),"D":(80,160),"E":(200,160),"F":(320,160),"G":(440,160)}
    leaves=[("H",50,-1),("I",110,4),("J",170,2),("K",230,6),("L",290,-3),("M",350,-5),("N",410,0),("O",470,7)]
    par={"H":"D","I":"D","J":"E","K":"E","L":"F","M":"F","N":"G","O":"G"}
    o=""
    for c,p in (("B","A"),("C","A"),("D","B"),("E","B"),("F","C"),("G","C")): o+=line(*P[p],*P[c])
    for l,x,v in leaves: o+=line(*P[par[l]],x,235)
    for n,(x,y) in P.items():
        sh="tri_up" if n in "ADEFG" else "tri_dn"
        val={"A":4,"B":4,"C":-3,"D":4,"E":6,"F":-3,"G":7}[n]
        o+=node(x,y,n,r=17,shape=sh,fill="#fde9e0" if sh=="tri_up" else "#dbe6fb")+text(x+26,y+4,str(val),fs=12,bold=True,color="#c9302c")
    for l,x,v in leaves: o+=node(x,245,l,r=14,shape="s",fill="#f1f1f1")+text(x,278,str(v),fs=12,bold=True)
    o+=text(500,30,"MAX ▲",anchor="start",bold=True,color="#c9602a")+text(500,95,"MIN ▼",anchor="start",bold=True,color="#3b6fd4")+text(500,165,"MAX ▲",anchor="start",bold=True,color="#c9602a")
    o+=line(260,25,140,90,color="#2a7a3a",w=3)+line(140,90,80,160,color="#2a7a3a",w=3)+line(80,160,110,231,color="#2a7a3a",w=3)
    return fig("Figure B1. Minimax tree: red numbers are backed-up values; best path A → B → D → I (value 4)",o,580,290)
add("SB",minimax())
def alphabeta():
    P={"A":(240,25),"B":(130,90),"C":(350,90),"D":(70,160),"E":(190,160),"F":(310,160),"G":(430,160)}
    L=[("2",40,"D",1),("3",100,"D",1),("5",160,"E",1),("9",220,"E",0),("0",280,"F",1),("1",340,"F",1),("7",400,"G",0),("5",460,"G",0)]
    o=""
    for c,p in (("B","A"),("C","A"),("D","B"),("E","B"),("F","C"),("G","C")): o+=line(*P[p],*P[c])
    for v,x,p,kept in L: o+=line(*P[p],x,238,color="#999" if kept else "#c9302c",dash=not kept)
    vals={"A":"3","B":"3","C":"1","D":"3","E":"5","F":"1","G":"pruned"}
    for n,(x,y) in P.items():
        sh="tri_up" if n in "ADEFG" else "tri_dn"
        o+=node(x,y,n,shape=sh,fill="#fde9e0" if sh=="tri_up" else "#dbe6fb")+text(x+28,y+4,vals[n],fs=12,bold=True,color="#c9302c")
    for v,x,p,kept in L: o+=box(x-14,238,28,28,v,fill="#f1f1f1" if kept else "#fff",stroke="#888" if kept else "#c9302c",fs=12)
    o+=text(230,105,"α=−∞ β=3",fs=10,color="#555")+text(190,185,"α=5 ≥ β=3 → ✂ prune 9",fs=10,color="#c9302c",anchor="middle")
    o+=text(350,60,"α=3 β=1 → ✂ prune G",fs=10,color="#c9302c")
    return fig("Figure B2. Alpha-beta pruning: dashed red branches are never evaluated; root value 3",o,520,285)
add("SB",alphabeta())

# Supplement C Bayesian network
b=box(120,10,110,36,"Disease\nP=0.1",fill="#fde9e0",stroke="#c9602a",fs=12)+box(20,100,110,36,"Fever\nP(F|D)=0.8",fill="#e8f0fe",fs=11)+box(220,100,120,36,"Cough\nP(C|D)=0.7",fill="#e8f0fe",fs=11)
b+=arrow(150,46,90,100)+arrow(200,46,260,100)
b+=box(380,10,110,36,"Rain",fill="#fde9e0",stroke="#c9602a")+box(380,100,110,36,"Wet road\nP=0.95 | 0.10",fill="#e8f0fe",fs=11)+arrow(435,46,435,100)
add("SC",fig("Figure C. Bayesian networks (DAGs with conditional probability tables)",b,520,150))
