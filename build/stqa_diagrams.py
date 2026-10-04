import math
from svg import box, arrow, line, node, text, fig

G = dict(fill="#e6f4ea", stroke="#2e7d32")   # green
R = dict(fill="#fdecea", stroke="#c62828")   # red
Y = dict(fill="#fff6e0", stroke="#b7791f")   # amber
P = dict(fill="#f1e8fb", stroke="#6a3fb5")   # purple
D = {}

# ---------- Q1: McCall's quality factors ----------
b = box(250, 8, 200, 34, "McCall's Quality Factors", bold=True)
b += line(350, 42, 350, 60) + line(115, 60, 585, 60)
cols = [("Product Operation", ["Correctness", "Reliability", "Efficiency", "Integrity", "Usability"], G),
        ("Product Revision", ["Maintainability", "Flexibility", "Testability"], Y),
        ("Product Transition", ["Portability", "Reusability", "Interoperability"], P)]
for i, (h, items, c) in enumerate(cols):
    x = 15 + i * 235
    b += line(x + 100, 60, x + 100, 78)
    b += f'<rect x="{x}" y="78" width="200" height="132" rx="7" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.4"/>'
    b += text(x + 100, 98, h, 13, bold=True)
    for j, it in enumerate(items):
        b += text(x + 100, 122 + j * 18, it, 12)
D["Q1"] = [fig("Fig 1.1 – McCall's quality factors grouped into three categories", b, 700, 218)]

# ---------- Q2: error -> fault -> failure, DMP, defect life cycle ----------
b = box(10, 15, 190, 50, "Error / Mistake\n(human action)", **Y)
b += arrow(200, 40, 250, 40)
b += box(252, 15, 190, 50, "Fault / Defect / Bug\n(in code or document)", **R)
b += arrow(442, 40, 492, 40)
b += box(494, 15, 190, 50, "Failure\n(wrong behaviour at run time)", fill="#fbe0e0", stroke="#8e1b1b")
b += text(225, 32, "causes", 10, color="#555") + text(467, 32, "if executed", 10, color="#555")
f1 = fig("Fig 2.1 – Error → Fault (Defect) → Failure", b, 700, 80)

steps = ["Defect\nPrevention", "Deliverable\nBaseline", "Defect\nDiscovery", "Defect\nResolution", "Process\nImprovement"]
b = ""
for i, s in enumerate(steps):
    x = 6 + i * 139
    b += box(x, 12, 120, 50, s, **(G if i in (0, 4) else {}))
    if i < 4:
        b += arrow(x + 120, 37, x + 139, 37)
    b += line(x + 60, 62, x + 60, 95, dash=True)
b += box(6, 95, 676, 34, "Management Reporting  (status, trends and metrics at every stage)", **Y)
f2 = fig("Fig 2.2 – Defect Management Process", b, 690, 136)

b = ""
row = ["New", "Assigned", "Open", "Fixed", "Retest", "Verified"]
for i, s in enumerate(row):
    x = 8 + i * 112
    b += box(x, 20, 84, 36, s, fs=12)
    if i < 5:
        b += arrow(x + 84, 38, x + 112, 38)
b += box(568, 110, 84, 36, "Closed", fs=12, **G) + arrow(610, 56, 610, 110)
b += box(344, 110, 84, 36, "Reopened", fs=12, **R)
b += arrow(480, 56, 420, 110) + text(462, 92, "fails", 10, color="#c62828", anchor="start")
b += arrow(360, 110, 304, 56)
for i, s in enumerate(["Rejected", "Duplicate", "Deferred"]):
    x = 8 + i * 112
    b += box(x, 160, 84, 32, s, fs=12, fill="#f2f2f2", stroke="#777")
    b += arrow(250, 56, x + 42, 160)
f3 = fig("Fig 2.3 – Defect (bug) life cycle", b, 670, 200)
D["Q2"] = [f1, f2, f3]

# ---------- Q3: V-model ----------
L = ["Requirements Analysis", "System Design", "Architecture Design", "Module Design"]
Rt = ["Acceptance Testing", "System Testing", "Integration Testing", "Unit Testing"]
plans = ["Acceptance test plan", "System test plan", "Integration test plan", "Unit test plan"]
b = ""
for i in range(4):
    lx, rx, y = 10 + i * 40, 520 - i * 40, 15 + i * 65
    b += box(lx, y, 170, 40, L[i], fs=12)
    b += box(rx, y, 170, 40, Rt[i], fs=12, **G)
    b += arrow(lx + 170, y + 20, rx, y + 20, dash=True)
    b += text((lx + 170 + rx) / 2, y + 14, plans[i], 10, color="#555", italic=True)
    if i < 3:
        b += arrow(lx + 85, y + 40, lx + 125, y + 65)
        b += arrow(rx - 40 + 85, y + 65, rx + 85, y + 40)
