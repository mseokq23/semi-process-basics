import numpy as np
from common import *

P = 27

# 1. 핵 저지 / 전자 저지 (Si 기판)
Z2, M2 = 14, 28.09


def sn(E, Z1, M1):
    a = Z1 ** 0.23 + Z2 ** 0.23
    eps = 32.53 * M2 * E / (Z1 * Z2 * (M1 + M2) * a)
    s = np.log(1 + 1.1383 * eps) / (2 * (eps + 0.01321 * eps ** 0.21226 + 0.19593 * eps ** 0.5))
    return 8.462 * Z1 * Z2 * M1 * s / ((M1 + M2) * a)       # eV / (1e15 atoms/cm²)


def se(E):
    return 0.2 * np.sqrt(E * 1e3)                            # k ≈ 0.2e-15 eV^0.5 cm²


E = np.logspace(-0.5, 3.3, 400)
f, ax = plot_ax(7.6, 4.6)
for (name, Z1, M1), c in zip([("B", 5, 11), ("P", 15, 31), ("As", 33, 75)], PAL):
    s_n = sn(E, Z1, M1)
    ax.loglog(E, s_n, color=c, lw=2.2, label=f"{name} 핵 저지")
    k = np.argmin(np.abs(np.log(s_n / se(E))))
    ax.plot(E[k], se(E[k]), "o", color=c, ms=7)
    print(f"{name}: crossover ~ {E[k]:.0f} keV")
ax.loglog(E, se(E), "--", color="#222222", lw=2.0, label="전자 저지 (ion 종류와 거의 무관)")
ax.set_xlabel("ion energy (keV)")
ax.set_ylabel("저지능 (eV / 10¹⁵ atoms·cm⁻²)")
ax.set_title("Si 속 ion 저지: 무거울수록 핵 저지가 오래 우세 (ZBL + LSS 근사)", loc="left", fontsize=10.5)
ax.legend(fontsize=9)
ax.set_ylim(1, 1000)
save(f, P, "stopping")

# 2. Gaussian 분포
Rp, dRp, dose, NB = 98.7, 37.1, 1e14, 1e16
x = np.linspace(0, 350, 600)
N = 0.4 * dose / (dRp * 1e-7) * np.exp(-(x - Rp) ** 2 / (2 * dRp ** 2))
Np = 0.4 * dose / (dRp * 1e-7)
xj = Rp + dRp * np.sqrt(2 * np.log(Np / NB))
print(f"B 30keV 1e14: Np = {Np:.2e}, xj = {xj:.0f} nm")
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.2))
ax1.plot(x, N, color=PAL[1], lw=2.2)
ax1.axvline(Rp, color="#555555", lw=0.8, ls=":")
ax1.annotate("", xy=(Rp - dRp, Np * 0.6065), xytext=(Rp + dRp, Np * 0.6065),
             arrowprops=dict(arrowstyle="<|-|>", color=PAL[0], lw=1.4))
ax1.text(Rp, Np * 0.66, "2ΔRp", ha="center", color=PAL[0], fontsize=10)
ax1.text(Rp + 4, Np * 1.02, f"Rp = {Rp:.0f} nm", fontsize=10)
ax1.set_xlabel("깊이 (nm)")
ax1.set_ylabel("농도 (cm⁻³)")
ax1.set_title("B 30 keV, 10¹⁴ cm⁻² (선형 축)", loc="left", fontsize=11)
ax1.grid(alpha=0.25)
ax2.semilogy(x, N + 1, color=PAL[1], lw=2.2)
ax2.axhline(NB, color="#555555", lw=1.0, ls="--")
ax2.text(250, NB * 1.6, "기판 n형 10¹⁶", fontsize=9.5)
ax2.plot(xj, NB, "o", color=PAL[1])
ax2.text(xj + 6, NB * 8, f"x_j ≈ {xj:.0f} nm", fontsize=9.5, color=PAL[1])
ax2.text(15, Np * 0.5, f"최대 농도 = 0.4 × dose / ΔRp\n≈ {Np:.1e} cm⁻³", fontsize=9.5)
ax2.set_ylim(1e15, 5e19)
ax2.set_xlabel("깊이 (nm)")
ax2.set_title("log 축으로 보면 접합 깊이가 보임", loc="left", fontsize=11)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "gaussian")

# 3. B, P, As 비교 (같은 30 keV, 10¹⁵)
tab = {"B": (98.7, 37.1), "P": (36.8, 16.6), "As": (21.5, 8.0)}
x = np.linspace(0, 260, 600)
f, ax = plot_ax(7.2, 4.2)
for (el, (rp, drp)), c in zip(tab.items(), PAL):
    n = 0.4 * 1e15 / (drp * 1e-7) * np.exp(-(x - rp) ** 2 / (2 * drp ** 2))
    ax.semilogy(x, n + 1, color=c, lw=2.2, label=f"{el}: Rp {rp:.0f} nm, ΔRp {drp:.0f} nm")
