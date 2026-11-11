import numpy as np
from common import *

P = 18

# 1. 게이트 식각
tt = ["① 하드마스크/PR 패턴", "② 메인 식각 (Cl₂, HBr): 수직으로", "③ 종말점 → 과식각 (HBr + O₂)",
      "④ PR 제거"]
f, axs = panels(4, 4, 3.3, 3.0, (0, 10), (0, 6.6), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.6, "si", lw=0.6)
    rect(ax, 0.3, 1.9, 9.4, 0.12, "ox", lw=0.4)
    if k == 0:
        rect(ax, 0.3, 2.02, 9.4, 2.4, "poly", lw=0.6)
    elif k == 1:
        rect(ax, 0.3, 2.62, 9.4, 0.0, "poly", lw=0)
        rect(ax, 0.3, 2.02, 3.4, 0.5, "poly", lw=0.6)
        rect(ax, 6.3, 2.02, 3.4, 0.5, "poly", lw=0.6)
        rect(ax, 3.7, 2.02, 2.6, 2.4, "poly", lw=0.6)
    else:
        rect(ax, 3.7, 2.02, 2.6, 2.4, "poly", lw=0.6)
    if k < 3:
        rect(ax, 3.7, 4.42, 2.6, 0.9, "pr", lw=0.6)
    if k == 1:
        for x in (1.2, 2.2, 7.8, 8.8):
            arrow(ax, x, 6.2, x, 2.7, color="red", lw=1.1, ms=7)
    if k == 2:
        text(ax, 5.0, 1.15, "2 nm 산화막 위에서 멈춰야 함", size=8.6, color=C["red"])
        for x in (1.2, 8.8):
            arrow(ax, x, 6.2, x, 2.2, color="red", lw=1.1, ms=7)
save(f, P, "gate_etch")

# 2. F/C 비 (개념도)
fc = np.linspace(1.0, 4.2, 200)
bound = 60 * (fc - 1.4) ** 1.6
f, ax = plot_ax(7.6, 4.6)
ax.fill_between(fc, 0, np.clip(bound, 0, 300), color="#ffe0b2", alpha=0.8)
ax.fill_between(fc, np.clip(bound, 0, 300), 300, color="#e3f2fd", alpha=0.8)
ax.plot(fc, np.clip(bound, 0, 300), color="#555555", lw=1.4)
ax.text(1.5, 230, "식각 영역", fontsize=12, color=C["blue"], fontweight="bold")
ax.text(3.0, 40, "폴리머 증착 영역", fontsize=12, color=C["orange"], fontweight="bold")
for name, x in [("C₄F₈", 2.0), ("C₃F₈", 2.67), ("C₂F₆", 3.0), ("CF₄", 4.0)]:
    ax.axvline(x, color="#999999", lw=0.7, ls=":")
    ax.text(x, 285, name, ha="center", fontsize=10)
ax.annotate("", xy=(1.9, 120), xytext=(3.1, 120), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.6))
ax.text(2.5, 128, "H₂ 추가 (F 소모)", ha="center", fontsize=9.5, color=C["red"])
ax.annotate("", xy=(4.1, 170), xytext=(3.2, 170), arrowprops=dict(arrowstyle="-|>", color=C["green"], lw=1.6))
ax.text(3.65, 178, "O₂ 추가 (C 소모)", ha="center", fontsize=9.5, color=C["green"])
ax.set_xlim(1.0, 4.2)
ax.set_ylim(0, 300)
ax.set_xlabel("F / C 비")
ax.set_ylabel("이온 에너지 (바이어스, 상대값)")
ax.set_title("불화탄소 가스: F/C 비와 이온 에너지로 식각 ↔ 증착이 갈림 (개념도)", loc="left", fontsize=11)
save(f, P, "fc_ratio")

