import numpy as np
from common import *
import cmos

P = 1

# 1. 칩이 만들어지는 전체 순서
f, ax = canvas(13, 3.2, (0, 13.9), (-0.9, 2.6))
items = ["설계", "마스크\n제작", "웨이퍼\n제조", "FAB 공정\n(산화, 포토, 식각,\n증착, 이온주입,\n금속배선)",
         "EDS\n(웨이퍼 테스트)", "패키징", "최종\n테스트", "출하"]
ws = [1.2, 1.2, 1.3, 2.3, 1.6, 1.3, 1.2, 1.0]
fcs = ["#eef3f8", "#eef3f8", "#fff4e0", "#fff4e0", "#eaf5e6", "#eaf5e6", "#eaf5e6", "#f4f4f4"]
x = 0.1
xs = []
for s, w, fc in zip(items, ws, fcs):
    box(ax, x, 0.3, w, 1.6, s, fc=fc, size=9.5)
    xs.append((x, x + w))
    x += w + 0.35
for (a, b), (c, d) in zip(xs[:-1], xs[1:]):
    arrow(ax, b + 0.04, 1.1, c - 0.04, 1.1, lw=1.2, ms=10)
bracket(ax, xs[0][0], xs[1][1], -0.05, "설계 단계", below=True, color=C["blue"])
bracket(ax, xs[2][0], xs[3][1], -0.05, "전공정 (웨이퍼 위에 회로 만들기)", below=True, color=C["orange"])
bracket(ax, xs[4][0], xs[6][1], -0.05, "후공정 (검사, 칩으로 포장)", below=True, color=C["green"])
save(f, P, "chip_flow")

# 2. 8대 공정 카드
f, axs = plt.subplots(2, 4, figsize=(13, 6.2))
titles = ["① 웨이퍼 제조", "② 산화", "③ 포토", "④ 식각", "⑤ 증착 · 이온주입", "⑥ 금속배선",
          "⑦ EDS", "⑧ 패키징"]
subs = ["모래 → 단결정 잉곳 → 얇은 원판", "표면에 SiO₂ 보호막·절연막", "빛으로 PR에 회로 그림 옮기기",
        "그림대로 필요 없는 부분 깎기", "막 올리기 / 불순물 넣기", "소자끼리 금속선으로 연결",
        "웨이퍼 상태로 칩마다 전기 검사", "칩 자르고 보호, 외부와 연결"]
for ax, t, s in zip(axs.ravel(), titles, subs):
    canvas(0, 0, (0, 10), (0, 8.6), ax=ax)
    ax.add_patch(FancyBboxPatch((0.1, 0.1), 9.8, 8.4, boxstyle="round,pad=0,rounding_size=0.4",
                                fc="#fafafa", ec="#bbbbbb", lw=1.0, zorder=0))
    text(ax, 5, 7.7, t, size=12, weight="bold")
    text(ax, 5, 0.9, s, size=9.5, color="#444444")
a = axs.ravel()
# ① 웨이퍼
wafer_top(a[0], 5, 4.2, 2.4, c="#c9d1d9")
for i in np.arange(-2, 2.01, 0.8):
    for j in np.arange(-2, 2.01, 0.8):
        if (i + 0.4) ** 2 + (j + 0.4) ** 2 < 1.9 ** 2:
            rect(a[0], 5 + i - 0.4 + 0.05, 4.2 + j - 0.4 + 0.05, 0.7, 0.7, "#e9eef2", lw=0.4, z=3)
# ② 산화
rect(a[1], 1.5, 2.0, 7, 2.2, "si")
rect(a[1], 1.5, 4.2, 7, 0.8, "ox")
for xx in [2.5, 4, 5.5, 7]:
    arrow(a[1], xx, 6.6, xx, 5.2, color="red", ms=9)
text(a[1], 5, 6.9, "O₂ / H₂O", size=9, color=C["red"])
text(a[1], 5, 3.1, "Si", size=10)
text(a[1], 5, 4.6, "SiO₂", size=9)
# ③ 포토
rect(a[2], 1.5, 1.8, 7, 1.6, "si")
rect(a[2], 1.5, 3.4, 7, 0.5, "ox")
rect(a[2], 1.5, 3.9, 7, 0.7, "pr")
for x0, x1 in [(1.2, 3.2), (4.2, 5.8), (6.8, 8.8)]:
    rect(a[2], x0, 6.0, x1 - x0, 0.35, "#444444")
rect(a[2], 1.2, 6.0, 7.6, 0.35, "none", ec="#444444")
for xx in [3.7, 6.3]:
    arrow(a[2], xx, 7.0, xx, 4.7, color="#8e44ad", ls="--", ms=9)
text(a[2], 9.0, 6.2, "마스크", size=8.5, ha="left")
# ④ 식각
rect(a[3], 1.5, 1.8, 7, 2.0, "si")
for x0, x1 in [(1.5, 3.2), (4.2, 5.8), (6.8, 8.5)]:
    rect(a[3], x0, 3.8, x1 - x0, 0.6, "ox")
    rect(a[3], x0, 4.4, x1 - x0, 0.7, "pr")
for xx in [3.7, 6.3]:
    arrow(a[3], xx, 6.6, xx, 4.0, color="#555555", ms=9)