b += box(270, 275, 160, 40, "Coding", bold=True, **Y)
b += arrow(215, 250, 300, 275) + arrow(400, 275, 485, 250)
b += text(60, 300, "← Verification", 12, color="#1a3f8f", bold=True)
b += text(640, 300, "Validation →", 12, color="#2e7d32", bold=True)
D["Q3"] = [fig("Fig 3.1 – V-Model: every development phase has a matching test phase", b, 700, 322)]

# ---------- Q4: inspection process ----------
b = ""
st = ["Planning", "Overview", "Preparation", "Inspection\nMeeting", "Rework", "Follow-up"]
for i, s in enumerate(st):
    x = 4 + i * 116
    b += box(x, 12, 100, 46, s, fs=12, **(G if i == 5 else {}))
    if i < 5:
        b += arrow(x + 100, 35, x + 116, 35)
D["Q4"] = [fig("Fig 4.1 – Steps of a formal inspection (Fagan inspection)", b, 690, 70)]

# ---------- Q5: metrics life cycle + types ----------
b = box(175, 10, 150, 40, "1. Analysis", bold=True)
b += box(330, 100, 150, 40, "2. Communicate", bold=True, **Y)
b += box(175, 190, 150, 40, "3. Evaluation", bold=True, **G)
b += box(20, 100, 150, 40, "4. Report", bold=True, **P)
b += arrow(325, 30, 405, 100) + arrow(405, 140, 325, 210) + arrow(175, 210, 95, 140) + arrow(95, 100, 175, 30)
D["Q5"] = [fig("Fig 5.1 – Software testing metrics life cycle", b, 500, 240)]

b = box(260, 8, 180, 34, "Software Metrics", bold=True)
b += line(350, 42, 350, 58) + line(110, 58, 590, 58)
for i, (h, s) in enumerate([("Process Metrics", "efficiency of the process\n(DRE, test cycle time)"),
                            ("Product Metrics", "quality of the product\n(defect density, size)"),
                            ("Project Metrics", "project progress\n(effort, cost, schedule)")]):
    x = 10 + i * 240
    b += line(x + 100, 58, x + 100, 72)
    b += box(x, 72, 200, 30, h, bold=True, **[G, Y, P][i])
    b += text(x + 100, 120, s.split("\n")[0], 11, color="#444") + text(x + 100, 135, s.split("\n")[1], 11, color="#444")
D["Q5"].insert(0, fig("Fig 5.0 – Categories of software metrics", b, 700, 145))

# ---------- Q6: black/white box, BVA, state transition ----------
b = text(170, 18, "Black Box Testing", 13, bold=True)
b += box(10, 45, 70, 34, "Input", fs=12) + arrow(80, 62, 120, 62)
b += f'<rect x="120" y="30" width="110" height="64" rx="6" fill="#222"/>' + text(175, 67, "? ? ?", 14, color="#fff", bold=True)
b += arrow(230, 62, 270, 62) + box(270, 45, 70, 34, "Output", fs=12)
b += text(175, 115, "tests behaviour against specification", 11, color="#444", italic=True)
ox = 360
b += text(ox + 170, 18, "White Box Testing", 13, bold=True)
b += box(ox + 10, 45, 70, 34, "Input", fs=12) + arrow(ox + 80, 62, ox + 120, 62)
b += f'<rect x="{ox+120}" y="30" width="110" height="64" rx="6" fill="#fff" stroke="#3b6fd4" stroke-width="1.4"/>'
b += node(ox + 175, 44, "", r=6) + node(ox + 150, 78, "", r=6) + node(ox + 200, 78, "", r=6)
b += line(ox + 171, 49, ox + 154, 73) + line(ox + 179, 49, ox + 196, 73) + line(ox + 156, 78, ox + 194, 78)
b += arrow(ox + 230, 62, ox + 270, 62) + box(ox + 270, 45, 70, 34, "Output", fs=12)
b += text(ox + 175, 115, "tests internal code paths & logic", 11, color="#444", italic=True)
f1 = fig("Fig 6.1 – Black box vs white box view of the program", b, 710, 125)

