import numpy as np
from common import *

P = 10

# 1. reticle + pellicle
f, ax = canvas(10, 5.0, (0, 20), (0, 10))
rect(ax, 2.0, 6.0, 16.0, 1.6, "#e3f2fd", lw=0.9)
text(ax, 10.0, 7.0, "석영 기판 (빛이 통과)", size=10)
for x0, x1 in [(2.0, 5.0), (6.2, 8.4), (9.6, 11.0), (12.2, 15.0), (16.0, 18.0)]:
    rect(ax, x0, 5.75, x1 - x0, 0.25, "#424242", lw=0.4)
text(ax, 18.3, 5.85, "Cr pattern", size=9.5, ha="left")
rect(ax, 2.0, 2.6, 0.4, 3.15, "#9e9e9e", lw=0.5)
rect(ax, 17.6, 2.6, 0.4, 3.15, "#9e9e9e", lw=0.5)
line(ax, [2.0, 18.0], [2.6, 2.6], color="#7e57c2", lw=1.6)
text(ax, 18.3, 2.6, "pellicle (얇은 막)", size=9.5, ha="left", color=C["purple"])
text(ax, 1.8, 4.1, "frame\n(수 mm)", size=9, ha="right")
circ(ax, 7.0, 2.35, 0.22, "#6d4c41", lw=0.5, z=6)
text(ax, 7.0, 1.6, "먼지: pattern 면에서 멀리 떨어져 있음", size=9.5)
text(ax, 7.0, 0.9, "→ wafer에 맺힐 때 초점이 안 맞아서 흐려짐 (찍히지 않음)", size=9.5)
arrow(ax, 10.0, 9.8, 10.0, 7.7, color="#8e44ad", lw=1.4, ls="--")
text(ax, 10.3, 9.3, "빛", size=9.5, ha="left", color=C["purple"])
save(f, P, "mask_pellicle")

# 2. 접촉 / 근접 / 투영 노광
f, axs = panels(3, 3, 3.8, 4.0, (0, 10), (0, 10), titles=["접촉 (contact)", "근접 (proximity)",
                                                         "투영 (projection)"], size=11)
for k, ax in enumerate(axs):
    rect(ax, 1.0, 0.4, 8.0, 1.0, "si", lw=0.6)
    rect(ax, 1.0, 1.4, 8.0, 0.4, "pr", lw=0.6)
my = {0: 1.85, 1: 3.0, 2: 7.2}[k]
for k, ax in enumerate(axs):
    y = {0: 1.85, 1: 3.0, 2: 7.2}[k]
    rect(ax, 1.0, y, 8.0, 0.35, "#e3f2fd", lw=0.6)
    for x0 in (2.0, 4.6, 7.2):
        rect(ax, x0, y, 0.8, 0.12, "#424242", lw=0.3)
    for x in np.linspace(1.6, 8.4, 6):
        arrow(ax, x, 9.6, x, y + 0.4, color="#8e44ad", ls="--", ms=7, lw=1.0)
text(axs[0], 5.0, 3.2, "mask가 PR에 닿음\n→ 해상도 좋지만 mask, PR 손상", size=9)
vdim(axs[1], 9.4, 1.8, 3.0, "간격", size=9)
text(axs[1], 5.0, 4.5, "띄워서 손상은 줄었지만\n회절로 흐려짐", size=9)
ax = axs[2]
ax.add_patch(Ellipse((5.0, 4.6), 6.0, 1.0, fc="#e1f5fe", ec="#4fc3f7", lw=1.2, zorder=4))
text(ax, 5.0, 4.6, "축소 lens (4:1)", size=9)
for x in (2.4, 5.0, 7.6):
    line(ax, [x, 5.0 + (x - 5.0) * 0.25], [7.15, 1.85], color="#8e44ad", lw=0.9, ls="--")
text(ax, 5.0, 3.0, "mask pattern을 줄여서 맺음", size=9, box="white")
save(f, P, "exposure_types")

# 3. stepper vs scanner
f, axs = plt.subplots(1, 3, figsize=(13.5, 4.4))
for ax in axs:
    canvas(0, 0, (0, 10), (0, 10), ax=ax)
