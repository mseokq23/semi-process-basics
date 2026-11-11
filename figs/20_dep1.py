import numpy as np
from common import *
from cmos import conformal

P = 20

# 1. 산화(성장) vs 증착
tt = ["산화: Si를 먹으면서 자람", "증착: 위에 쌓기만 함 (아래 재료 상관없음)"]
f, axs = panels(2, 2, 5.8, 3.0, (0, 12), (0, 6), titles=tt, size=11)
for k, ax in enumerate(axs):
    line(ax, [0.3, 11.7], [3.0, 3.0], color="#555555", lw=0.8, ls="--", z=12)
    if k == 0:
        rect(ax, 0.5, 0.5, 5.0, 2.5, "si", lw=0.6)
        text(ax, 3.0, 4.6, "전", size=10)
        rect(ax, 6.5, 0.5, 5.0, 1.9, "si", lw=0.6)
        rect(ax, 6.5, 2.4, 5.0, 1.35, "ox", lw=0.6)
        text(ax, 9.0, 4.6, "후", size=10)
    else:
        rect(ax, 0.5, 0.5, 5.0, 2.5, "si", lw=0.6)
        rect(ax, 2.0, 2.0, 2.0, 1.0, "ox", lw=0.6)
        text(ax, 3.0, 4.6, "전", size=10)
        rect(ax, 6.5, 0.5, 5.0, 2.5, "si", lw=0.6)
        rect(ax, 8.0, 2.0, 2.0, 1.0, "ox", lw=0.6)
        rect(ax, 6.5, 3.0, 5.0, 0.8, "nit", lw=0.6)
        text(ax, 9.0, 4.6, "후", size=10)
    arrow(ax, 5.6, 1.8, 6.4, 1.8, lw=1.2)
save(f, P, "growth_vs_dep")


# 2. 단차 피복성
def trench(ax, kind):
    rect(ax, 0.3, 0.3, 9.4, 1.0, "ox", lw=0.6)
    rect(ax, 0.3, 1.3, 3.2, 3.0, "ox", lw=0.6)
    rect(ax, 6.5, 1.3, 3.2, 3.0, "ox", lw=0.6)
    if kind == "conf":
        conformal(ax, [(0.3, 3.5, 4.3), (6.5, 9.7, 4.3)], 0.45, "al", base=1.3, x0=0.3, x1=9.7)
    elif kind == "poor":
        poly(ax, [(0.3, 4.3), (3.5, 4.3), (3.5, 1.3), (6.5, 1.3), (6.5, 4.3), (9.7, 4.3), (9.7, 4.9), (6.4, 4.9),
                  (6.32, 4.3), (6.42, 1.5), (3.58, 1.5), (3.68, 4.3), (3.6, 4.9), (0.3, 4.9)], "al", lw=0.6, z=6)
    elif kind == "over":
        poly(ax, [(0.3, 4.3), (3.5, 4.3), (3.5, 1.3), (6.5, 1.3), (6.5, 4.3), (9.7, 4.3), (9.7, 5.0), (6.6, 5.0),
                  (6.05, 4.6), (6.4, 4.2), (6.45, 1.45), (3.55, 1.45), (3.6, 4.2), (3.95, 4.6), (3.4, 5.0),
                  (0.3, 5.0)], "al", lw=0.6, z=6)


tt = ["좋음: 고르게 덮임 (conformal)", "나쁨: 측벽, 바닥이 얇음", "overhang: 입구가 먼저 두꺼워짐"]
f, axs = panels(3, 3, 3.8, 3.0, (0, 10), (0, 6.2), titles=tt, size=10.5)
for ax, k in zip(axs, ("conf", "poor", "over")):
    trench(ax, k)
ax = axs[0]
text(ax, 2.0, 5.4, "윗면 t_top", size=8.6)
text(ax, 5.0, 2.3, "바닥 t_bot", size=8.6)
text(ax, 5.0, 3.6, "측벽\nt_side", size=8.6)
plt.suptitle("단차 피복성 = 측벽(또는 바닥) 두께 / 윗면 두께", fontsize=11.5, y=1.03)
save(f, P, "step_coverage")

# 3. gap fill 불량
tt = ["void (빈 공간)", "seam (가운데 이음선)", "정상"]
f, axs = panels(3, 3, 3.6, 3.2, (0, 10), (0, 6.4), titles=tt, size=11)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "si", lw=0.6)
    for x0 in (0.3, 6.2):
        rect(ax, x0, 1.1, 3.5, 3.4, "poly", lw=0.6)
    rect(ax, 3.8, 1.1, 2.4, 0.0, "white", lw=0)
    poly(ax, [(0.3, 4.5), (3.8, 4.5), (3.8, 1.1), (6.2, 1.1), (6.2, 4.5), (9.7, 4.5), (9.7, 5.6), (0.3, 5.6)],
         "ox", lw=0.6, z=4)
    if k == 0:
        ax.add_patch(Ellipse((5.0, 2.6), 0.9, 2.4, fc="white", ec="#555555", lw=0.8, zorder=6))
    elif k == 1:
        line(ax, [5.0, 5.0], [1.3, 5.0], color="#555555", lw=1.0, ls=":", z=7)
save(f, P, "gapfill_defects")

# 4. 박막 응력
f, axs = panels(2, 2, 5.4, 3.0, (-6, 6), (-2.0, 2.4), titles=["인장 응력: 막이 줄어들려고 함 → 오목",
                                                               "압축 응력: 막이 늘어나려고 함 → 볼록"], size=10.5)