b = line(30, 50, 670, 50, w=2)
b += f'<rect x="150" y="38" width="400" height="24" fill="#e6f4ea" stroke="#2e7d32"/>'
b += text(350, 55, "Valid partition: 18 – 60", 12, color="#2e7d32", bold=True)
b += text(75, 32, "Invalid (< 18)", 11, color="#c62828") + text(625, 32, "Invalid (> 60)", 11, color="#c62828")
for v, x, ok in [(17, 120, 0), (18, 150, 1), (19, 180, 1), (59, 520, 1), (60, 550, 1), (61, 580, 0)]:
    c = "#2e7d32" if ok else "#c62828"
    b += f'<circle cx="{x}" cy="50" r="5" fill="{c}"/>' + text(x, 82, str(v), 12, color=c, bold=True)
b += text(350, 100, "Test values = min−1, min, min+1, max−1, max, max+1", 11, color="#444", italic=True)
f2 = fig("Fig 6.2 – Boundary Value Analysis for an 'age' field that accepts 18 to 60", b, 700, 108)

b = ""
names = ["Card\nInserted", "1st PIN\nattempt", "2nd PIN\nattempt", "3rd PIN\nattempt", "Card\nBlocked"]
for i, s in enumerate(names):
    x = 10 + i * 140
    c = R if i == 4 else ({} if i else Y)
    b += f'<rect x="{x}" y="25" width="100" height="44" rx="20" fill="{c.get("fill","#e8f0fe")}" stroke="{c.get("stroke","#3b6fd4")}" stroke-width="1.4"/>'
    for k, t in enumerate(s.split("\n")):
        b += text(x + 50, 43 + k * 15, t, 12)
    if i < 4:
        b += arrow(x + 100, 47, x + 140, 47, "" if i == 0 else "wrong", ly=-6)
b += f'<rect x="290" y="135" width="120" height="40" rx="20" fill="#e6f4ea" stroke="#2e7d32" stroke-width="1.4"/>' + text(350, 160, "Access Granted", 12)
b += arrow(200, 69, 310, 135, "correct", lx=-28) + arrow(340, 69, 345, 135, "correct", lx=26) + arrow(480, 69, 390, 135, "correct", lx=30)
f3 = fig("Fig 6.3 – State transition diagram for an ATM PIN entry", b, 690, 185)
D["Q6"] = [f1, f2, f3]

# ---------- Q7: top-down / bottom-up ----------
def tree(ox, title, stub_levels, direction):
    o = text(ox + 160, 18, title, 13, bold=True)
    pos = {"M1": (160, 40), "M2": (60, 100), "M3": (160, 100), "M4": (260, 100), "M5": (34, 160), "M6": (106, 160), "M7": (260, 160)}
    lvl = {"M1": 0, "M2": 1, "M3": 1, "M4": 1, "M5": 2, "M6": 2, "M7": 2}
    for a, c in [("M1", "M2"), ("M1", "M3"), ("M1", "M4"), ("M2", "M5"), ("M2", "M6"), ("M4", "M7")]:
        o += line(ox + pos[a][0], pos[a][1] + 28, ox + pos[c][0], pos[c][1])
    for m, (x, y) in pos.items():
        dashed = lvl[m] in stub_levels
        st = ' stroke-dasharray="4,3"' if dashed else ""
        fill = "#fff6e0" if dashed else "#e8f0fe"
        o += f'<rect x="{ox+x-28}" y="{y}" width="56" height="28" rx="5" fill="{fill}" stroke="#3b6fd4" stroke-width="1.4"{st}/>' + text(ox + x, y + 19, m, 12)
    if direction == "down":
        o += arrow(ox + 318, 45, ox + 318, 185)
    else:
        o += arrow(ox + 318, 185, ox + 318, 45)
    return o
b = tree(0, "Top-down integration", {2}, "down") + tree(360, "Bottom-up integration", {0}, "up")
b += text(160, 210, "dashed lower modules = STUBS (called programs)", 11, color="#b7791f", italic=True)
b += text(520, 210, "dashed top module = DRIVER (calling program)", 11, color="#b7791f", italic=True)
D["Q7"] = [fig("Fig 7.1 – Top-down vs bottom-up integration on the same module hierarchy", b, 700, 220)]

# ---------- Q8: system testing types + alpha/beta ----------
b = box(270, 65, 160, 40, "System Testing", bold=True, **Y)
top = ["Functional", "Performance", "Load / Stress", "Security"]
bot = ["Recovery", "Usability", "Compatibility", "Regression"]
for i, t in enumerate(top):
    x = 10 + i * 175
    b += box(x, 5, 150, 32, t, fs=12) + line(x + 75, 37, 350, 65)
