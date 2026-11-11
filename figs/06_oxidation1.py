import numpy as np
from common import *

P = 6

# 1. 산화막이 하는 일
tt = ["① 게이트 절연막", "② 소자 분리 (STI)", "③ 이온주입·확산 마스크", "④ 패드 산화막 (응력 완충)",
      "⑤ 스크린 산화막", "⑥ 희생 산화막 (손상층 제거)"]
f, axs = panels(6, 3, 4.0, 2.6, (0, 10), (0, 6.2), titles=tt, size=10.5)
a = axs
for ax in a:
    rect(ax, 0.3, 0.4, 9.4, 2.6, "si", lw=0.8)
# ①
rect(a[0], 1.0, 2.0, 2.0, 1.0, "np", lw=0.5)
rect(a[0], 7.0, 2.0, 2.0, 1.0, "np", lw=0.5)
rect(a[0], 3.0, 3.0, 4.0, 0.25, "ox")
rect(a[0], 3.0, 3.25, 4.0, 1.3, "poly")
text(a[0], 5.0, 3.9, "게이트", size=9)
arrow(a[0], 8.6, 4.7, 6.6, 3.15, lw=0.8, ms=7)
text(a[0], 8.6, 5.0, "얇은 SiO₂", size=9)
# ②
rect(a[1], 4.0, 1.5, 2.0, 1.5, "ox")
text(a[1], 2.1, 2.3, "소자 A", size=9)
text(a[1], 7.9, 2.3, "소자 B", size=9)
text(a[1], 5.0, 2.25, "SiO₂", size=9)
# ③
rect(a[2], 0.3, 3.0, 3.8, 1.2, "ox")
rect(a[2], 5.9, 3.0, 3.8, 1.2, "ox")
rect(a[2], 4.1, 2.2, 1.8, 0.8, "np", lw=0.5)
for x in np.arange(0.8, 9.6, 0.8):
    yb = 3.05 if 4.1 < x < 5.9 else 4.25
    arrow(a[2], x, 5.9, x, yb, color="red", lw=1.0, ms=7)
text(a[2], 2.2, 3.6, "두꺼운 SiO₂", size=8.6)
# ④
rect(a[3], 0.3, 3.0, 9.4, 0.3, "ox")
rect(a[3], 0.3, 3.3, 9.4, 1.0, "nit")
text(a[3], 5.0, 3.8, "Si₃N₄", size=9)
arrow(a[3], 8.8, 5.3, 7.5, 3.15, lw=0.8, ms=7)
text(a[3], 8.8, 5.6, "얇은 SiO₂", size=8.6)
# ⑤
rect(a[4], 0.3, 3.0, 9.4, 0.3, "ox")
rect(a[4], 0.3, 2.2, 9.4, 0.6, "np", lw=0.4, alpha=0.6)
for x in np.arange(0.8, 9.6, 0.8):
    arrow(a[4], x, 5.9, x, 3.35, color="red", lw=1.0, ms=7)
text(a[4], 5.0, 1.3, "채널링, 표면 오염 줄이기", size=8.6)
# ⑥
rect(a[5], 0.3, 2.75, 9.4, 0.5, "ox", alpha=0.85)
rect(a[5], 0.3, 2.75, 9.4, 0.25, "#e57373", lw=0, alpha=0.5, z=3)
text(a[5], 5.0, 4.6, "키운 다음 HF로 벗겨냄", size=9)
text(a[5], 5.0, 1.3, "손상된 표면이 산화막과 같이 없어짐", size=8.6)
plt.tight_layout()
save(f, P, "oxide_roles")

# 2. 건식 / 습식
f, axs = panels(2, 2, 6.0, 3.8, (0, 10), (0, 7.2),
                titles=["건식 산화: Si + O₂ → SiO₂", "습식 산화: Si + 2H₂O → SiO₂ + 2H₂"], size=11)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 2.4, "si", lw=0.8)
    th = 0.6 if k == 0 else 1.5
    rect(ax, 0.3, 2.7, 9.4, th, "ox", lw=0.8)
    text(ax, 5.0, 1.5, "Si", size=10)
    text(ax, 5.0, 2.7 + th / 2, "SiO₂", size=10)
    rng = np.random.default_rng(k + 1)
    for _ in range(7):
        x, y = rng.uniform(0.8, 9.2), rng.uniform(4.8, 6.6)
        if k == 0:
            circ(ax, x - 0.17, y, 0.17, "#e57373", lw=0.5)
            circ(ax, x + 0.17, y, 0.17, "#e57373", lw=0.5)
        else:
            circ(ax, x, y, 0.2, "#e57373", lw=0.5)
            circ(ax, x - 0.28, y - 0.2, 0.12, "#ffffff", lw=0.5)
            circ(ax, x + 0.28, y - 0.2, 0.12, "#ffffff", lw=0.5)
    note = "느림, 막이 치밀함 → 얇고 중요한 막\n(게이트 산화막)" if k == 0 else "빠름 (같은 온도에서 수 배~10배 이상)\n→ 두꺼운 막 (예전 필드 산화막)"
    text(ax, 5.0, 4.05 if k == 0 else 4.95, "O₂" if k == 0 else "H₂O", size=10, color=C["red"])
    text(ax, 5.0, -0.25, note, size=9.3, va="top")
f.subplots_adjust(bottom=0.2)
save(f, P, "dry_wet")

# 3. 실리콘 소모
f, axs = panels(2, 2, 4.6, 3.9, (0, 10), (-0.5, 8.0), titles=["산화 전", "산화 후"], size=11)
for k, ax in enumerate(axs):
    line(ax, [0, 10], [4.0, 4.0], color="#555555", lw=0.8, ls="--", z=12)