xs = np.linspace(-5, 5, 200)
for k, ax in enumerate(axs):
    s = 1 if k == 0 else -1
    y = s * 0.04 * xs ** 2
    ax.fill_between(xs, y - 0.6, y, color=C["si"], ec=EC, lw=0.6, zorder=2)
    ax.fill_between(xs, y, y + 0.25, color=C["nit"], ec=EC, lw=0.6, zorder=3)
    for sgn in (-1, 1):
        if k == 0:
            arrow(ax, sgn * 4.6, 1.75, sgn * 2.8, 1.75, color="red", lw=1.4)
        else:
            arrow(ax, sgn * 2.8, -1.4, sgn * 4.6, -1.4, color="red", lw=1.4)
text(axs[0], 0, -1.6, "(휘어짐은 과장해서 그림)", size=8.8, color="#666666")
save(f, P, "stress")

# 5. 박막 성장 mode
tt = ["층 단위 성장 (FM)", "섬 성장 (VW)", "층 + 섬 (SK)"]
f, axs = panels(3, 3, 3.6, 2.4, (0, 10), (0, 4.4), titles=tt, size=11)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.2, "si", lw=0.6)
    if k == 0:
        rect(ax, 0.3, 1.5, 9.4, 0.5, "al", lw=0.5)
        rect(ax, 0.3, 2.0, 9.4, 0.5, "al", lw=0.5)
        rect(ax, 0.3, 2.5, 5.0, 0.5, "al", lw=0.5)
    if k == 2:
        rect(ax, 0.3, 1.5, 9.4, 0.45, "al", lw=0.5)
    if k in (1, 2):
        base = 1.5 if k == 1 else 1.95
        for x in (1.6, 4.4, 7.6):
            th = np.linspace(0, np.pi, 30)
            poly(ax, list(zip(x + 1.0 * np.cos(th), base + 1.1 * np.sin(th))), "al", lw=0.5)
save(f, P, "growth_modes")


# 6. 부착 계수와 피복성
def bounce(ax, sticky):
    rect(ax, 0.3, 0.3, 9.4, 1.0, "ox", lw=0.6)
    rect(ax, 0.3, 1.3, 3.0, 4.2, "ox", lw=0.6)
    rect(ax, 6.7, 1.3, 3.0, 4.2, "ox", lw=0.6)
    if sticky:
        paths = [[(4.0, 7.6), (3.4, 5.6)], [(5.6, 7.6), (6.7, 5.0)], [(5.0, 7.6), (4.4, 3.8), (3.4, 3.2)]]
        poly(ax, [(0.3, 5.5), (3.3, 5.5), (3.3, 4.6), (3.75, 5.1), (3.55, 5.9), (0.3, 5.9)], "al", lw=0.5, z=6)
        poly(ax, [(9.7, 5.5), (6.7, 5.5), (6.7, 4.6), (6.25, 5.1), (6.45, 5.9), (9.7, 5.9)], "al", lw=0.5, z=6)
    else:
        paths = [[(4.0, 7.6), (6.6, 4.2), (3.4, 2.4), (5.2, 1.4)], [(5.8, 7.6), (3.4, 4.4), (6.6, 2.0)]]
        conformal(ax, [(0.3, 3.3, 5.5), (6.7, 9.7, 5.5)], 0.25, "al", base=1.3, x0=0.3, x1=9.7)
    for pth in paths:
        xs_, ys_ = zip(*pth)
        ax.plot(xs_, ys_, color=C["red"], lw=1.1, zorder=8)
        circ(ax, xs_[-1], ys_[-1], 0.14, "#e57373", lw=0.3, z=9)


f, axs = panels(2, 2, 4.6, 3.8, (0, 10), (0, 8), titles=["부착 계수 큼: 처음 닿은 곳(입구)에 붙음",
                                                       "부착 계수 작음: 튕기면서 안쪽까지 들어감"], size=10.5)
bounce(axs[0], True)
bounce(axs[1], False)
save(f, P, "sticking")

# 7. PVD / CVD / ALD 피복성 비교
tt = ["PVD (sputter)", "CVD", "ALD"]
f, axs = panels(3, 3, 3.4, 3.4, (0, 10), (0, 7.2), titles=tt, size=11)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "ox", lw=0.6)
    rect(ax, 0.3, 1.1, 3.7, 4.6, "ox", lw=0.6)
    rect(ax, 6.0, 1.1, 3.7, 4.6, "ox", lw=0.6)
    if k == 0:
        poly(ax, [(0.3, 5.7), (4.0, 5.7), (4.0, 1.1), (6.0, 1.1), (6.0, 5.7), (9.7, 5.7), (9.7, 6.4), (6.15, 6.4),
                  (5.6, 6.0), (5.92, 5.5), (5.95, 1.25), (4.05, 1.25), (4.08, 5.5), (4.4, 6.0), (3.85, 6.4),
                  (0.3, 6.4)], "tin", lw=0.5, z=6)
    elif k == 1:
        poly(ax, [(0.3, 5.7), (4.0, 5.7), (4.0, 1.1), (6.0, 1.1), (6.0, 5.7), (9.7, 5.7), (9.7, 6.3), (5.6, 6.3),
                  (5.65, 5.6), (5.75, 1.35), (4.25, 1.35), (4.35, 5.6), (4.4, 6.3), (0.3, 6.3)], "tin", lw=0.5, z=6)
    else:
        conformal(ax, [(0.3, 4.0, 5.7), (6.0, 9.7, 5.7)], 0.45, "tin", base=1.1, x0=0.3, x1=9.7)
save(f, P, "coverage_compare")
