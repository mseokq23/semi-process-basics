import numpy as np
from common import *
from cmos import conformal

P = 23

# 1. PECVD chamber
f, ax = canvas(8.4, 5.4, (0, 16), (0, 10.2))
rect(ax, 0.8, 0.8, 14.4, 8.4, "#fafafa", lw=1.2)
rect(ax, 2.5, 7.0, 11.0, 0.7, "#b0bec5", lw=0.8)
for x in np.arange(3.0, 13.2, 0.6):
    line(ax, [x, x], [7.0, 6.6], color="#78909c", lw=1.0)
text(ax, 8.0, 7.35, "showerhead (gas 분사 + RF 전극)", size=9.5)
arrow(ax, 8.0, 9.9, 8.0, 7.8, color="blue", lw=1.4)
text(ax, 8.3, 9.5, "SiH₄ + NH₃ / N₂O, TEOS + O₂ ...", size=9, ha="left", color=C["blue"])
ax.add_patch(Ellipse((8.0, 4.9), 11.0, 2.6, fc="#e1bee7", ec="none", alpha=0.85, zorder=3))
text(ax, 8.0, 4.9, "plasma: 낮은 온도에서도 전구체를 분해", size=9.5, z=21)
rect(ax, 3.0, 2.4, 10.0, 0.9, "#ef9a9a", lw=0.8)
rect(ax, 4.0, 3.3, 8.0, 0.2, "si", lw=0.5)
text(ax, 8.0, 2.85, "heater 받침대 (200 ~ 400 °C)", size=9.5)
rect(ax, 0.0, 7.1, 1.6, 0.6, "#fff3e0", lw=0.6)
text(ax, 0.8, 7.4, "RF", size=9)
arrow(ax, 15.2, 1.6, 16.0, 1.6, lw=1.2)
text(ax, 15.9, 2.1, "배기", size=9, ha="right")
save(f, P, "pecvd_chamber")

# 2. gap fill이 막히는 과정
tt = ["① 증착 시작", "② 입구 모서리가 더 빨리 두꺼워짐", "③ 입구가 먼저 맞붙음", "④ 안에 빈 공간 (void)"]
f, axs = panels(4, 4, 3.0, 3.2, (0, 10), (0, 6.8), titles=tt, size=9.8)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "si", lw=0.6)
    rect(ax, 0.3, 1.1, 3.6, 4.0, "poly", lw=0.6)
    rect(ax, 6.1, 1.1, 3.6, 4.0, "poly", lw=0.6)
    t = [0.3, 0.6, 0.9, 1.3][k]
    ov = [0.05, 0.35, 1.05, 1.05][k]
    pts = [(0.3, 5.1), (3.9, 5.1), (3.9, 1.1), (6.1, 1.1), (6.1, 5.1), (9.7, 5.1), (9.7, 5.1 + t + 0.3),
           (6.1 - ov, 5.1 + t + 0.3), (6.1 - ov, 4.7), (6.1 - t * 0.55, 3.0), (6.1 - t * 0.5, 1.1 + t * 0.5),
           (3.9 + t * 0.5, 1.1 + t * 0.5), (3.9 + t * 0.55, 3.0), (3.9 + ov, 4.7), (3.9 + ov, 5.1 + t + 0.3),
           (0.3, 5.1 + t + 0.3)]
    poly(ax, pts, "ox", lw=0.6, z=5)
    if k == 3:
        rect(ax, 0.3, 5.1, 9.4, 1.6, "ox", lw=0.6, z=6)
        ax.add_patch(Ellipse((5.0, 3.0), 0.9, 2.6, fc="white", ec="#555555", lw=0.8, zorder=7))
save(f, P, "gapfill_steps")

