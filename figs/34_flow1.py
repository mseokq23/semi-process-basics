import numpy as np
from common import *
import cmos

P = 34

# 1. 전체 흐름
phases = [("소자 분리\n(STI)", "7, 17, 23, 32편", "#e3f2fd"), ("well", "26 ~ 28편", "#fde2e2"),
          ("gate", "6, 22, 18편", "#fff3e0"), ("LDD, spacer", "26, 20, 18편", "#e8f5e9"),
          ("source / drain", "26 ~ 28편", "#fde2e2"), ("silicide", "29편", "#ede7f6"),
          ("contact", "23, 30, 32편", "#eceff1"), ("배선", "31, 32편", "#fbe9e7")]
f, ax = canvas(14.4, 3.0, (0, 40), (-1.8, 6.4))
for i, (s, ref, c) in enumerate(phases):
    x = 0.3 + i * 4.95
    box(ax, x, 1.4, 4.3, 3.0, s, fc=c, size=10, weight="bold")
    text(ax, x + 2.15, 0.6, ref, size=8.6, color="#555555")
    if i < len(phases) - 1:
        arrow(ax, x + 4.35, 2.9, x + 4.9, 2.9, lw=1.2, ms=9)
ax.plot([0.3, 19.9], [5.2, 5.2], color=C["blue"], lw=2.0)
text(ax, 10.1, 5.75, "34편: STI ~ gate", size=10, color=C["blue"], weight="bold")
ax.plot([15.15, 39.6], [-0.9, -0.9], color=C["red"], lw=2.0)
text(ax, 27.4, -1.45, "35편: LDD ~ 배선", size=10, color=C["red"], weight="bold")
save(f, P, "flow_overview")

# 2. 단계별 단면 (A: 16단계 → 4장)
for g in range(4):
    st = cmos.A[g * 4:(g + 1) * 4]
    f, axs = panels(4, 2, 6.3, 2.55, (-0.3, 24.3), (-5.0, 3.3), titles=[s for s, _ in st], size=10.5)
    for ax, (_, d) in zip(axs, st):
        cmos.draw(ax, d, lab=True, size=8.5)
    if g == 0:
        legend(axs[1], ["ox", "nit", "pr"], loc="upper right", ncol=3, size=8.5, bbox=(1.0, 1.0),
               names=dict(ox="SiO₂"))
    if g == 3:
        legend(axs[3], ["ox", "poly", "pw", "nw"], loc="upper right", ncol=4, size=8.0, bbox=(1.0, 1.0),
               names=dict(ox="SiO₂"))
    save(f, P, f"a{g + 1}")

# 3. layout (위에서 본 모습)
f, ax = canvas(10.5, 5.6, (-1.5, 25.5), (-2.4, 11.2))
rect(ax, 0, -0.6, 12, 10.2, "pw", lw=0.6, z=1)
rect(ax, 12, -0.6, 12, 10.2, "nw", lw=1.2, z=1, ls="--")
text(ax, 0.3, 9.25, "P-well", size=9, ha="left", color="#a33")
text(ax, 23.7, 9.25, "N-well (NWELL)", size=9, ha="right", color=C["blue"])
for a, b in cmos.ACT:
    rect(ax, a, 2.6, b - a, 3.8, "#c5e1a5", lw=0.9, z=2)
text(ax, 1.4, 6.0, "ACTIVE", size=8.5, ha="left", color="#33691e")
for gx0, gx1 in cmos.GATE:
    rect(ax, gx0, 0.9, gx1 - gx0, 6.6, "poly", lw=0.8, z=3, alpha=0.95)
rect(ax, 5.4, 0.3, 13.2, 0.9, "poly", lw=0.8, z=3, alpha=0.95)
text(ax, 6.0, 7.9, "POLY", size=8.5, color="#8d6e00")
for x in cmos.CT_X:
    rect(ax, x - 0.35, 4.15, 0.7, 0.7, "#212121", lw=0.4, z=5)
rect(ax, 11.65, 0.4, 0.7, 0.7, "#212121", lw=0.4, z=5)
M1C = "#d58f5a"
for xs_, ys_ in [((2.2, 3.8), (3.9, 9.9)), ((20.2, 21.8), (3.9, 9.9)), ((8.2, 15.8), (3.9, 5.1)),
                 ((11.4, 12.6), (5.1, 9.9)), ((11.4, 12.6), (-1.6, 1.3))]:
    rect(ax, xs_[0], ys_[0], xs_[1] - xs_[0], ys_[1] - ys_[0], M1C, lw=0.6, z=4, alpha=0.55)
text(ax, 3.0, 10.45, "GND", size=10, weight="bold")
text(ax, 21.0, 10.45, "VDD", size=10, weight="bold")
text(ax, 12.0, 10.45, "OUT", size=10, weight="bold")
text(ax, 12.0, -2.05, "IN", size=10, weight="bold")
ax.plot([-1.0, 25.0], [4.5, 4.5], color=C["red"], lw=1.3, ls="--", zorder=6)
text(ax, -1.2, 4.5, "A", size=11, color=C["red"], weight="bold", ha="right")
text(ax, 25.2, 4.5, "A'", size=11, color=C["red"], weight="bold", ha="left")
text(ax, 8.8, 2.0, "NMOS", size=9.5, weight="bold", z=22)
text(ax, 20.8, 2.0, "PMOS", size=9.5, weight="bold", z=22)
hs = [Rectangle((0, 0), 1, 1, fc=c, ec="#333333", lw=0.6, alpha=a) for c, a in
      [(C["nw"], 1), ("#c5e1a5", 1), (C["poly"], 1), ("#212121", 1), (M1C, 0.55)]]
ax.legend(hs, ["NWELL", "ACTIVE", "POLY", "CONTACT", "METAL1"], loc="upper center", ncol=5, fontsize=9,
          bbox_to_anchor=(0.5, 0.0), handlelength=1.2)
save(f, P, "layout_top")