ax.set_ylim(1e16, 1e21)
ax.set_xlabel("깊이 (nm)")
ax.set_ylabel("농도 (cm⁻³)")
ax.set_title("같은 30 keV: 무거운 ion일수록 얕고 좁게 (Rp, ΔRp는 표 대략값)", loc="left", fontsize=10.5)
ax.legend(fontsize=9)
save(f, P, "ion_compare")

# 4. 충돌 cascade
f, axs = panels(2, 2, 5.2, 4.5, (-0.5, 10.5), (-1.5, 9.5), titles=["가벼운 ion (B): 길게 가다가 끝에서 조금 손상",
                                                                 "무거운 ion (As): 짧게 가면서 많이 부숨"], size=10.5)
rng = np.random.default_rng(3)
for k, ax in enumerate(axs):
    for i in range(11):
        for j in range(9):
            circ(ax, i, j, 0.18, "#cfd8dc", lw=0.3)
    if k == 0:
        path = [(3.2, 9.3), (3.5, 7.0), (3.3, 5.0), (4.1, 3.2), (3.8, 2.0), (4.6, 1.2)]
        dis = [(4.0, 2.9), (4.4, 1.6)]
    else:
        path = [(5.2, 9.3), (5.5, 7.6), (5.0, 6.4), (5.8, 5.6)]
        dis = [(4.4, 7.2), (6.4, 7.0), (4.6, 6.0), (6.6, 6.2), (5.3, 5.0), (6.2, 4.8), (4.2, 5.4), (6.8, 5.6),
               (5.0, 4.4), (5.9, 4.2)]
    xs, ys = zip(*path)
    ax.plot(xs, ys, color=C["red"], lw=2.0, zorder=8)
    for (dx, dy) in dis:
        circ(ax, dx, dy, 0.22, "#ffb74d", lw=0.4, z=9)
        circ(ax, round(dx), round(dy), 0.2, "white", ec="#999999", lw=0.6, z=9)
for ax in axs:
    text(ax, 5.0, -1.0, "빨간 선: ion 경로 / 주황: 튕겨 나간 Si (격자간) / 흰색: 빈자리", size=8.8)
save(f, P, "cascade")

# 5. 비정질화
tt = ["낮은 dose: 손상이 띄엄띄엄", "중간: 손상 영역이 겹치기 시작", "높은 dose: 표면층이 비정질(a-Si)로"]
f, axs = panels(3, 3, 3.6, 3.0, (0, 10), (0, 6), titles=tt, size=10.2)
rng = np.random.default_rng(9)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 4.8, "si", lw=0.6)
    n = [6, 18, 0][k]
    for _ in range(n):
        ax.add_patch(Ellipse((rng.uniform(1, 9), rng.uniform(3.0, 4.6)), 1.2, 0.7, fc="#ffcc80", ec="none", alpha=0.85,
                             zorder=3))
    if k == 2:
        rect(ax, 0.3, 2.9, 9.4, 2.2, "#ffcc80", lw=0.6, alpha=0.9)
        text(ax, 5.0, 4.0, "비정질층", size=9.5)
        text(ax, 5.0, 1.5, "아래는 결정 그대로", size=9)
save(f, P, "amorphization")

# 6. mask 두께
x = np.linspace(0, 1200, 800)
Rp_pr, dRp_pr = 300, 90
N0 = 0.4 * 1e15 / (dRp_pr * 1e-7)
f, axs = plt.subplots(1, 2, figsize=(12.5, 4.0), sharey=True)
for ax, tm, title in [(axs[0], 450, "mask가 얇음: 꼬리가 Si까지 들어감"), (axs[1], 800, "mask가 충분: Si에는 거의 없음")]:
    n = N0 * np.exp(-(x - Rp_pr) ** 2 / (2 * dRp_pr ** 2))
    ax.semilogy(x, n + 1, color=PAL[1], lw=2.2)
    ax.axvspan(0, tm, color=C["pr"], alpha=0.35)
    ax.axvspan(tm, 1200, color=C["si"], alpha=0.6)
    ax.axhline(1e15, color="#555555", lw=1.0, ls="--")
    ax.text(tm / 2, 3e20, "PR mask", ha="center", fontsize=10)
    ax.text((tm + 1200) / 2, 3e20, "Si", ha="center", fontsize=10)
    ax.set_ylim(1e12, 1e21)
    ax.set_xlabel("깊이 (nm)")
    ax.set_title(title, loc="left", fontsize=11)
axs[0].set_ylabel("농도 (cm⁻³)")
axs[1].text(820, 3e15, "mask 두께 ≳ Rp + (4 ~ 5)ΔRp", fontsize=9.5)
plt.tight_layout()
save(f, P, "mask_thickness")
