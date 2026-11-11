import numpy as np
from common import *

P = 28

# 1. 열처리 방식별 온도-시간
f, axs = plt.subplots(1, 4, figsize=(14, 3.4))
t = np.linspace(0, 120, 600)
T = np.clip(np.where(t < 30, 600 + 10 * t, np.where(t < 60, 900, 900 - 10 * (t - 60))), 600, None)
axs[0].plot(t, T, color=PAL[0], lw=2.2)
axs[0].set_xlabel("시간 (분)")
axs[0].set_title("퍼니스: 수십 분", loc="left", fontsize=11)
t = np.linspace(0, 40, 600)
T = np.where(t < 7, 400 + 100 * t, np.where(t < 17, 1100, np.maximum(1100 - 60 * (t - 17), 400)))
axs[1].plot(t, np.minimum(T, 1100), color=PAL[1], lw=2.2)
axs[1].set_xlabel("시간 (초)")
axs[1].set_title("RTA: 수 ~ 수십 초", loc="left", fontsize=11)
t = np.linspace(-6, 6, 600)
axs[2].plot(t, 500 + 550 * np.exp(-np.abs(t) / 1.4), color=PAL[2], lw=2.2)
axs[2].set_xlabel("시간 (초)")
axs[2].set_title("스파이크: 최고점에서 거의 안 머묾", loc="left", fontsize=11)
t = np.linspace(-2, 8, 600)
axs[3].plot(t, np.where(t < 0, 800, 800 + 500 * np.exp(-t / 1.0)), color=PAL[3], lw=2.2)
axs[3].set_xlabel("시간 (ms)")
axs[3].set_title("플래시 / 레이저: ms 이하", loc="left", fontsize=11)
for ax in axs:
    ax.set_ylim(300, 1400)
    ax.grid(alpha=0.25)
axs[0].set_ylabel("웨이퍼 온도 (°C)")
plt.suptitle("짧게, 높게 → 활성화는 하면서 확산은 줄이기 (모양만 나타낸 그래프)", fontsize=11, y=1.03)
plt.tight_layout()
save(f, P, "anneal_types")

# 2. 손상 회복과 활성화
f, axs = panels(2, 2, 4.8, 4.0, (-0.8, 8.8), (-0.8, 6.8), titles=["주입 직후: 격자 손상, 도펀트가 격자 사이에",
                                                               "열처리 후: 격자 회복, 도펀트가 Si 자리에 (활성화)"],
                size=10.2)
for k, ax in enumerate(axs):
    rng = np.random.default_rng(1)
    for i in range(5):
        for j in range(4):
            dx, dy = (rng.normal(0, 0.25, 2) if k == 0 and j >= 2 else (0, 0))
            if (i, j) in [(1, 3), (3, 2)]:
                if k == 1:
                    circ(ax, i * 2.0, j * 2.0, 0.42, C["pp"], lw=0.8)
                    text(ax, i * 2.0, j * 2.0, "B", size=9, weight="bold")
                else:
                    circ(ax, i * 2.0, j * 2.0, 0.42, "white", ec="#999999", lw=0.8)
                continue
            circ(ax, i * 2.0 + dx, j * 2.0 + dy, 0.42, "#e8e8e8", lw=0.6)
    if k == 0:
        for (x, y) in [(3.0, 5.0), (5.0, 3.0)]:
            circ(ax, x, y, 0.42, C["pp"], lw=0.8)
            text(ax, x, y, "B", size=9, weight="bold")
save(f, P, "activation")

# 3. TED (개념)
x = np.linspace(0, 200, 600)
Rp, s0 = 30, 12


def prof(s):
    return 0.4 * 1e15 / (s * 1e-7) * np.exp(-(x - Rp) ** 2 / (2 * s ** 2))


f, ax = plot_ax(7.2, 4.2)
ax.semilogy(x, prof(s0) + 1, color="#555555", lw=1.8, ls="--", label="주입 직후")
ax.semilogy(x, prof(np.sqrt(s0 ** 2 + 6 ** 2)) + 1, color=PAL[0], lw=2.2, label="열처리 후 (정상 확산만)")
ax.semilogy(x, prof(np.sqrt(s0 ** 2 + 30 ** 2)) + 1, color=PAL[1], lw=2.2, label="열처리 후 (TED)")
ax.axhline(1e17, color="#999999", lw=0.8, ls=":")
ax.text(150, 1.4e17, "기판", fontsize=9)
ax.set_ylim(1e16, 1e21)
ax.set_xlabel("깊이 (nm)")
ax.set_ylabel("B 농도 (cm⁻³)")
ax.set_title("TED: 주입 손상(격자간 Si) 때문에 처음 잠깐 B가 훨씬 빨리 퍼짐 (개념)", loc="left", fontsize=10.5)
ax.legend(fontsize=9)
save(f, P, "ted")

