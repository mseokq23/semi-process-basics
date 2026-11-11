import numpy as np
from common import *

P = 9

# 1. 양성 / 음성 PR
f, axs = panels(3, 3, 3.8, 3.2, (0, 10), (0, 7.6),
                titles=["같은 mask로 노광", "양성 PR: 빛 받은 곳이 녹음", "음성 PR: 빛 받은 곳이 남음"], size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.4, 9.4, 1.8, "si", lw=0.7)
    rect(ax, 0.3, 2.2, 9.4, 0.5, "ox", lw=0.7)
opens = [(2.0, 4.0), (6.0, 8.0)]
rect(axs[0], 0.3, 2.7, 9.4, 1.0, "pr", lw=0.7)
for x0, x1 in opens:
    rect(axs[0], x0, 2.7, x1 - x0, 1.0, "#c39bd3", lw=0.5, z=3)
for x0, x1 in [(0.3, 2.0), (4.0, 6.0), (8.0, 9.7)]:
    rect(axs[0], x0, 5.2, x1 - x0, 0.35, "#444444", lw=0.4)
for x in (2.6, 3.4, 6.6, 7.4):
    arrow(axs[0], x, 7.2, x, 3.8, color="#8e44ad", ls="--", ms=8, lw=1.1)
for x0, x1 in [(0.3, 2.0), (4.0, 6.0), (8.0, 9.7)]:
    rect(axs[1], x0, 2.7, x1 - x0, 1.0, "pr", lw=0.7)
for x0, x1 in opens:
    rect(axs[2], x0, 2.7, x1 - x0, 1.0, "pr", lw=0.7)
text(axs[1], 5.0, 5.4, "mask 그림 그대로", size=9.5)
text(axs[2], 5.0, 5.4, "mask 그림 반대", size=9.5)
save(f, P, "pos_neg")

# 2. PR 구성
f, ax = canvas(11, 3.6, (0, 22), (0, 7.2))
items = [("수지 (polymer)", "막의 뼈대.\n현상액에 녹는 정도가\n바뀌는 주인공", "#fde2e4"),
         ("감광제 (PAC / PAG)", "빛을 받으면 화학 반응.\ng/i-line: DNQ, DUV 이후: PAG", "#e2ece9"),
         ("용매", "coating할 때 잘 퍼지게.\nsoft bake로 대부분 날림", "#dfe7fd"),
         ("첨가제", "quencher(산 확산 조절),\n계면활성제 등", "#f1f1f1")]
for k, (t, s, c) in enumerate(items):
    x = 0.3 + k * 5.45
    box(ax, x, 0.4, 5.0, 6.2, "", fc=c, size=10)
    text(ax, x + 2.5, 5.4, t, size=11, weight="bold")
    text(ax, x + 2.5, 2.8, s, size=9.5)
save(f, P, "pr_components")

# 3. DNQ-novolac
f, axs = panels(2, 2, 5.6, 3.6, (0, 10), (0, 7),
                titles=["빛 안 받은 곳: DNQ가 녹는 걸 막음", "빛 받은 곳: DNQ → carboxylic acid, 오히려 잘 녹음"],
                size=10.5)
rng = np.random.default_rng(2)
for k, ax in enumerate(axs):
    rect(ax, 0.5, 0.5, 9.0, 3.6, "pr", lw=0.7, alpha=0.65)
    xs = np.linspace(0.7, 9.3, 300)
    for yy in [1.1, 1.9, 2.7, 3.5]:
        ax.plot(xs, yy + 0.12 * np.sin(xs * 3 + yy), color="#8d6e63", lw=1.2, zorder=4)
    pts = rng.uniform([0.9, 0.8], [9.1, 3.8], (12, 2))
    for x, y in pts:
        if k == 0:
            circ(ax, x, y, 0.2, "#455a64", lw=0.4, z=5)
        else:
            circ(ax, x, y, 0.2, "#fbc02d", lw=0.4, z=5)
    text(ax, 5.0, 5.9, "현상액 (TMAH, alkali)", size=9.5, color=C["blue"])
    if k == 0:
        for x in (2.5, 5.0, 7.5):
            arrow(ax, x, 5.4, x, 4.4, color="blue", lw=1.2)
            text(ax, x + 0.3, 4.65, "×", size=14, color=C["red"], weight="bold")
        text(ax, 5.0, 0.0, "● DNQ (억제제)  /  ~ novolac 수지", size=9)
    else:
        for x in (2.5, 5.0, 7.5):
            arrow(ax, x, 5.4, x, 3.0, color="blue", lw=1.6)
        text(ax, 5.0, 0.0, "● 빛 받아 바뀐 DNQ (산)", size=9)
save(f, P, "dnq")

