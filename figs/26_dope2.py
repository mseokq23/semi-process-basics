import numpy as np
from common import *

P = 26

# 1. ion 주입기 구성
f, ax = canvas(12, 5.0, (0, 24), (-0.6, 10))
box(ax, 0.4, 6.6, 3.2, 2.4, "ion source\n(BF₃, PH₃, AsH₃\n → plasma)", fc="#fff3e0", size=9.2)
r = 2.4
cx, cy = 5.0, 7.8 - r
ax.add_patch(Wedge((cx, cy), r + 0.75, 0, 90, width=1.5, fc="#cfd8dc", ec="#555555", lw=0.8))
text(ax, 7.9, 8.9, "질량 분석 자석", size=9.5, ha="left")
line(ax, [3.6, cx], [7.8, 7.8], color=C["red"], lw=2.0)
ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=0, theta2=90, color=C["red"], lw=2.0, zorder=6))
ex = cx + r
line(ax, [ex, ex], [cy, 2.3], color=C["red"], lw=2.0)
rect(ax, ex - 0.95, 3.7, 0.7, 0.35, "#424242", lw=0)
rect(ax, ex + 0.25, 3.7, 0.7, 0.35, "#424242", lw=0)
text(ax, ex + 1.1, 3.85, "분해능 slit (원하는 질량만)", size=9, ha="left")
ax.add_patch(Arc((ex + 0.8, 2.3), 1.6, 1.4, theta1=180, theta2=270, color=C["red"], lw=2.0, zorder=6))
line(ax, [ex + 0.8, 10.6], [1.6, 1.6], color=C["red"], lw=2.0)
box(ax, 10.6, 0.6, 3.6, 2.0, "가속관\n(energy 결정)", fc="#e3f2fd", size=9.5)
line(ax, [14.2, 16.0], [1.6, 1.6], color=C["red"], lw=2.0)
box(ax, 16.0, 0.6, 2.8, 2.0, "beam scan", fc="#ede7f6", size=9.5)
for a_ in (-12, 0, 12):
    line(ax, [18.8, 21.4], [1.6, 1.6 + 2.6 * np.tan(np.deg2rad(a_))], color=C["red"], lw=1.2)
rect(ax, 21.4, 0.0, 0.35, 3.4, "si", lw=0.6)
text(ax, 21.6, 3.9, "wafer", size=9.5)
rect(ax, 22.3, 0.6, 1.2, 2.0, "#ffe0b2", lw=0.6)
text(ax, 22.9, 0.1, "Faraday cup\n(전류로 dose 측정)", size=8.5, va="top")
text(ax, 16.5, 7.4, "dose = ∫ I dt / (q × 면적)\nenergy = 전하 × 가속 전압", size=10, box="#fff8e1")
save(f, P, "implanter")

# 2. 질량 분석
f, ax = canvas(7.4, 5.8, (-1.2, 9.0), (-8.6, 1.6))
r11 = 5.0
ax.add_patch(Wedge((0, -r11), r11 * 1.22, 0, 90, width=r11 * 0.40, fc="#eceff1", ec="#90a4ae", lw=0.8))
line(ax, [-1.2, 0.0], [0.0, 0.0], color="#555555", lw=2.4)
text(ax, -0.6, 0.45, "입사", size=9)
for m, c, s in [(10, PAL[0], "¹⁰B⁺"), (11, PAL[1], "¹¹B⁺"), (19, PAL[3], "F⁺"), (49, PAL[2], "BF₂⁺")]:
    rr = r11 * np.sqrt(m / 11)
    ph = np.linspace(0, np.pi / 2, 300)
    xs, ys = rr * np.sin(ph), -rr * (1 - np.cos(ph))
    d = np.hypot(xs, ys + r11)
    inside = d <= r11 * 1.22
    k = np.argmax(~inside) if (~inside).any() else len(xs)
    ax.plot(xs[:k], ys[:k], color=c, lw=2.0, label=f"{s} (질량 {m})")
    if k < len(xs):
        text(ax, xs[k - 1] + 0.15, ys[k - 1] + 0.1, "×", size=13, color=C["red"], weight="bold")
    elif m == 11:
        line(ax, [xs[-1], xs[-1]], [ys[-1], -8.0], color=c, lw=2.0)
    else:
        line(ax, [xs[-1], xs[-1]], [ys[-1], -6.8], color=c, lw=2.0)
        text(ax, xs[-1] - 0.35, -6.55, "×", size=13, color=C["red"], weight="bold")
rect(ax, r11 - 1.4, -7.2, 1.32, 0.4, "#424242", lw=0)
rect(ax, r11 + 0.08, -7.2, 1.32, 0.4, "#424242", lw=0)
text(ax, r11, -8.3, "slit: ¹¹B⁺만 통과", size=9.5)
ax.legend(fontsize=9, loc="lower left")
text(ax, 3.9, 1.2, "같은 전압으로 가속 → 무거울수록 크게 돎 (반지름 ∝ 질량의 제곱근)", size=9.2)
save(f, P, "mass_analysis")