# 4. 4점 탐침 + 면저항
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.2))
canvas(0, 0, (0, 12), (-0.5, 9.5), ax=ax1)
ax1.set_title("4점 탐침", loc="left", fontsize=11)
rect(ax1, 0.5, 0.5, 11.0, 1.6, "si", lw=0.6)
rect(ax1, 0.5, 2.1, 11.0, 0.5, "pp", lw=0.6)
xs_ = [2.5, 5.0, 7.0, 9.5]
for x in xs_:
    poly(ax1, [(x - 0.2, 5.6), (x + 0.2, 5.6), (x, 2.65)], "#9e9e9e", lw=0.6)
line(ax1, [2.5, 2.5, 9.5, 9.5], [5.6, 7.0, 7.0, 5.6], lw=1.2)
circ(ax1, 6.0, 7.0, 0.45, "white", lw=1.0)
text(ax1, 6.0, 7.0, "I", size=10, weight="bold")
line(ax1, [5.0, 5.0, 7.0, 7.0], [5.6, 6.0, 6.0, 5.6], lw=1.2, color=C["blue"])
circ(ax1, 6.0, 6.0, 0.42, "white", lw=1.0, ec=C["blue"])
text(ax1, 6.0, 6.0, "V", size=10, weight="bold", color=C["blue"])
text(ax1, 6.0, 8.7, "바깥 두 개로 전류, 안쪽 두 개로 전압 → 접촉 저항 영향 없음", size=9.5)
text(ax1, 6.0, 1.3, "↑ 얇은 도핑층 (Si 기판 위)", size=9.5, color="#333333")
text(ax1, 6.0, 0.0, "면저항 Rs ≈ 4.532 × V / I (Ω/□)", size=10, va="bottom")
canvas(0, 0, (0, 12), (-0.5, 9.5), ax=ax2)
ax2.set_title("면저항: 정사각형 하나의 저항", loc="left", fontsize=11)
for k in range(3):
    rect(ax2, 1.5 + k * 2.6, 3.0, 2.6, 2.6, "pp", lw=1.0, alpha=0.6)
text(ax2, 5.4, 4.3, "□                □                □", size=12)
bracket(ax2, 1.5, 9.3, 6.1, "길이 L", size=10)
vdim(ax2, 9.7, 3.0, 5.6, "폭 W", size=10)
text(ax2, 6.0, 1.6, "R = Rs × L / W = Rs × (정사각형 개수)\n위 예: 3 × Rs. 크기와 상관없이 정사각형이면 Rs", size=10)
plt.tight_layout()
save(f, P, "four_point")

# 5. SIMS vs 캐리어 분포 (개념)
x = np.linspace(0, 120, 500)
chem = 0.4 * 5e15 / (12e-7) * np.exp(-(x - 20) ** 2 / (2 * 12 ** 2)) + 1e15
act = np.minimum(chem, 2e20)
f, ax = plot_ax(7.2, 4.2)
ax.semilogy(x, chem, color=PAL[0], lw=2.2, label="SIMS: 들어간 B 원자 전부")
ax.semilogy(x, act, "--", color=PAL[1], lw=2.2, label="SRP / Hall: 실제로 전기적으로 활성된 캐리어")
ax.axhline(2e20, color="#999999", lw=0.8, ls=":")
ax.text(70, 2.6e20, "고용 한계 근처에서 잘림 (예시 2×10²⁰)", fontsize=9)
ax.set_ylim(1e16, 3e21)
ax.set_xlabel("깊이 (nm)")
ax.set_ylabel("농도 (cm⁻³)")
ax.set_title("고농도에서는 넣은 양과 활성화된 양이 다름 (개념)", loc="left", fontsize=11)
ax.legend(fontsize=9)
save(f, P, "sims_srp")

# 6. 접합 깊이 vs 면저항
xj = np.linspace(5, 100, 200)
f, ax = plot_ax(7.2, 4.2)
for Na, mu, c in [(1e20, 60, PAL[0]), (2e20, 45, PAL[1]), (5e20, 35, PAL[2])]:
    Rs = 1 / (1.602e-19 * mu * Na * xj * 1e-7)
    ax.plot(xj, Rs, color=c, lw=2.2, label=f"활성 농도 {Na:.0e} cm⁻³")
ax.set_yscale("log")
ax.set_xlabel("접합 깊이 x_j (nm)")
ax.set_ylabel("면저항 (Ω/□)")
ax.set_title("얕게 만들수록 저항이 커짐 → 활성 농도를 올려야 함 (상자 분포 근사)", loc="left", fontsize=10.5)
ax.legend(fontsize=9)
save(f, P, "xj_rs")
