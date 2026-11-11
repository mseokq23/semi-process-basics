import numpy as np
from common import *
import cmos

P = 2


def lattice(ax, dop=None):
    n = 5
    for i in range(n):
        for j in range(4):
            x, y = i * 2.0, j * 2.0
            if i < n - 1:
                for dy in (-0.12, 0.12):
                    line(ax, [x + 0.45, x + 1.55], [y + dy, y + dy], color="#777777", lw=1.0, z=2)
            if j < 3:
                for dx in (-0.12, 0.12):
                    line(ax, [x + dx, x + dx], [y + 0.45, y + 1.55], color="#777777", lw=1.0, z=2)
    for i in range(n):
        for j in range(4):
            x, y = i * 2.0, j * 2.0
            if dop and (i, j) == (2, 2):
                c = "#9cc3e8" if dop == "P" else "#f0a8a8"
                circ(ax, x, y, 0.45, c, lw=1.0)
                text(ax, x, y, dop, size=10, weight="bold")
            else:
                circ(ax, x, y, 0.42, "#e8e8e8", lw=0.8)
                text(ax, x, y, "Si", size=8.5)
    if dop == "P":
        circ(ax, 5.0, 4.95, 0.16, C["blue"], ec=C["blue"], z=6)
        ax.add_patch(Arc((4.0, 4.0), 2.2, 2.2, theta1=-20, theta2=110, color=C["blue"], lw=1.0,
                         ls="--", zorder=5))
        text(ax, 5.3, 5.35, "남는 전자 (자유전자)", size=9, ha="left", color=C["blue"], box="white")
    if dop == "B":
        # 오른쪽 결합 하나가 전자 하나 부족
        circ(ax, 5.0, 4.12, 0.17, "white", ec=C["red"], lw=1.4, z=6)
        text(ax, 5.3, 4.75, "빈자리 (홀)", size=9, ha="left", color=C["red"], box="white")


f, axs = plt.subplots(1, 3, figsize=(13, 4.4))
tt = ["순수 실리콘 (전자 4개씩 공유)", "인(P) 도핑 → n형", "붕소(B) 도핑 → p형"]
for ax, d, t in zip(axs, [None, "P", "B"], tt):
    canvas(0, 0, (-0.9, 9.9), (-0.9, 6.9), ax=ax)
    lattice(ax, d)
    ax.set_title(t, fontsize=11.5)
plt.tight_layout()
save(f, P, "lattice_doping")

# 도핑 농도 감각
f, ax = plt.subplots(figsize=(10, 3.3))
ax.set_xscale("log")
ax.set_xlim(1e9, 1e23)
ax.set_ylim(0, 6)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
rows = [("진성 캐리어 nᵢ (300 K)", 1e10, 1e10, "#888888"),
        ("기판", 1e15, 1e16, PAL[0]),
        ("웰", 1e16, 1e18, PAL[2]),
        ("채널 (Vt 조절)", 1e17, 1e18, PAL[3]),
        ("소스/드레인", 1e19, 1e21, PAL[1]),
        ("Si 원자 자체", 5e22, 5e22, "#222222")]
for k, (s, a, b, c) in enumerate(rows):
    y = 5.2 - k * 0.9
    if a == b:
        ax.plot([a], [y], "D", color=c, ms=8)
    else:
        ax.plot([a, b], [y, y], color=c, lw=8, solid_capstyle="butt")
    ax.text(b * 2.2 if a != b else a * 2.2, y, s, va="center", fontsize=10)
ax.set_xlabel("농도 (cm⁻³)")
ax.set_title("도핑 농도 감각: 가장 진한 소스/드레인도 Si 원자 수십~수천 개 중 1개", fontsize=11.5, loc="left")
ax.grid(axis="x", alpha=0.3)
save(f, P, "doping_scale")