# 4. 화학증폭형 (CAR)
f, ax = canvas(12, 4.4, (0, 24), (0, 8.8))
rect(ax, 0.5, 0.6, 23, 4.2, "pr", lw=0.7, alpha=0.55)
xs = np.linspace(0.8, 22.8, 600)
ax.plot(xs, 2.7 + 0.18 * np.sin(xs * 1.5), color="#8d6e63", lw=2.0, zorder=4)
gx = np.arange(1.6, 22.5, 1.4)
for x in gx:
    y = 2.7 + 0.18 * np.sin(x * 1.5)
    line(ax, [x, x], [y, y + 0.7], color="#8d6e63", lw=1.2, z=4)
    if 6.5 < x < 15.0:
        text(ax, x, y + 0.95, "OH", size=8, color=C["blue"], weight="bold")
    else:
        circ(ax, x, y + 0.95, 0.3, "#90a4ae", lw=0.5, z=5)
ax.add_patch(Ellipse((10.6, 2.7), 9.5, 3.0, fc="none", ec=C["red"], ls="--", lw=1.2, zorder=6))
arrow(ax, 10.5, 8.2, 10.5, 5.0, color="purple", ls="--", lw=1.4)
text(ax, 10.8, 7.8, "빛 (광자 1개)", size=9.5, ha="left", color=C["purple"])
circ(ax, 10.5, 4.2, 0.35, "#fbc02d", lw=0.6, z=7)
text(ax, 10.5, 4.2, "H⁺", size=8.5, weight="bold", z=8)
for x0, x1 in [(10.2, 7.5), (10.8, 13.6)]:
    arrow(ax, x0, 3.9, x1, 3.5, color="red", lw=1.0, ms=8)
text(ax, 10.6, 0.15, "PEB 동안 산(H⁺) 하나가 돌아다니며 보호기를 여러 개 떼어냄 → 그 부분이 현상액에 녹음", size=9.5)
circ(ax, 18.6, 7.2, 0.3, "#90a4ae", lw=0.5)
text(ax, 19.2, 7.2, "보호기 (녹지 않게 막음)", size=9, ha="left")
text(ax, 18.6, 6.3, "OH", size=8, color=C["blue"], weight="bold")
text(ax, 19.2, 6.3, "떼어진 자리 (alkali에 녹음)", size=9, ha="left")
save(f, P, "car")

# 5. contrast 곡선
D = np.logspace(0, 2.3, 400)
D0, D100 = 20, 40
pos = np.clip(1 - np.log10(D / D0) / np.log10(D100 / D0), 0, 1)
g0, g100 = 12, 30
neg = np.clip(np.log10(D / g0) / np.log10(g100 / g0), 0, 1)
f, ax = plot_ax(7, 4.2)
ax.plot(D, pos, color=PAL[0], lw=2.4, label="양성 PR")
ax.plot(D, neg, color=PAL[1], lw=2.4, label="음성 PR")
ax.set_xscale("log")
ax.set_xlabel("노광량 (mJ/cm²)")
ax.set_ylabel("현상 후 남은 두께 비율")
for d, s in [(D0, "D₀"), (D100, "D₁₀₀")]:
    ax.axvline(d, color=PAL[0], lw=0.8, ls=":")
    ax.text(d, 1.05, s, color=PAL[0], ha="center", fontsize=10)
ax.set_ylim(-0.05, 1.15)
ax.text(70, 0.55, "contrast γ = 1 / log₁₀(D₁₀₀ / D₀)\n이 예: 1 / log₁₀(40/20) ≈ 3.3\n→ γ가 클수록 경계가 날카로움",
        fontsize=9.5, ha="left")
ax.legend(loc="center left")
ax.set_title("contrast 곡선 (예시 값)", loc="left")
save(f, P, "contrast_curve")

# 6. T-top, footing
f, axs = panels(3, 3, 3.4, 3.0, (0, 10), (0, 6.4), titles=["정상", "T-top (위쪽이 덜 녹음)",
                                                           "footing (바닥이 덜 녹음)"], size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.2, "si", lw=0.6)
    if k == 0:
        for x0, x1 in [(0.3, 3.0), (7.0, 9.7)]:
            rect(ax, x0, 1.5, x1 - x0, 3.0, "pr", lw=0.7)
    elif k == 1:
        poly(ax, [(0.3, 1.5), (3.0, 1.5), (3.0, 4.0), (3.9, 4.0), (3.9, 4.5), (0.3, 4.5)], "pr", lw=0.7)
        poly(ax, [(9.7, 1.5), (7.0, 1.5), (7.0, 4.0), (6.1, 4.0), (6.1, 4.5), (9.7, 4.5)], "pr", lw=0.7)
        text(ax, 5.0, 5.5, "공기 중 amine이 표면 산을 중화", size=8.8)
    else:
        poly(ax, [(0.3, 1.5), (4.0, 1.5), (3.0, 2.3), (3.0, 4.5), (0.3, 4.5)], "pr", lw=0.7)
        poly(ax, [(9.7, 1.5), (6.0, 1.5), (7.0, 2.3), (7.0, 4.5), (9.7, 4.5)], "pr", lw=0.7)
        text(ax, 5.0, 5.5, "아래 막(SiON, TiN 등)이 산을 중화", size=8.8)
save(f, P, "ttop_footing")