# 3. channeling
f, axs = plt.subplots(1, 3, figsize=(13.5, 4.0), gridspec_kw=dict(width_ratios=[1, 1, 1.3]))
for k, ax in enumerate(axs[:2]):
    canvas(0, 0, (-0.5, 8.5), (-0.5, 8.5), ax=ax)
    for i in range(5):
        for j in range(5):
            circ(ax, i * 2.0, j * 2.0, 0.35, "#cfd8dc", lw=0.4)
    if k == 0:
        line(ax, [3.0, 3.0], [8.4, -0.2], color=C["red"], lw=2.0)
        ax.set_title("결정 방향과 나란히: 원자 사이 통로로 깊이 들어감", fontsize=10.2, loc="left")
    else:
        xs = [2.4, 3.4, 3.0, 4.1, 3.6]
        ys = [8.4, 6.0, 5.0, 4.0, 3.2]
        ax.plot(xs, ys, color=C["red"], lw=2.0)
        ax.set_title("7° 기울이면: 바로 원자들과 부딪힘", fontsize=10.2, loc="left")
x = np.linspace(0, 400, 400)
g = 1e19 * np.exp(-(x - 100) ** 2 / (2 * 37 ** 2))
tail = 3e17 * np.exp(-x / 70) * (x > 60)
axs[2].semilogy(x, g + 1e14, color=PAL[0], lw=2, label="기울여서 주입 (거의 Gaussian)")
axs[2].semilogy(x, g + tail + 1e14, "--", color=PAL[1], lw=2, label="channeling 꼬리")
axs[2].set_ylim(1e15, 3e19)
axs[2].set_xlabel("깊이 (nm)")
axs[2].set_ylabel("농도 (cm⁻³)")
axs[2].set_title("channeling이 있으면 꼬리가 길어져 접합이 깊어짐 (개념)", fontsize=10.2, loc="left")
axs[2].legend(fontsize=8.8)
axs[2].grid(alpha=0.25)
plt.tight_layout()
save(f, P, "channeling")

# 4. shadowing
f, axs = panels(2, 2, 5.6, 3.6, (0, 12), (0, 7.4), titles=["기울여 주입하면 gate 한쪽에 그림자",
                                                         "wafer를 90°씩 돌려 4번 (quad 주입)"], size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 11.4, 3.0, "pw", lw=0.6)
    rect(ax, 4.8, 3.3, 2.4, 0.15, "ox", lw=0.4)
    rect(ax, 4.8, 3.45, 2.4, 2.6, "poly", lw=0.6)
    if k == 0:
        for x in np.arange(0.6, 11.5, 0.9):
            arrow(ax, x, 7.2, x + 1.2, 3.5, color="red", lw=1.0, ms=7)
        rect(ax, 0.8, 2.6, 4.0, 0.7, "nl", lw=0.4)
        rect(ax, 8.4, 2.6, 3.0, 0.7, "nl", lw=0.4)
        poly(ax, [(7.2, 3.3), (8.4, 3.3), (8.4, 3.3), (7.2, 3.3)], "white", lw=0)
        text(ax, 7.8, 2.2, "그림자\n(안 들어감)", size=9, color=C["red"])
    else:
        rect(ax, 0.8, 2.6, 4.0, 0.7, "nl", lw=0.4)
        rect(ax, 7.2, 2.6, 4.2, 0.7, "nl", lw=0.4)
        for sgn in (-1, 1):
            for x in np.arange(1.0, 11.5, 1.4):
                arrow(ax, x, 7.2, x + sgn * 1.0, 3.6, color="red", lw=0.9, ms=6)
        text(ax, 6.0, 1.5, "양쪽이 대칭이 됨", size=9.5)
save(f, P, "shadowing")

# 5. 용도별 dose-energy 지도
items = [("retrograde well", 200, 1500, 5e12, 5e13), ("well", 80, 200, 5e12, 3e13), ("halo / punch-through", 10, 80, 5e12, 5e13),
         ("Vt 조절", 5, 50, 5e11, 1e13), ("LDD", 2, 20, 5e13, 5e14), ("source / drain", 1, 30, 1e15, 6e15),
         ("PAI (Ge, 비정질화)", 10, 50, 1e14, 1e15), ("poly gate doping", 5, 30, 1e15, 1e16)]
f, ax = plot_ax(8.4, 5.0)
lab_pos = {"source / drain": (2.2, 2.2e15), "poly gate doping": (14, 7e15)}
for (s, e0, e1, d0, d1), c in zip(items, PAL + PAL):
    ax.add_patch(Rectangle((e0, d0), e1 - e0, d1 - d0, fc=c, alpha=0.3, ec=c, lw=1.4))
    lx, ly = lab_pos.get(s, (np.sqrt(e0 * e1), np.sqrt(d0 * d1)))
    ax.text(lx, ly, s, ha="center", va="center", fontsize=9)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.7, 2000)
ax.set_ylim(2e11, 3e16)
ax.set_xlabel("energy (keV)")
ax.set_ylabel("dose (ions/cm²)")
ax.set_title("CMOS 공정에서 쓰는 주입 조건 (대략적인 범위)", loc="left")
save(f, P, "dose_energy")