text(axs[0], 9.9, 4.3, "원래 표면", size=9, ha="right", color="#555555")
text(axs[1], 5.0, 3.55, "원래 표면 위치", size=9, color="#555555")
rect(axs[0], 1.0, 0.0, 8.0, 4.0, "si", lw=0.8)
rect(axs[1], 1.0, 0.0, 8.0, 2.24, "si", lw=0.8)
rect(axs[1], 1.0, 2.24, 8.0, 4.0, "ox", lw=0.8)
vdim(axs[1], 9.3, 2.24, 6.24, "x", size=10)
vdim(axs[1], 0.6, 2.24, 4.0, "0.44x", size=9.2, side="left")
vdim(axs[1], 0.6, 4.0, 6.24, "0.56x", size=9.2, side="left")
text(axs[1], 5.0, 5.2, "SiO₂ (두께 x)", size=10)
text(axs[1], 5.0, 1.1, "Si", size=10)
text(axs[0], 5.0, 2.0, "Si", size=10)
save(f, P, "si_consumption")

# 4. 수직 퍼니스
f, ax = canvas(6.4, 8.0, (0, 12), (0, 15))
rect(ax, 1.6, 2.6, 8.8, 10.4, "#f4f4f4", lw=1.0)
for y in np.arange(3.2, 12.6, 0.5):
    line(ax, [2.0, 2.6], [y, y], color=C["red"], lw=1.6)
    line(ax, [9.4, 10.0], [y, y], color=C["red"], lw=1.6)
for k, y0 in enumerate([3.0, 6.2, 9.4]):
    text(ax, 1.4, y0 + 1.6, f"구역 {3 - k}", size=8.5, ha="right", color=C["red"])
ax.add_patch(FancyBboxPatch((3.0, 2.8), 6.0, 10.0, boxstyle="round,pad=0,rounding_size=1.5",
                            fc="#eef7fc", ec="#6a9fc0", lw=1.4, zorder=2))
rect(ax, 4.4, 3.2, 0.25, 8.6, "#bdbdbd", lw=0.5, z=3)
rect(ax, 7.35, 3.2, 0.25, 8.6, "#bdbdbd", lw=0.5, z=3)
for y in np.arange(3.6, 11.6, 0.32):
    line(ax, [4.2, 7.8], [y, y], color="#7f8c99", lw=1.6, z=4)
rect(ax, 3.4, 1.6, 5.2, 1.2, "#9e9e9e", lw=0.8)
text(ax, 6.0, 2.2, "보트 받침 / 승강기", size=8.5, color="white")
arrow(ax, 6.0, 14.6, 6.0, 12.9, color="blue", lw=1.6)
text(ax, 6.2, 14.4, "O₂ / H₂ + O₂ / N₂", size=9.5, ha="left", color=C["blue"])
arrow(ax, 9.2, 3.3, 11.6, 3.3, color="#555555", lw=1.2)
text(ax, 11.6, 3.8, "배기", size=9, ha="right")
text(ax, 6.0, 7.6, "웨이퍼 100장 이상\n(보트에 가로로 쌓음)", size=9.5, box="white")
text(ax, 11.6, 9.0, "히터\n800~1200 °C", size=9, ha="right", color=C["red"])
text(ax, 6.0, 0.8, "석영 튜브 안에서 한 번에 산화", size=9.5)
save(f, P, "furnace")

# 5. 산화가 일어나는 곳 (Deal-Grove 그림 준비)
f, ax = canvas(9.6, 5.0, (0, 16), (-1.2, 8.0))
rect(ax, 0, 0, 5.0, 7.0, "#ffffff", lw=0)
rect(ax, 5.0, 0, 4.0, 7.0, "ox", lw=0.8)
rect(ax, 9.0, 0, 7.0, 7.0, "si", lw=0.8)
text(ax, 2.5, 7.4, "기체", size=11, weight="bold")
text(ax, 7.0, 7.4, "SiO₂", size=11, weight="bold")
text(ax, 12.5, 7.4, "Si", size=11, weight="bold")
xs = [0.3, 4.3, 5.0, 9.0]
ys = [5.8, 5.0, 4.6, 1.2]
ax.plot([0.3, 3.8, 5.0], [5.8, 5.8, 5.0], color=C["red"], lw=2.2, zorder=8)
ax.plot([5.0, 9.0], [4.5, 1.2], color=C["red"], lw=2.2, zorder=8)
text(ax, 1.4, 6.25, "$C_G$", size=11, color=C["red"])
text(ax, 4.55, 4.6, "$C_S$", size=11, color=C["red"])
text(ax, 5.25, 5.0, "$C_O$", size=11, color=C["red"], ha="left")
text(ax, 8.75, 1.75, "$C_I$", size=11, color=C["red"], ha="right")
arrow(ax, 2.2, 3.2, 4.8, 3.2, color="blue", lw=1.6)
text(ax, 3.5, 2.7, "F₁ 기체 → 표면", size=9.5, color=C["blue"])
arrow(ax, 5.3, 6.1, 8.7, 6.1, color="blue", lw=1.6)
text(ax, 7.0, 6.55, "F₂ 산화막 통과 (확산)", size=9.5, color=C["blue"])
arrow(ax, 9.0, 3.6, 10.4, 3.6, color="green", lw=1.6)
text(ax, 11.5, 4.3, "F₃ 계면에서 Si와 반응\n(새 SiO₂가 여기서 생김)", size=9.5, color=C["green"])
text(ax, 8.0, -0.7, "산화제 농도 (빨간 선): 산화막을 지나면서 줄어듦", size=9.5, color="#555555")
save(f, P, "oxidation_mechanism")