for i, t in enumerate(bot):
    x = 10 + i * 175
    b += box(x, 133, 150, 32, t, fs=12) + line(x + 75, 133, 350, 105)
f1 = fig("Fig 8.1 – Common types of system testing", b, 700, 170)
b = ""
for i, (t, c) in enumerate([("Development\n& System Test", {}), ("Alpha Test\n(in-house, dev site)", Y), ("Beta Test\n(real users, real env.)", P), ("Release to\nMarket", G)]):
    x = 5 + i * 175
    b += box(x, 10, 150, 48, t, fs=12, **c)
    if i < 3:
        b += arrow(x + 150, 34, x + 175, 34)
f2 = fig("Fig 8.2 – Where alpha and beta testing fit before release", b, 690, 68)
D["Q8"] = [f1, f2]

# ---------- Q9: smoke testing ----------
b = box(10, 45, 120, 40, "New Build\nfrom Dev", fs=12)
b += arrow(130, 65, 180, 65)
b += f'<polygon points="260,25 340,65 260,105 180,65" fill="#fff6e0" stroke="#b7791f" stroke-width="1.4"/>' + text(260, 62, "Smoke", 12, bold=True) + text(260, 77, "Test", 12, bold=True)
b += arrow(340, 65, 440, 65, "PASS (stable)") + box(440, 45, 240, 40, "Detailed testing: functional,\nregression, system", fs=12, **G)
b += line(260, 105, 260, 130) + arrow(260, 130, 70, 130, "FAIL – build rejected", ly=-5) + arrow(70, 130, 70, 85)
D["Q9"] = [fig("Fig 9.1 – Smoke test as the gate for every new build", b, 690, 140)]

# ---------- Q10: fishbone, pareto, scatter ----------
b = line(30, 130, 560, 130, w=3, color="#333")
b += box(560, 103, 130, 54, "EFFECT:\nHigh defect rate", bold=True, **R)
bones = [(170, "People", ["Lack of training", "Inexperience"]), (330, "Process", ["No reviews", "Tight schedule"]),
         (490, "Tools", ["No automation", "Outdated tools"])]
for bx, name, subs in bones:
    b += line(bx - 70, 30, bx, 128, w=2, color="#1a3f8f") + text(bx - 70, 22, name, 13, bold=True, color="#1a3f8f")
    for k, (yy, s) in enumerate([(65, subs[0]), (98, subs[1])]):
        xx = bx - 70 + 70 * (yy - 30) / 98
        b += line(xx - 85, yy, xx, yy, w=1) + text(xx - 12, yy - 3, s, 10.5, anchor="end")
bones = [(170, "Requirements", ["Unclear specs", "Frequent changes"]), (330, "Environment", ["Unstable test env.", "Config mismatch"]),
         (490, "Methods", ["Poor test design", "Low coverage"])]
for bx, name, subs in bones:
    b += line(bx - 70, 230, bx, 132, w=2, color="#1a3f8f") + text(bx - 70, 247, name, 13, bold=True, color="#1a3f8f")
    for k, (yy, s) in enumerate([(165, subs[0]), (198, subs[1])]):
        xx = bx - 70 + 70 * (230 - yy) / 98
        b += line(xx - 85, yy, xx, yy, w=1) + text(xx - 12, yy - 3, s, 10.5, anchor="end")
f1 = fig("Fig 10.1 – Cause and effect (Ishikawa / fishbone) diagram", b, 700, 255)

cats = [("UI", 45), ("Functional", 30), ("Performance", 12), ("Security", 8), ("Docs", 5)]
b = line(60, 230, 620, 230) + line(60, 30, 60, 230) + line(620, 30, 620, 230)
for v in range(0, 51, 10):
    y = 230 - 4 * v
    b += line(55, y, 60, y) + text(50, y + 4, str(v), 10, anchor="end")
for p in range(0, 101, 20):
    y = 230 - 2 * p
    b += line(620, y, 625, y) + text(630, y + 4, f"{p}%", 10, anchor="start")
cum, pts = 0, []
for i, (c, n) in enumerate(cats):
    cx = 116 + 112 * i
    cum += n
    b += f'<rect x="{cx-40}" y="{230-4*n}" width="80" height="{4*n}" fill="#7da2e8" stroke="#3b6fd4"/>'
    b += text(cx, 226 - 4 * n, str(n), 11, bold=True) + text(cx, 246, c, 11)
    pts.append((cx, 230 - 2 * cum))