# 3. HDP-CVD
tt = ["증착 + 동시에 sputter 식각", "모서리가 깎여서 입구가 안 막힘", "바닥부터 차오름 (bottom-up)"]
f, axs = panels(3, 3, 3.6, 3.6, (0, 10), (-0.9, 7.0), titles=tt, size=10.2)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "si", lw=0.6)
    rect(ax, 0.3, 1.1, 3.6, 4.0, "poly", lw=0.6)
    rect(ax, 6.1, 1.1, 3.6, 4.0, "poly", lw=0.6)
    h = [0.6, 1.8, 3.6][k]
    rect(ax, 3.9, 1.1, 2.2, h, "ox", lw=0.6, z=4)
    top = 5.1 + [0.5, 1.0, 1.4][k]
    for x0, x1, sgn in [(0.3, 3.9, 1), (6.1, 9.7, -1)]:
        edge = x1 if sgn == 1 else x0
        cap = top - 5.1
        if sgn == 1:
            pts = [(x0, 5.1), (edge, 5.1), (edge, 5.1 + 0.05), (edge - cap, top), (x0, top)]
        else:
            pts = [(x1, 5.1), (edge, 5.1), (edge, 5.1 + 0.05), (edge + cap, top), (x1, top)]
        poly(ax, pts, "ox", lw=0.6, z=4)
    if k == 0:
        for x in (2.0, 5.0, 8.0):
            arrow(ax, x, 6.9, x, 6.0 if x != 5.0 else 1.9, color="red", lw=1.0, ms=7)
        text(ax, 7.6, 6.65, "Ar⁺", size=9, color=C["red"])
text(axs[1], 5.0, -0.45, "45° 근처 경사면이 가장 잘 깎임", size=9)
save(f, P, "hdp")

# 4. 증착-식각-증착
tt = ["① 1차 증착 (입구가 좁아짐)", "② 식각으로 입구 넓히기", "③ 2차 증착 → 채움 완료"]
f, axs = panels(3, 3, 3.6, 3.2, (0, 10), (0, 6.8), titles=tt, size=10.2)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "si", lw=0.6)
    rect(ax, 0.3, 1.1, 3.6, 4.0, "poly", lw=0.6)
    rect(ax, 6.1, 1.1, 3.6, 4.0, "poly", lw=0.6)
    if k == 0:
        poly(ax, [(0.3, 5.1), (3.9, 5.1), (3.9, 1.1), (6.1, 1.1), (6.1, 5.1), (9.7, 5.1), (9.7, 5.9), (5.75, 5.9),
                  (5.45, 5.4), (5.6, 1.5), (4.4, 1.5), (4.55, 5.4), (4.25, 5.9), (0.3, 5.9)], "ox", lw=0.6, z=5)
    elif k == 1:
        poly(ax, [(0.3, 5.1), (3.9, 5.1), (3.9, 1.1), (6.1, 1.1), (6.1, 5.1), (9.7, 5.1), (9.7, 5.5), (6.4, 5.5),
                  (5.6, 4.6), (5.62, 1.5), (4.38, 1.5), (4.4, 4.6), (3.6, 5.5), (0.3, 5.5)], "ox", lw=0.6, z=5)
        for x in (4.4, 5.0, 5.6):
            arrow(ax, x, 6.7, x, 5.6, color="#555555", lw=1.0, ms=7)
    else:
        poly(ax, [(0.3, 5.1), (3.9, 5.1), (3.9, 1.1), (6.1, 1.1), (6.1, 5.1), (9.7, 5.1), (9.7, 6.3), (0.3, 6.3)],
             "ox", lw=0.6, z=5)
save(f, P, "dep_etch_dep")

# 5. 유동성 막 (FCVD, SOD)
tt = ["액체처럼 흘러 들어가서 좁은 틈을 채움", "경화(열처리)해서 단단한 SiO₂로"]
f, axs = panels(2, 2, 4.8, 3.2, (0, 12), (0, 7), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 11.4, 0.8, "si", lw=0.6)
    for x0 in (0.3, 3.3, 6.3, 9.3):
        rect(ax, x0, 1.1, 2.0, 4.0, "si", lw=0.6)
    xs = np.linspace(0.3, 11.7, 200)
    top = 5.6 + (0.25 * np.sin(xs * 2.2) if k == 0 else 0)
    ax.fill_between(xs, 1.1, top, color="#ce93d8" if k == 0 else C["ox"], zorder=1, ec="#555555", lw=0.6)
    for x0 in (0.3, 3.3, 6.3, 9.3):
        rect(ax, x0, 1.1, 2.0, 4.0, "si", lw=0.6, z=3)
    if k == 1:
        for x in (2.0, 6.0, 10.0):
            xs2 = np.linspace(0, 0.5, 20)
            ax.plot(x + 0.15 * np.sin(xs2 * 20), 6.0 + xs2 * 1.5, color=C["red"], lw=1.0, zorder=8)
save(f, P, "flowable")
