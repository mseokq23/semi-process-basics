import numpy as np
from common import *

P = 4

# 1. 모래 → wafer
f, ax = canvas(14, 3.4, (0, 28.4), (-2.6, 3.6))
items = [("규사\n(SiO₂)", "#f3e6c8"), ("MG-Si\n순도 98~99 %", "#e3e3e3"), ("TCS\n(SiHCl₃, 액체)", "#e8f1f8"),
         ("polysilicon\n순도 9N~11N", "#d5dbe1"), ("단결정\ningot", "#c9d1d9"), ("wafer", "#c9d1d9")]
steps = ["arc furnace, 탄소로 환원\nSiO₂ + 2C → Si + 2CO", "HCl과 반응\nSi + 3HCl → SiHCl₃ + H₂",
         "증류 → H₂로 환원\n(Siemens 공정)", "CZ 단결정 성장\n(이번 편)", "자르고 갈기\n(5편)"]
w, gap = 3.0, 2.08
for i, (s, c) in enumerate(items):
    x = 0.2 + i * (w + gap)
    box(ax, x, 0.6, w, 2.2, s, fc=c, size=10)
    if i < len(steps):
        arrow(ax, x + w + 0.08, 1.7, x + w + gap - 0.08, 1.7, lw=1.3, ms=11)
        text(ax, x + w + gap / 2, -0.75, steps[i], size=8.6, color="#444444")
save(f, P, "sand_to_wafer")

# 2. CZ 장비
f, ax = canvas(9.2, 8.6, (-3.6, 13.4), (0, 14.6))
rect(ax, 1.0, 0.6, 11.0, 8.6, "#f4f4f4", lw=1.2)                 # chamber
rect(ax, 4.6, 9.2, 3.8, 4.6, "#f4f4f4", lw=1.2)                  # 위쪽 인상 chamber
rect(ax, 1.5, 1.2, 1.0, 7.2, "#bdbdbd", lw=0.6)                  # 단열재
rect(ax, 10.5, 1.2, 1.0, 7.2, "#bdbdbd", lw=0.6)
for x in (2.7, 9.7):
    rect(ax, x, 2.2, 0.55, 3.6, "#e57373", lw=0.6)                # heater
poly(ax, [(3.5, 5.6), (3.5, 2.6), (4.0, 2.0), (9.0, 2.0), (9.5, 2.6), (9.5, 5.6), (9.25, 5.6),
          (9.25, 2.75), (8.85, 2.25), (4.15, 2.25), (3.75, 2.75), (3.75, 5.6)], "#9e9e9e", lw=0.6)
poly(ax, [(3.75, 5.6), (3.75, 2.75), (4.15, 2.25), (8.85, 2.25), (9.25, 2.75), (9.25, 5.6), (9.0, 5.6),
          (9.0, 2.9), (8.7, 2.5), (4.3, 2.5), (4.0, 2.9), (4.0, 5.6)], "#eceff1", lw=0.6)
poly(ax, [(4.0, 4.6), (4.0, 2.9), (4.3, 2.5), (8.7, 2.5), (9.0, 2.9), (9.0, 4.6)], "#f4b183", lw=0.6)
rect(ax, 6.2, 0.6, 0.6, 1.4, "#9e9e9e", lw=0.6)                 # 도가니 축
# ingot
poly(ax, [(5.4, 4.6), (5.4, 7.6), (6.25, 8.4), (6.4, 8.9), (6.6, 8.9), (6.75, 8.4), (7.6, 7.6), (7.6, 4.6)],
     "#c9d1d9", lw=0.8, z=3)
rect(ax, 6.35, 8.9, 0.3, 0.6, "#a0aab4", lw=0.6, z=3)            # 종자
line(ax, [6.5, 6.5], [9.5, 13.4], lw=1.4)
ax.add_patch(Arc((6.5, 12.6), 1.6, 0.5, theta1=200, theta2=340, color=C["blue"], lw=1.4, zorder=8))
arrow(ax, 7.2, 12.42, 7.33, 12.5, color="blue", ms=9)
arrow(ax, 8.9, 10.6, 8.9, 12.4, color="blue", lw=1.4)
text(ax, 9.1, 11.5, "천천히\n끌어올림", size=9, ha="left", color=C["blue"])
ax.add_patch(Arc((6.5, 1.2), 1.8, 0.5, theta1=200, theta2=340, color=C["red"], lw=1.4, zorder=8))
arrow(ax, 5.81, 1.08, 5.68, 1.15, color="red", ms=9)
text(ax, 4.4, 0.25, "도가니는 반대로 회전", size=8.5, color=C["red"])
arrow(ax, 4.0, 14.2, 5.6, 13.0, color="#555555", lw=1.0)
text(ax, 3.9, 14.25, "Ar gas", size=9, ha="right")
arrow(ax, 12.0, 1.0, 12.9, 1.0, color="#555555", lw=1.0)
text(ax, 12.9, 1.45, "배기", size=8.5, ha="right")
labels = [((7.7, 6.4), (10.2, 7.3), "단결정 ingot"), ((6.5, 9.2), (9.6, 9.9), "종자 (seed)"),
          ((7.8, 3.6), (11.0, 4.5), "Si 융액\n(1414 °C 이상)")]