# PN 접합
f, axs = plt.subplots(2, 1, figsize=(9, 5.6))
rng = np.random.default_rng(3)
for k, ax in enumerate(axs):
    canvas(0, 0, (-0.2, 16.2), (-0.6, 4.4), ax=ax)
    if k == 0:
        rect(ax, 0, 0, 7.6, 4, "#f9e0e0")
        rect(ax, 8.4, 0, 7.6, 4, "#dceaf7")
        dep = (99, -99)
    else:
        rect(ax, 0, 0, 8, 4, "#f9e0e0")
        rect(ax, 8, 0, 8, 4, "#dceaf7")
        dep = (6.4, 9.6)
        rect(ax, 6.4, 0, 3.2, 4, "#ffffff", alpha=0.75, z=2.5, lw=0.0)
        ax.plot([6.4, 6.4], [0, 4], "--", color="#555555", lw=0.8, zorder=3)
        ax.plot([9.6, 9.6], [0, 4], "--", color="#555555", lw=0.8, zorder=3)
        arrow(ax, 9.3, 4.25, 6.7, 4.25, color="purple", ms=10)
        text(ax, 8.0, 4.55, "전계 E", size=9, color=C["purple"])
    xs0 = np.linspace(0.5, 7.1, 7)
    xs1 = np.linspace(8.9, 15.5, 7) if k == 0 else np.linspace(8.5, 15.5, 8)
    if k == 1:
        xs0 = np.linspace(0.5, 7.5, 8)
    for x in xs0:
        for y in [0.7, 2.0, 3.3]:
            text(ax, x, y, "⊖", size=11, color="#a33")
            if not (dep[0] <= x + 0.35 <= dep[1]):
                text(ax, x + 0.4, y + 0.3, "+", size=9, color=C["red"], weight="bold")
    for x in xs1:
        for y in [0.7, 2.0, 3.3]:
            text(ax, x, y, "⊕", size=11, color="#235")
            if not (dep[0] <= x - 0.35 <= dep[1]):
                text(ax, x - 0.4, y + 0.3, "−", size=10, color=C["blue"], weight="bold")
    if k == 0:
        text(ax, 3.8, -0.35, "p형: 홀(+)이 많음, ⊖는 고정된 억셉터 이온", size=9)
        text(ax, 12.2, -0.35, "n형: 전자(−)가 많음, ⊕는 고정된 도너 이온", size=9)
        ax.set_title("붙이기 전", fontsize=11, loc="left")
    else:
        text(ax, 8.0, -0.35, "공핍영역: 캐리어가 빠져나가고 고정 이온만 남음", size=9.5)
        ax.set_title("붙인 후 (PN 접합)", fontsize=11, loc="left")
plt.tight_layout()
save(f, P, "pn_junction")

# MOSFET 구조
f, ax = canvas(10, 5.2, (-1.5, 15.5), (-6.0, 4.6))
rect(ax, 0, -5, 14, 5, "pw", lw=0.8)
rect(ax, 0.6, -1.4, 4.0, 1.4, "np")
rect(ax, 9.4, -1.4, 4.0, 1.4, "np")
rect(ax, 4.3, 0, 5.4, 0.25, "ox")
rect(ax, 4.3, 0.25, 5.4, 1.6, "poly")
for x, s in [(2.6, "S"), (7.0, "G"), (11.4, "D")]:
    yb = 1.85 if s == "G" else 0.0
    line(ax, [x, x], [yb, 3.3], lw=1.4)
    circ(ax, x, 3.5, 0.22, "white", lw=1.3)
    text(ax, x, 4.1, {"S": "소스 (S)", "G": "게이트 (G)", "D": "드레인 (D)"}[s], size=10.5,
         weight="bold")