b += line(60, 70, 620, 70, color="#c62828", dash=True) + text(612, 64, "80% line", 10, anchor="end", color="#c62828")
b += '<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) + '" fill="none" stroke="#b7791f" stroke-width="2"/>'
for x, y in pts:
    b += f'<circle cx="{x}" cy="{y}" r="4" fill="#b7791f"/>'
b += text(60, 16, "Defects", 11, bold=True) + text(625, 16, "Cum. %", 11, bold=True)
f2 = fig("Fig 10.2 – Pareto diagram of defects by category (bars) with cumulative % line", b, 700, 255)

data = [(5, 12), (8, 15), (10, 22), (12, 20), (15, 30), (18, 34), (20, 38), (22, 45), (25, 48), (28, 52),
        (30, 60), (33, 58), (35, 66), (38, 72), (40, 75), (43, 80), (45, 88), (48, 90)]
X = lambda v: 60 + v * 11.6
Yv = lambda v: 220 - v * 2
b = line(60, 220, 650, 220) + line(60, 24, 60, 220)
for v in range(0, 51, 10):
    b += line(X(v), 220, X(v), 225) + text(X(v), 238, str(v), 10)
for v in range(0, 101, 20):
    b += line(55, Yv(v), 60, Yv(v)) + text(50, Yv(v) + 4, str(v), 10, anchor="end")
b += line(X(0), Yv(4), X(50), Yv(96), color="#c62828", dash=True)
for x, y in data:
    b += f'<circle cx="{X(x):.1f}" cy="{Yv(y)}" r="4.5" fill="#3b6fd4"/>'
b += text(355, 256, "Module size (KLOC)", 11, bold=True) + text(66, 14, "Defects", 11, bold=True, anchor="start")
b += text(540, 150, "positive correlation", 11, color="#c62828", italic=True)
f3 = fig("Fig 10.3 – Scatter diagram: module size vs number of defects", b, 690, 262)
D["Q10"] = [f1, f2, f3]

# ---------- Q11: control flow graph ----------
N = {1: (150, 30), 2: (150, 95), 3: (150, 165), 4: (80, 235), 5: (220, 235), 6: (150, 305), 7: (290, 95)}
b = ""
def edge(a, c):
    (x1, y1), (x2, y2) = N[a], N[c]
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return arrow(x1 + ux * 17, y1 + uy * 17, x2 - ux * 19, y2 - uy * 19)
for a, c in [(1, 2), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (2, 7)]:
    b += edge(a, c)
b += '<path d="M134,300 C 0,300 0,100 131,98" fill="none" stroke="#444" stroke-width="1.5" marker-end="url(#a)"/>'
for k, (x, y) in N.items():
    b += node(x, y, str(k), **(Y if k in (2, 3) else {}))
b += text(150, 240, "R1", 12, color="#c62828", bold=True) + text(85, 175, "R2", 12, color="#c62828", bold=True) + text(300, 260, "R3", 12, color="#c62828", bold=True)
b += text(215, 88, "false", 10, color="#555") + text(160, 132, "true", 10, color="#555", anchor="start")
D["Q11"] = [fig("Fig 11.1 – Control flow graph (shaded nodes = predicate nodes, R = regions)", b, 340, 330)]

# ---------- Q12: cost of quality ----------
b = box(275, 8, 150, 34, "Cost of Quality", bold=True, **Y)
b += line(350, 42, 350, 60) + line(180, 60, 520, 60) + line(180, 60, 180, 75) + line(520, 60, 520, 75)
b += box(70, 75, 220, 42, "Cost of Conformance\n(cost of good quality)", fs=12, **G)
b += box(410, 75, 220, 42, "Cost of Non-conformance\n(cost of poor quality)", fs=12, **R)
b += line(180, 117, 180, 135) + line(90, 135, 270, 135) + line(520, 117, 520, 135) + line(430, 135, 610, 135)
leaf = [(90, "Prevention", "training, planning,\nstandards", G), (270, "Appraisal", "reviews, testing,\naudits", G),
        (430, "Internal Failure", "rework, re-test,\ndebugging", R), (610, "External Failure", "support, warranty,\nrecalls, penalties", R)]
for x, h, s, c in leaf:
    b += line(x, 135, x, 150) + box(x - 75, 150, 150, 30, h, fs=12, bold=True, **c)
    for k, t in enumerate(s.split("\n")):
        b += text(x, 198 + k * 14, t, 10.5, color="#444")