ax = axs[0]
ax.set_title("stepper: 한 칸(shot)을 한 번에", fontsize=11)
rect(ax, 2.0, 8.0, 6.0, 0.4, "#e3f2fd", lw=0.6)
ax.add_patch(Ellipse((5.0, 5.4), 7.0, 1.2, fc="#e1f5fe", ec="#4fc3f7", lw=1.2))
poly(ax, [(2.0, 8.0), (8.0, 8.0), (6.0, 2.4), (4.0, 2.4)], "#ce93d8", lw=0, alpha=0.35)
rect(ax, 4.0, 2.0, 2.0, 0.4, "#c9d1d9", lw=0.6)
text(ax, 5.0, 1.2, "lens 시야 전체를 씀", size=9.5)
ax = axs[1]
ax.set_title("scanner: 좁은 slit으로 훑으며 노광", fontsize=11)
rect(ax, 1.5, 8.0, 7.0, 0.4, "#e3f2fd", lw=0.6)
arrow(ax, 7.0, 9.0, 3.0, 9.0, color="blue", lw=1.4)
text(ax, 5.0, 9.45, "mask 이동", size=9, color=C["blue"])
ax.add_patch(Ellipse((5.0, 5.4), 7.0, 1.2, fc="#e1f5fe", ec="#4fc3f7", lw=1.2))
poly(ax, [(4.4, 8.0), (5.6, 8.0), (5.15, 2.4), (4.85, 2.4)], "#ce93d8", lw=0, alpha=0.6)
rect(ax, 2.0, 2.0, 6.0, 0.4, "#c9d1d9", lw=0.6)
arrow(ax, 4.0, 1.4, 6.0, 1.4, color="red", lw=1.4)
text(ax, 5.0, 0.8, "wafer는 반대로 (1/4 속도)", size=9, color=C["red"])
text(ax, 9.9, 6.9, "lens 가운데 좁은\n부분만 씀 → 수차 작음", size=9, ha="right")
ax = axs[2]
ax.set_title("wafer 위 shot 배치 (예)", fontsize=11)
wafer_top(ax, 5.0, 5.0, 4.4, c="#dfe6ec")
sw, sh = 1.3, 1.65
for i in range(-4, 4):
    for j in range(-3, 3):
        x0, y0 = 5.0 + i * sw, 5.0 + j * sh
        cs = [(x0, y0), (x0 + sw, y0), (x0, y0 + sh), (x0 + sw, y0 + sh)]
        if sum(np.hypot(cx - 5, cy - 5) < 4.3 for cx, cy in cs) >= 3:
            rect(ax, x0, y0, sw, sh, "none", ec=C["blue"], lw=0.8, z=4)
text(ax, 5.0, 0.0, "shot 하나 최대 26 × 33 mm (chip 여러 개)", size=9)
plt.tight_layout()
save(f, P, "stepper_scanner")

# 4. 광원 파장 변천
data = [("g-line", 436, 1982), ("i-line", 365, 1990), ("KrF", 248, 1996), ("ArF", 193, 2002),
        ("ArF 액침", 134, 2007), ("EUV", 13.5, 2019)]
f, ax = plot_ax(7.6, 4.2)
xs = [d[2] for d in data]
ys = [d[1] for d in data]
ax.step(xs + [2026], ys + [ys[-1]], where="post", color="#999999", lw=1.0)
ax.scatter(xs, ys, color=PAL[:6], s=70, zorder=5)
for (n, l, y), c in zip(data, PAL):
    lab = f"{n}\n{l:g} nm" if n != "ArF 액침" else "ArF 액침\n193 nm (물 속 134 nm)"
    ax.text(y + 0.6, l * 1.12, lab, fontsize=9, color=c)
ax.set_yscale("log")
ax.set_ylim(8, 800)
ax.set_xlim(1979, 2027)
ax.set_xlabel("양산에 쓰이기 시작한 시기 (대략)")
ax.set_ylabel("파장 (nm)")
ax.set_title("노광 파장 변천", loc="left")
save(f, P, "wavelength")

# 5. overlay
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6))
canvas(0, 0, (0, 10), (0, 10), ax=ax1)
ax1.set_title("box-in-box mark", fontsize=11)
rect(ax1, 1.5, 1.5, 7.0, 7.0, "none", ec="#333333", lw=6)
rect(ax1, 3.7, 3.3, 3.0, 3.0, "none", ec=C["red"], lw=6)
text(ax1, 5.0, 9.3, "바깥: 아래층에서 만든 mark", size=9.5)
text(ax1, 5.2, 4.8, "안쪽: 지금\n찍은 PR mark", size=9.2, color=C["red"])
ax1.plot([5.0, 5.2], [5.0, 4.8], alpha=0)
arrow(ax1, 5.0, 0.8, 5.2, 0.8, color="blue", lw=1.0)
text(ax1, 5.0, 0.3, "가운데끼리 어긋난 만큼이 overlay 오차 (Δx, Δy)", size=9)
canvas(0, 0, (-5.5, 5.5), (-5.5, 5.5), ax=ax2)
ax2.set_title("wafer 전체 overlay 지도 (예: 회전 + 확대 오차)", fontsize=11)
wafer_top(ax2, 0, 0, 5.0, c="#f0f3f6")
for x in np.arange(-4, 4.1, 1.33):
    for y in np.arange(-4, 4.1, 1.33):
        if np.hypot(x, y) < 4.5:
            dx = -0.12 * y + 0.08 * x
            dy = 0.12 * x + 0.08 * y
            arrow(ax2, x, y, x + dx * 3, y + dy * 3, color="red", lw=1.0, ms=7)
plt.tight_layout()
save(f, P, "overlay")
