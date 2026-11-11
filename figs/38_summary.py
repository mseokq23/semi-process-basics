import numpy as np
from common import *

P = 38

# 1. 시리즈 전체 지도
phases = [("시작", "1 ~ 3편", "8대 공정, PN / MOSFET\nclean room", "#eceff1"),
          ("wafer", "4 ~ 5편", "CZ ingot, wafer 가공\nepi / SOI", "#eceff1"),
          ("산화", "6 ~ 7편", "건식 / 습식 산화\nDeal-Grove, STI", "#e3f2fd"),
          ("photo", "8 ~ 13편", "PR, 해상도 / DoF\nOPC, multi patterning, EUV", "#fce4ec"),
          ("진공, plasma", "14 ~ 15편", "평균자유행로, sheath\nCCP / ICP", "#f3e5f5"),
          ("식각", "16 ~ 19편", "선택비, 이방성, RIE\n고종횡비, ALE", "#fff3e0"),
          ("증착", "20 ~ 24편", "피복성, gap fill, PVD / CVD\nALD, High-k", "#e8f5e9"),
          ("doping", "25 ~ 28편", "확산, ion 주입\n열처리, TED", "#fde2e2"),
          ("금속배선", "29 ~ 31편", "silicide, W plug, EM\nCu damascene, Low-k", "#fbe9e7"),
          ("CMP, 세정", "32 ~ 33편", "평탄화, dishing / erosion\nRCA 세정, 건조", "#e0f2f1"),
          ("공정 통합", "34 ~ 35편", "CMOS inverter 32단계\nmask 15장", "#fff8e1"),
          ("계측, 후공정", "36 ~ 37편", "SPC, 수율, EDS\nTSV, HBM, hybrid bonding", "#ede7f6")]
f, ax = canvas(14.6, 7.6, (0, 40), (-0.6, 20.4))
W, H = 8.6, 5.0
pos = {}
for i, (name, ref, kw, c) in enumerate(phases):
    row, col = divmod(i, 4)
    col = col if row % 2 == 0 else 3 - col
    x = 0.6 + col * 10.0
    y = 14.4 - row * 7.0
    pos[i] = (x, y)
    box(ax, x, y, W, H, "", fc=c, size=9)
    text(ax, x + W / 2, y + H - 0.9, name, size=11.5, weight="bold")
    text(ax, x + W / 2, y + H - 1.85, ref, size=9, color="#555555")
    text(ax, x + W / 2, y + 1.45, kw, size=9)
for i in range(len(phases) - 1):
    (x0, y0), (x1, y1) = pos[i], pos[i + 1]
    if abs(y0 - y1) < 0.1:
        if x1 > x0:
            arrow(ax, x0 + W + 0.05, y0 + H / 2, x1 - 0.05, y1 + H / 2, lw=1.3, ms=10)
        else:
            arrow(ax, x0 - 0.05, y0 + H / 2, x1 + W + 0.05, y1 + H / 2, lw=1.3, ms=10)
    else:
        arrow(ax, x0 + W / 2, y0 - 0.05, x1 + W / 2, y1 + H + 0.05, lw=1.3, ms=10)
save(f, P, "big_map")

# 2. 공정끼리 주고받는 영향
f, ax = canvas(13.6, 6.6, (0, 40), (0.2, 19.6))
BW, BH = 6.2, 2.2
nodes = {"photo": (8, 14), "식각": (21, 14), "증착": (21, 4), "CMP": (8, 4), "세정, 계측": (14.5, 9),
         "ion 주입": (33, 14), "열처리": (33, 9), "silicide, 배선": (33, 4)}
cols = {"photo": "#fce4ec", "식각": "#fff3e0", "증착": "#e8f5e9", "CMP": "#e0f2f1", "세정, 계측": "#eceff1",
        "ion 주입": "#fde2e2", "열처리": "#fff8e1", "silicide, 배선": "#fbe9e7"}
for k, (x, y) in nodes.items():
    box(ax, x - BW / 2, y - BH / 2, BW, BH, k, fc=cols[k], size=10.5, weight="bold")


def link(a, b, lab, lx, ly, ha="center", ls="-", col="#455a64", lw=1.5):
    (xa, ya), (xb, yb) = nodes[a], nodes[b]
    if abs(ya - yb) < 0.01:
        p0 = (xa + np.sign(xb - xa) * (BW / 2 + 0.15), ya)
        p1 = (xb - np.sign(xb - xa) * (BW / 2 + 0.15), yb)
    elif abs(xa - xb) < 0.01:
        p0 = (xa, ya + np.sign(yb - ya) * (BH / 2 + 0.15))
        p1 = (xb, yb - np.sign(yb - ya) * (BH / 2 + 0.15))
    else:
        d = np.array([xb - xa, yb - ya], float)
        d /= np.linalg.norm(d)
        t0 = min((BW / 2 + 0.2) / abs(d[0]), (BH / 2 + 0.2) / abs(d[1]))
        p0 = (xa + d[0] * t0, ya + d[1] * t0)
        p1 = (xb - d[0] * t0, yb - d[1] * t0)
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=13, color=col, lw=lw, ls=ls, zorder=6))
    if lab:
        text(ax, lx, ly, lab, size=9, color="#37474f", ha=ha)


link("photo", "식각", "PR 선폭, 두께가 식각 결과로 (선택비)", 14.5, 15.6)
link("식각", "증착", "깎은 모양을 막이\n덮고 채움 (gap fill)", 21.8, 9.0, ha="left")
link("증착", "CMP", "넘치게 쌓은 막을 갈아냄", 14.5, 2.4)
link("CMP", "photo", "평평해야\n초점이 맞음 (DoF)", 7.2, 9.0, ha="right")
for k in ("photo", "식각", "증착", "CMP"):
    link("세정, 계측", k, "", 0, 0, ls="--", col="#90a4ae", lw=1.0)
text(ax, 14.5, 6.75, "모든 공정 앞뒤로 세정,\n결과를 재서 앞 공정에 feedback", size=8.6, color="#607d8b")
link("ion 주입", "열처리", "손상 회복, 활성화 (TED)", 33.6, 11.5, ha="left")
link("열처리", "silicide, 배선", "뒤로 갈수록\n온도 제한 (열 예산)", 33.6, 6.5, ha="left")
text(ax, 14.5, 18.6, "층 하나를 만드는 고리", size=11, weight="bold", color="#455a64")
text(ax, 33.0, 18.6, "doping과 열 예산", size=11, weight="bold", color="#455a64")
save(f, P, "relations")