D["Q12"] = [fig("Fig 12.1 – Classification of quality costs", b, 700, 230)]

# ---------- Q13: MTTF / MTTR / MTBF ----------
b = line(30, 60, 670, 60, color="#999")
b += f'<rect x="40" y="40" width="260" height="20" fill="#7cc48a"/>' + text(170, 54, "system working (up)", 11)
b += f'<rect x="300" y="40" width="80" height="20" fill="#e57373"/>' + text(340, 54, "repair", 11, color="#fff")
b += f'<rect x="380" y="40" width="260" height="20" fill="#7cc48a"/>' + text(510, 54, "system working (up)", 11)
b += text(300, 32, "failure ↓", 10, color="#c62828") + text(380, 32, "↓ restored", 10, color="#2e7d32", anchor="start")
for x1, x2, y, t in [(40, 300, 80, "MTTF"), (300, 380, 80, "MTTR"), (40, 380, 108, "MTBF = MTTF + MTTR")]:
    b += line(x1, y, x2, y) + line(x1, y - 5, x1, y + 5) + line(x2, y - 5, x2, y + 5) + text((x1 + x2) / 2, y + 16, t, 12, bold=True)
D["Q13"] = [fig("Fig 13.1 – Relationship between MTTF, MTTR and MTBF", b, 700, 135)]

# ---------- Q14: FTR flow ----------
b = ""
st = ["Producer says\nproduct is ready", "Review leader\nchecks & distributes", "Reviewers prepare\n(1–2 hrs each)", "Review meeting\n(3–5 people, < 2 hrs)"]
for i, s in enumerate(st):
    x = 4 + i * 172
    b += box(x, 10, 150, 46, s, fs=11.5)
    if i < 3:
        b += arrow(x + 150, 33, x + 172, 33)
for i, (t, c) in enumerate([("Accept", G), ("Accept provisionally", Y), ("Reject", R)]):
    x = 140 + i * 160
    b += box(x, 100, 140, 32, t, fs=12, **c) + arrow(595, 56, x + 70, 100)
D["Q14"] = [fig("Fig 14.1 – Flow of a formal technical review and its three possible decisions", b, 700, 140)]

# ---------- Q15: DMAIC ----------
cx, cy, Rr = 250, 135, 92
lab = [("D", "Define"), ("M", "Measure"), ("A", "Analyze"), ("I", "Improve"), ("C", "Control")]
cols = [{}, Y, R, G, P]
b = ""
for i in range(5):
    a1, a2 = math.radians(-90 + 72 * i + 27), math.radians(-90 + 72 * (i + 1) - 27)
    b += f'<path d="M{cx+Rr*math.cos(a1):.1f},{cy+Rr*math.sin(a1):.1f} A{Rr},{Rr} 0 0 1 {cx+Rr*math.cos(a2):.1f},{cy+Rr*math.sin(a2):.1f}" fill="none" stroke="#444" stroke-width="1.6" marker-end="url(#a)"/>'
for i, (l, w) in enumerate(lab):
    a = math.radians(-90 + 72 * i)
    x, y = cx + Rr * math.cos(a), cy + Rr * math.sin(a)
    c = cols[i]
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="38" fill="{c.get("fill","#e8f0fe")}" stroke="{c.get("stroke","#3b6fd4")}" stroke-width="1.6"/>'
    b += text(x, y - 2, l, 20, bold=True) + text(x, y + 15, w, 11)
b += text(cx, cy + 5, "DMAIC", 14, bold=True, color="#1a3f8f")
D["Q15"] = [fig("Fig 15.1 – The DMAIC improvement cycle of Six Sigma", b, 500, 275)]

b = box(250, 8, 200, 34, "ISO 9000 family", bold=True, **Y)
b += line(350, 42, 350, 58) + line(115, 58, 585, 58)
for i, (h, s) in enumerate([("ISO 9000", "Fundamentals &\nvocabulary"), ("ISO 9001", "Requirements for a QMS\n(the certifiable one)"),
                            ("ISO 9004", "Guidelines for sustained\nsuccess / improvement")]):
    x = 15 + i * 235
    b += line(x + 100, 58, x + 100, 70) + box(x, 70, 200, 56, h + "\n" + s, fs=11.5, **[G, {}, P][i])
D["Q15"].append(fig("Fig 15.2 – Main standards in the ISO 9000 family", b, 700, 135))