text(a[3], 5, 6.9, "플라즈마 / 식각액", size=9, color="#555555")
# ⑤ 증착, 이온주입
rect(a[4], 0.8, 2.0, 4.0, 2.0, "si")
rect(a[4], 0.8, 4.0, 4.0, 0.6, "nit")
for xx, yy in [(1.5, 6.2), (2.6, 5.6), (3.6, 6.4), (2.0, 5.1), (4.1, 5.3)]:
    circ(a[4], xx, yy, 0.18, "nit", lw=0.5)
text(a[4], 2.8, 3.0, "증착", size=9.5)
rect(a[4], 5.4, 2.0, 4.0, 2.6, "si")
rect(a[4], 5.4, 3.3, 4.0, 0.8, "np", lw=0.3)
for xx in [6.0, 6.9, 7.8, 8.7]:
    arrow(a[4], xx, 6.6, xx, 4.7, color="red", ms=8)
text(a[4], 7.4, 2.6, "이온주입", size=9.5)
# ⑥ 금속배선
rect(a[5], 1.2, 1.8, 7.6, 1.2, "si")
rect(a[5], 1.2, 3.0, 7.6, 3.6, "ox", lw=0.6)
for xx in [2.5, 5.0, 7.5]:
    rect(a[5], xx - 0.25, 3.0, 0.5, 1.4, "w")
rect(a[5], 2.0, 4.4, 3.5, 0.6, "cu")
rect(a[5], 6.8, 4.4, 1.5, 0.6, "cu")
rect(a[5], 4.85, 5.0, 0.5, 0.8, "cu")
rect(a[5], 3.3, 5.8, 5.0, 0.6, "cu")
# ⑦ EDS
rect(a[6], 1.5, 2.0, 7.0, 1.3, "si")
for xx in [2.7, 4.3, 5.7, 7.3]:
    rect(a[6], xx - 0.35, 3.3, 0.7, 0.25, "al", z=3)
rect(a[6], 1.2, 6.2, 7.6, 0.5, "#555555")
for xx in [2.7, 4.3, 5.7, 7.3]:
    line(a[6], [xx + 0.6, xx], [6.2, 3.6], color="#444444", lw=1.3)
text(a[6], 5, 6.9, "프로브 카드", size=9)
# ⑧ 패키징
rect(a[7], 1.0, 2.0, 8.0, 0.5, "#2e7d32", lw=0.6)
for xx in np.arange(1.6, 8.6, 0.9):
    circ(a[7], xx, 1.8, 0.22, "#cfcfcf", lw=0.5)
rect(a[7], 1.6, 2.5, 6.8, 2.8, "emc", lw=0.6, z=2)
rect(a[7], 3.2, 2.7, 3.6, 0.6, "#c9d1d9", z=3, lw=0.5)
for xx, sgn in [(3.3, -1), (6.7, 1)]:
    a[7].plot([xx, xx + sgn * 0.9], [3.3, 2.55], color="#e0b040", lw=1.2, zorder=4)
text(a[7], 5, 4.4, "칩 + 봉지재", size=9, color="white")
plt.tight_layout()
save(f, P, "eight_steps")

# 3. 층마다 반복되는 순서
f, ax = canvas(7.5, 6.2, (-5.2, 5.2), (-4.3, 4.3))
steps = ["박막 만들기\n(산화, 증착)", "포토\n(PR에 그림)", "식각 또는\n이온주입", "PR 제거\n세정", "CMP\n(필요하면)",
         "검사\n(두께, 선폭, 결함)"]
cols = ["#fff4e0", "#f9e6f0", "#e8eef8", "#eaf5e6", "#f1ecf8", "#f4f4f4"]
R = 3.2
angs = np.deg2rad(90 - np.arange(6) * 60)
for a_, s, c in zip(angs, steps, cols):
    box(ax, R * np.cos(a_) - 1.15, R * np.sin(a_) - 0.6, 2.3, 1.2, s, fc=c, size=9.5)
for i in range(6):
    a0 = angs[i] - np.deg2rad(17)
    a1 = angs[(i + 1) % 6] + np.deg2rad(17)
    ax.add_patch(FancyArrowPatch((R * np.cos(a0), R * np.sin(a0)), (R * np.cos(a1), R * np.sin(a1)),
                                 connectionstyle="arc3,rad=-0.25", arrowstyle="-|>",
                                 mutation_scale=12, color="#555555", lw=1.3, zorder=1))
text(ax, 0, 0.35, "한 층 = 한 바퀴", size=12, weight="bold")
text(ax, 0, -0.45, "칩 하나 = 수십 바퀴", size=11, color="#555555")
save(f, P, "unit_loop")

# 4. 시리즈 끝에서 이해하게 될 그림 (CMOS 인버터 단면)
f, ax = canvas(12, 5.2, (-0.3, 24.3), (-4.6, 7.4))
cmos.draw(ax, dict(cmos.FINAL, dev_labels=False), size=9)
text(ax, 6.0, -4.95, "NMOS", size=11, weight="bold")
text(ax, 18.0, -4.95, "PMOS", size=11, weight="bold")
legend(ax, ["ox", "nit", "poly", "np", "pp", "sil", "w", "cu", "lowk"], loc="upper left",
       ncol=9, size=8.5, bbox=(0.0, 1.07),
       names=dict(ox="SiO₂", lowk="Low-k", w="W 플러그", cu="Cu 배선"))
save(f, P, "cmos_preview")
