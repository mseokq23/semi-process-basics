import numpy as np
from math import erfc
from common import *

P = 25
KB = 8.617e-5
# 진성 확산계수 (D0 cm²/s, Ea eV)
DIFF = {"B": (0.76, 3.46), "P": (3.85, 3.66), "As": (0.066, 3.44), "Sb": (0.214, 3.65)}


def D(el, T_c):
    d0, ea = DIFF[el]
    return d0 * np.exp(-ea / (KB * (T_c + 273.15)))


verfc = np.vectorize(erfc)

if __name__ == "__main__":
    for el in DIFF:
        print(f"{el}: D(1000C) = {D(el, 1000):.2e}, D(1100C) = {D(el, 1100):.2e} cm2/s")
    Cs, NB = 1e20, 1e15
    t1 = 30 * 60
    D1 = D("B", 1000)
    Q = 2 * Cs * np.sqrt(D1 * t1 / np.pi)
    t2 = 3600
    D2 = D("B", 1100)
    Dt2 = D2 * t2
    Csurf = Q / np.sqrt(np.pi * Dt2)
    xj = 2 * np.sqrt(Dt2) * np.sqrt(np.log(Csurf / NB))
    print(f"predep B 1000C 30min: sqrt(Dt) = {np.sqrt(D1 * t1) * 1e7:.0f} nm, Q = {Q:.2e} cm-2")
    print(f"drive-in 1100C 1h: sqrt(Dt) = {np.sqrt(Dt2) * 1e4:.3f} um, Cs = {Csurf:.2e}, xj = {xj * 1e4:.2f} um")

    # 1. 확산 vs 이온주입 단면
    tt = ["열확산: 표면이 가장 진하고, 마스크 밑으로도 퍼짐", "이온주입: 에너지로 깊이, 도즈로 양을 따로 조절"]
    f, axs = panels(2, 2, 5.6, 3.4, (0, 10), (0, 6.4), titles=tt, size=10.5)
    for k, ax in enumerate(axs):
        rect(ax, 0.3, 0.3, 9.4, 3.6, "si", lw=0.6)
        rect(ax, 0.3, 3.9, 3.4, 0.9, "ox", lw=0.6)
        rect(ax, 6.3, 3.9, 3.4, 0.9, "ox", lw=0.6)
        if k == 0:
            clip = Rectangle((0.3, 0.3), 9.4, 3.6, transform=ax.transData)
            for r, a in [(2.2, 0.25), (1.6, 0.45), (1.0, 0.75)]:
                e = Ellipse((5.0, 3.9), 2.6 + 2 * r, 2 * r, fc=C["pp"], ec="none", alpha=a, zorder=2)
                ax.add_patch(e)
                e.set_clip_path(clip)
            rect(ax, 0.3, 4.8, 9.4, 0.5, "#fff3e0", lw=0.4)
            text(ax, 5.0, 5.05, "도펀트 소스 (기체, 도핑된 막)", size=8.8)
        else:
            ax.add_patch(Ellipse((5.0, 2.9), 2.9, 1.1, fc=C["pp"], ec="none", alpha=0.75, zorder=2))
            rect(ax, 0.3, 4.8, 9.4, 0.0, "white", lw=0)
            for x in np.arange(3.9, 6.2, 0.35):
                arrow(ax, x, 6.2, x, 4.0, color="red", lw=1.0, ms=7)
    save(f, P, "diff_vs_impl")

    # 2. 확산 메커니즘
    tt = ["빈자리(공공)를 타고 이동", "격자 사이를 타고 이동"]
    f, axs = panels(2, 2, 4.8, 3.6, (-0.8, 8.8), (-0.8, 6.8), titles=tt, size=11)
    for k, ax in enumerate(axs):
        for i in range(5):
            for j in range(4):
                if k == 0 and (i, j) == (3, 2):
                    circ(ax, i * 2.0, j * 2.0, 0.42, "white", ec="#999999", lw=0.8)
                    continue
                if (i, j) == (2, 2):
                    circ(ax, i * 2.0, j * 2.0, 0.45, C["pp"], lw=0.8)
                    text(ax, i * 2.0, j * 2.0, "B", size=9, weight="bold")
                    continue
                circ(ax, i * 2.0, j * 2.0, 0.42, "#e8e8e8", lw=0.6)
        if k == 0:
            arrow(ax, 4.5, 4.0, 5.5, 4.0, color="red", lw=1.6)
            text(ax, 6.0, 5.2, "빈자리", size=9.5, color="#555555")
        else:
            circ(ax, 5.0, 3.0, 0.3, C["pp"], lw=0.6)
            ax.add_patch(FancyArrowPatch((5.0, 3.0), (7.0, 5.0), connectionstyle="arc3,rad=-0.4",
                                         arrowstyle="-|>", mutation_scale=12, color=C["red"], lw=1.4, zorder=9))
            text(ax, 4.0, 0.95 + 0.0, "격자 사이 원자", size=9.5, color="#555555")
    save(f, P, "mechanisms")

    # 3. 두 가지 해: erfc (선확산) / Gaussian (드라이브인)
    x = np.linspace(0, 2.0e-4, 600)          # cm
    pre = Cs * verfc(x / (2 * np.sqrt(D1 * t1)))
    gau = Q / np.sqrt(np.pi * Dt2) * np.exp(-x ** 2 / (4 * Dt2))
    f, ax = plot_ax(7.4, 4.4)
    ax.semilogy(x * 1e4, pre, color=PAL[0], lw=2.2, label="① 선확산: 표면 농도 일정 → erfc")
    ax.semilogy(x * 1e4, gau, color=PAL[1], lw=2.2, label="② 드라이브인: 총량 일정 → 가우시안")
    ax.axhline(NB, color="#555555", lw=1.0, ls="--")
    ax.text(1.55, NB * 1.6, "기판 농도 10¹⁵", fontsize=9.5)
    ax.plot(xj * 1e4, NB, "o", color=PAL[1])
    ax.text(xj * 1e4 + 0.03, NB * 6, f"접합 깊이 ≈ {xj * 1e4:.2f} µm", fontsize=9.5, color=PAL[1])
    ax.set_ylim(1e14, 3e20)
    ax.set_xlabel("깊이 (µm)")
    ax.set_ylabel("B 농도 (cm⁻³)")
    ax.set_title("B: ① 1000 °C 30분 선확산 → ② 1100 °C 1시간 드라이브인 (계산)", loc="left", fontsize=11)
    ax.legend(fontsize=9)
    save(f, P, "profiles")

    # 4. 드라이브인 시간에 따른 변화
    f, ax = plot_ax(7.2, 4.2)
    for th, c in zip((0.25, 1, 4, 16), PAL):
        Dt = D2 * th * 3600
        ax.plot(x * 1e4, Q / np.sqrt(np.pi * Dt) * np.exp(-x ** 2 / (4 * Dt)), color=c, lw=2, label=f"{th:g} 시간")
    ax.set_xlabel("깊이 (µm)")
    ax.set_ylabel("B 농도 (cm⁻³)")
    ax.set_title("1100 °C 드라이브인: 총량(면적)은 같고 깊이 퍼짐", loc="left")
    ax.legend()
    save(f, P, "drivein_time")

    # 5. 접합 깊이 정의
    xx = np.linspace(0, 2.0, 600)
    NA = Csurf * np.exp(-(xx * 1e-4) ** 2 / (4 * Dt2))
    NDb = 1e16
    xj2 = 2 * np.sqrt(Dt2) * np.sqrt(np.log(Csurf / NDb)) * 1e4
    f, ax = plot_ax(7.2, 4.2)
    ax.semilogy(xx, NA, color=PAL[1], lw=2, label="넣은 B (억셉터)")
    ax.semilogy(xx, np.full_like(xx, NDb), color=PAL[0], lw=2, label="기판 n형 도핑 (도너)")
    ax.semilogy(xx, np.abs(NA - NDb) + 1e12, "--", color="#222222", lw=1.6, label="순 도핑 |N_A − N_D|")
    ax.axvline(xj2, color="#999999", lw=1.0, ls=":")
    ax.text(xj2 + 0.03, 1e18, "접합 (x_j)\n여기서 p → n", fontsize=9.5)
    ax.text(0.15, 3e14, "p형", fontsize=11, color=PAL[1])
    ax.text(1.6, 3e14, "n형", fontsize=11, color=PAL[0])
    ax.set_ylim(1e14, 3e19)
    ax.set_xlabel("깊이 (µm)")
    ax.set_ylabel("농도 (cm⁻³)")
    ax.set_title("접합 깊이: 넣은 도펀트 = 기판 도핑이 되는 깊이", loc="left")
    ax.legend(fontsize=9, loc="upper right")
    save(f, P, "junction_depth")

    # 6. 확산계수 Arrhenius
    Ts = np.linspace(800, 1200, 50)
    f, ax = plot_ax(7.0, 4.2)
    for (el, c) in zip(("B", "P", "As", "Sb"), PAL):
        ax.semilogy(1000 / (Ts + 273.15), [D(el, T) for T in Ts], color=c, lw=2.2, label=el)
    ax.set_xlabel("1000 / T (1/K)")
    ax.set_ylabel("확산계수 D (cm²/s)")
    ax.set_title("진성 확산계수 (도핑이 낮을 때): B, P가 빠르고 As, Sb가 느림", loc="left", fontsize=11)
    ax.legend()
    sec = ax.secondary_xaxis("top", functions=(lambda v: 1000 / v - 273.15, lambda v: 1000 / (v + 273.15)))
    sec.set_xlabel("°C")
    save(f, P, "diffusivity")