line(ax, [7.0, 7.0], [-5, -5.5], lw=1.4)
circ(ax, 7.0, -5.7, 0.2, "white", lw=1.3)
text(ax, 7.6, -5.7, "바디 (B)", size=10, ha="left", weight="bold")
text(ax, 2.6, -0.7, "n⁺", size=11, weight="bold")
text(ax, 11.4, -0.7, "n⁺", size=11, weight="bold")
text(ax, 7.0, 1.05, "poly-Si 게이트", size=10)
text(ax, 7.0, -3.4, "p형 바디 (기판 또는 P-well)", size=10)
text(ax, 14.2, 0.4, "게이트 산화막\n(얇은 SiO₂)", size=9, ha="left")
arrow(ax, 14.1, 0.35, 9.8, 0.13, lw=0.9, ms=8)
bracket(ax, 4.6, 9.4, -2.0, "채널 길이 L", below=True, color=C["blue"])
ax.plot([4.6, 4.6], [-1.4, -2.0], ":", color=C["blue"], lw=0.8)
ax.plot([9.4, 9.4], [-1.4, -2.0], ":", color=C["blue"], lw=0.8)
text(ax, 7.0, -0.45, "채널 자리", size=9, color="#555555")
save(f, P, "mosfet")

# ON / OFF
f, axs = plt.subplots(1, 2, figsize=(12, 3.6))
for k, ax in enumerate(axs):
    canvas(0, 0, (-0.5, 14.5), (-4.0, 3.5), ax=ax)
    rect(ax, 0, -3.6, 14, 3.6, "pw", lw=0.8)
    rect(ax, 0.6, -1.4, 4.0, 1.4, "np")
    rect(ax, 9.4, -1.4, 4.0, 1.4, "np")
    rect(ax, 4.3, 0, 5.4, 0.25, "ox")
    rect(ax, 4.3, 0.25, 5.4, 1.6, "poly")
    if k == 0:
        ax.set_title("VG = 0 → 채널 없음 (OFF)", fontsize=11.5, loc="left")
        text(ax, 7.0, -1.0, "n⁺ - p - n⁺ 가 막고 있어서 전류 거의 0", size=9.5, color="#555555")
        text(ax, 7.0, 2.6, "0 V", size=10)
    else:
        ax.set_title("VG > Vth → 전자 채널 생김 (ON)", fontsize=11.5, loc="left")
        rect(ax, 4.6, -0.22, 4.8, 0.22, "#2f6fb0", lw=0.0, z=3)
        for x in np.arange(4.9, 9.3, 0.45):
            text(ax, x, -0.1, "−", size=8, color="white", weight="bold", z=6)
        text(ax, 7.0, 2.6, "+ 전압", size=10, color=C["red"])
        arrow(ax, 3.4, -1.9, 10.6, -1.9, color="blue", lw=1.6, ms=12)
        text(ax, 7.0, -2.5, "전자: 소스 → 드레인", size=9.5, color=C["blue"])
        text(ax, 7.0, -0.75, "반전층 (채널)", size=9, color=C["blue"])
plt.tight_layout()
save(f, P, "mosfet_onoff")

# CMOS 단면에서 공정이 만드는 부분
f, ax = canvas(13, 6.6, (-7.5, 31.5), (-6.4, 8.6))
cmos.draw(ax, dict(cmos.FEOL_DONE, pmd="flat", ct="plug", m1=True), size=8.5)
notes = [
    ((12.0, -0.9), (-7.2, -2.2), "STI (소자 분리)\n식각 + 증착 + CMP"),
    ((6.0, 0.05), (-7.2, 1.3), "게이트 산화막\n산화"),
    ((5.7, 1.0), (-7.2, 3.6), "게이트\n증착 + 포토 + 식각"),
    ((3.0, -0.4), (-7.2, -4.9), "소스/드레인\n이온주입 + 열처리"),
    ((9.0, 3.4), (25.3, 6.8), "컨택, 배선\n금속배선 (증착, 식각, CMP)"),
    ((19.4, -0.06), (25.3, 2.2), "실리사이드\n금속 증착 + 열처리"),
    ((19.0, 0.6), (25.3, 4.5), "스페이서\n증착 + 식각"),
    ((20.0, -2.8), (25.3, -2.6), "웰\n이온주입 + 열처리"),
]
for (px, py), (tx, ty), s in notes:
    ha = "left"
    text(ax, tx, ty, s, size=9, ha=ha, box="#fff8e1")
    x_end = tx + (0 if tx > 20 else 5.6)
    arrow(ax, x_end if tx < 0 else tx - 0.2, ty, px, py, lw=0.8, ms=7, color="#555555")
save(f, P, "cmos_parts")