for (px, py), (tx, ty), s in labels:
    text(ax, tx, ty, s, size=9, ha="left", box="white")
    arrow(ax, tx - 0.1, ty - 0.1, px, py, lw=0.7, ms=6, color="#555555")
for (px, py), ty, s in [((2.0, 7.6), 7.6, "단열재"), ((2.95, 4.9), 4.9, "흑연 heater"), ((3.6, 3.2), 3.2, "석영 도가니\n(흑연 받침)")]:
    text(ax, -3.4, ty, s, size=9, ha="left")
    arrow(ax, -1.2, ty, px, py, lw=0.7, ms=6, color="#555555")
save(f, P, "cz_puller")


# 3. CZ 성장 단계
def ingot(ax, kind):
    rect(ax, 0, 0, 10, 1.4, "#f4b183", lw=0.6)
    if kind == 0:
        rect(ax, 4.85, 1.4, 0.3, 3.8, "#a0aab4", lw=0.6)
    elif kind == 1:
        rect(ax, 4.85, 3.2, 0.3, 2.0, "#a0aab4", lw=0.6)
        rect(ax, 4.92, 1.4, 0.16, 1.8, "#c9d1d9", lw=0.6)
    elif kind == 2:
        rect(ax, 4.85, 5.0, 0.3, 1.4, "#a0aab4", lw=0.6)
        poly(ax, [(4.92, 5.0), (4.92, 3.4), (3.0, 1.4), (7.0, 1.4), (5.08, 3.4), (5.08, 5.0)], "#c9d1d9", lw=0.6)
    elif kind == 3:
        rect(ax, 4.85, 7.2, 0.3, 1.0, "#a0aab4", lw=0.6)
        poly(ax, [(4.92, 7.2), (4.92, 6.2), (3.0, 4.6), (3.0, 1.4), (7.0, 1.4), (7.0, 4.6), (5.08, 6.2),
                  (5.08, 7.2)], "#c9d1d9", lw=0.6)
    elif kind == 4:
        rect(ax, 4.85, 8.1, 0.3, 0.6, "#a0aab4", lw=0.6)
        poly(ax, [(4.92, 8.1), (4.92, 7.4), (3.0, 6.0), (3.0, 3.2), (5.0, 2.0), (7.0, 3.2), (7.0, 6.0),
                  (5.08, 7.4), (5.08, 8.1)], "#c9d1d9", lw=0.6)


tt = ["① 담그기 (dipping)", "② necking: 가늘게 뽑아\n결함(전위) 빼내기", "③ shoulder: 지름 키우기",
      "④ body: 일정한 지름으로\n길게 (wafer가 되는 부분)", "⑤ tail: 지름 줄이며\n융액에서 떼기"]
f, axs = panels(5, 5, 3.0, 4.0, (0, 10), (0, 9), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    ingot(ax, k)
save(f, P, "cz_stages")

# 4. 편석 (Scheil)
fs = np.linspace(0, 0.95, 300)
f, ax = plot_ax(6.6, 4.2)
for (el, k0), c in zip([("B", 0.8), ("P", 0.35), ("As", 0.3), ("Sb", 0.023)], PAL):
    ax.plot(fs, k0 * (1 - fs) ** (k0 - 1), color=c, lw=2, label=f"{el} (k₀ = {k0})")
ax.set_yscale("log")
ax.set_xlabel("굳은 비율 f (0 = ingot 위쪽, 1 = 아래쪽)")
ax.set_ylabel("결정 속 농도 / 처음 융액 농도")
ax.legend(fontsize=9.5)
ax.set_title("편석: 아래로 갈수록 dopant 농도가 올라감", loc="left")
save(f, P, "segregation")

# 5. FZ
f, ax = canvas(4.2, 5.6, (0, 8), (0, 11))
rect(ax, 2.6, 6.4, 2.8, 4.2, "#d5dbe1", lw=0.8)
text(ax, 4.0, 8.6, "polysilicon\n막대", size=9.5)
poly(ax, [(2.6, 6.4), (2.9, 5.6), (5.1, 5.6), (5.4, 6.4)], "#f4b183", lw=0.6)
poly(ax, [(2.9, 5.6), (2.7, 4.9), (5.3, 4.9), (5.1, 5.6)], "#f4b183", lw=0.6)
rect(ax, 2.7, 1.6, 2.6, 3.3, "#c9d1d9", lw=0.8)
text(ax, 4.0, 3.3, "단결정", size=9.5)
poly(ax, [(2.7, 1.6), (3.8, 0.9), (4.2, 0.9), (5.3, 1.6)], "#c9d1d9", lw=0.8)
rect(ax, 3.85, 0.3, 0.3, 0.6, "#a0aab4", lw=0.6)
for y in (5.05, 5.45):
    ax.add_patch(Ellipse((4.0, y), 4.6, 0.5, fc="none", ec=C["orange"], lw=2.2, zorder=6))
text(ax, 6.5, 5.25, "RF coil", size=9.5, ha="left", color=C["orange"])
text(ax, 0.2, 5.25, "녹은 구간", size=9.5, ha="left")
arrow(ax, 1.6, 5.2, 2.7, 5.3, lw=0.8, ms=7)
arrow(ax, 7.3, 4.6, 7.3, 7.4, color="orange", lw=1.4)
text(ax, 7.1, 8.0, "coil이 위로\n이동", size=8.5, ha="center", color=C["orange"])
save(f, P, "fz")