# 3. OES 종말점 (개념 신호)
t = np.linspace(0, 100, 600)
ep = 62
co = 1.0 / (1 + np.exp((t - ep) / 2.0)) * 0.8 + 0.15 + 0.01 * np.sin(t * 2)
fl = 0.35 + 0.45 / (1 + np.exp(-(t - ep) / 2.0)) + 0.01 * np.cos(t * 2.3)
f, ax = plot_ax(7.6, 4.0)
ax.plot(t, co, color=PAL[0], lw=2.2, label="CO 발광 (483.5 nm): 산화막에서 나옴")
ax.plot(t, fl, color=PAL[1], lw=2.2, label="F 발광 (703.7 nm): 덜 소모되면 늘어남")
ax.axvline(ep, color="#555555", ls="--", lw=1.0)
ax.axvspan(ep, ep + 15, color="#fff3e0")
ax.text(ep + 1, 1.05, "종말점", fontsize=10)
ax.text(ep + 7.5, 0.06, "과식각", ha="center", fontsize=9.5)
ax.set_ylim(0, 1.15)
ax.set_xlabel("식각 시간 (s)")
ax.set_ylabel("발광 세기 (상대값)")
ax.set_title("산화막 식각 OES 신호 (개념)", loc="left")
ax.legend(fontsize=9, loc="center left")
save(f, P, "oes")

# 4. 간섭계 (막 두께에 따른 반사율 진동)
lam = 670.0
n0, n1, n2 = 1.0, 1.457, 3.81 - 0.01j
d0, rate = 600.0, 200.0                      # nm, nm/min
tt_ = np.linspace(0, 3.6, 800)
d = np.clip(d0 - rate * tt_, 0, None)
r01 = (n0 - n1) / (n0 + n1)
r12 = (n1 - n2) / (n1 + n2)
ph = np.exp(-2j * 2 * np.pi * n1 * d / lam)
R = np.abs((r01 + r12 * ph) / (1 + r01 * r12 * ph)) ** 2
f, ax = plot_ax(7.6, 4.0)
ax.plot(tt_ * 60, R * 100, color=PAL[4], lw=2.2)
ax.axvline(d0 / rate * 60, color="#555555", ls="--", lw=1.0)
ax.text(d0 / rate * 60 + 3, 22, "막이 다 깎임\n→ 신호가 평평", fontsize=9.5)
ax.set_ylim(0, 42)
ax.set_xlabel("시간 (s)")
ax.set_ylabel("반사율 (%)")
ax.set_title(f"SiO₂ {d0:.0f} nm를 {rate:.0f} nm/min로 식각할 때 670 nm 반사율 (계산)", loc="left", fontsize=11)
ax.text(5, 38.5, f"진동 한 주기 = λ / (2n) ≈ {lam / (2 * n1):.0f} nm 깎일 때마다", fontsize=9.5)
save(f, P, "interferometry")

# 5. Al 식각 후 부식
tt = ["① Al 식각 (Cl₂ + BCl₃) 직후", "② 대기에 꺼내면: 남은 Cl + 수분 → 부식", "③ 대책: 진공 안에서 PR 제거 + 표면 처리"]
f, axs = panels(3, 3, 3.9, 3.0, (0, 10), (0, 6.4), titles=tt, size=10)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.6, "ox", lw=0.6)
    for a, b in [(1.0, 4.0), (6.0, 9.0)]:
        rect(ax, a, 1.9, b - a, 1.6, "al", lw=0.6)
        if k < 2:
            rect(ax, a, 3.5, b - a, 1.0, "pr", lw=0.6)
    if k == 0:
        for x, y in [(4.15, 2.5), (5.85, 2.9), (2.0, 4.7), (7.0, 4.65), (4.1, 3.2), (5.9, 2.2)]:
            text(ax, x, y, "Cl", size=8.5, color=C["green"], weight="bold")
    if k == 1:
        for x, y in [(3.7, 2.4), (6.3, 3.0), (2.4, 1.95), (8.2, 1.95)]:
            circ(ax, x, y, 0.28, "#8d6e63", lw=0.3, z=4)
        text(ax, 5.0, 5.4, "HCl이 생겨서 Al을 먹음", size=9, color=C["red"])
    if k == 2:
        text(ax, 5.0, 5.0, "Cl 제거, 얇은 산화막으로 표면 보호", size=9, color=C["green"])
save(f, P, "al_corrosion")
