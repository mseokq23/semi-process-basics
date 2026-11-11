import numpy as np
from common import *

P = 7
KB = 8.617e-5  # eV/K

# Deal-Grove 상수 (Si (111) 기준, (100)은 B/A를 1.68로 나눔)
DG = {"dry": dict(C1=7.72e2, E1=1.23, C2=6.23e6, E2=2.00),
      "wet": dict(C1=3.86e2, E1=0.78, C2=1.63e8, E2=2.05)}


def consts(kind, T_c, orient="100"):
    T = T_c + 273.15
    d = DG[kind]
    B = d["C1"] * np.exp(-d["E1"] / (KB * T))           # um^2/h
    BA = d["C2"] * np.exp(-d["E2"] / (KB * T))          # um/h
    if orient == "100":
        BA /= 1.68
    return B, BA


def thickness(kind, T_c, t_h, orient="100", tau=0.0):
    B, BA = consts(kind, T_c, orient)
    A = B / BA
    return (-A + np.sqrt(A ** 2 + 4 * B * (t_h + tau))) / 2   # um


def time_for(kind, T_c, x_um, orient="100"):
    B, BA = consts(kind, T_c, orient)
    return (x_um ** 2 + (B / BA) * x_um) / B


if __name__ == "__main__":
    print("T(C)  kind  B(um^2/h)   B/A(um/h)   x(1h, nm)")
    for kind in ("dry", "wet"):
        for T in (900, 1000, 1100):
            B, BA = consts(kind, T)
            print(f"{T:5d}  {kind}  {B:.3e}  {BA:.3e}  {thickness(kind, T, 1.0) * 1e3:8.1f}")
    print("dry 1000C, 10 nm:", round(time_for("dry", 1000, 0.010) * 60, 1), "min")
    print("wet 1000C, 500 nm:", round(time_for("wet", 1000, 0.5), 2), "h")
    print("dry 1000C, 500 nm:", round(time_for("dry", 1000, 0.5), 1), "h")

    # 1. 시간-두께 곡선
    t = np.logspace(-1.5, 1.3, 200)
    f, axs = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True)
    for ax, kind, name in zip(axs, ("dry", "wet"), ("건식 (O₂)", "습식 (H₂O)")):
        for T, c in zip((900, 1000, 1100, 1200), PAL):
            ax.plot(t, thickness(kind, T, t) * 1e3, color=c, lw=2, label=f"{T} °C")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("산화 시간 (h)")
        ax.set_title(f"{name}, Si (100)", loc="left")
        ax.grid(alpha=0.25, which="both", lw=0.5)
        ax.legend(fontsize=9.5)
    axs[0].set_ylabel("산화막 두께 (nm)")
    axs[0].set_ylim(1, 5000)
    plt.tight_layout()
    save(f, P, "dealgrove_curves")

    # 2. 선형 / 포물선 구간
    B, BA = consts("wet", 1000)
    A = B / BA
    t = np.logspace(-3, 2, 300)
    x = thickness("wet", 1000, t) * 1e3
    f, ax = plot_ax(6.6, 4.4)
    ax.plot(t, x, color="#222222", lw=2.5, label="Deal-Grove 식")
    ax.plot(t, BA * t * 1e3, "--", color=PAL[0], lw=1.6, label="x ≈ (B/A)·t  (반응이 결정)")
    ax.plot(t, np.sqrt(B * t) * 1e3, "--", color=PAL[1], lw=1.6, label="x ≈ √(B·t)  (확산이 결정)")
    ax.axvline(A ** 2 / B, color="#999999", lw=0.8, ls=":")
    ax.text(A ** 2 / B * 1.15, 3, "t ≈ A²/B", fontsize=9, color="#666666")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1, 1e4)
    ax.set_xlabel("산화 시간 (h)")
    ax.set_ylabel("두께 (nm)")
    ax.set_title("습식 1000 °C: 얇을 땐 선형, 두꺼워지면 포물선", loc="left")
    ax.legend(fontsize=9)
    save(f, P, "linear_parabolic")

    # 3. 결정면, 온도 의존성
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.3))
    t = np.linspace(0, 6, 200)
    for o, c in zip(("111", "100"), PAL):
        ax1.plot(t, thickness("dry", 1000, t, orient=o) * 1e3, color=c, lw=2, label=f"Si ({o})")
    ax1.set_xlabel("시간 (h)")
    ax1.set_ylabel("두께 (nm)")
    ax1.set_title("건식 1000 °C: (111)이 더 빠름", loc="left")
    ax1.legend()
    ax1.grid(alpha=0.25)
    Ts = np.linspace(850, 1200, 50)
    inv = 1000 / (Ts + 273.15)
    for kind, ls in (("dry", "-"), ("wet", "--")):
        Bv = np.array([consts(kind, T)[0] for T in Ts])
        BAv = np.array([consts(kind, T)[1] for T in Ts])
        nm = "건식" if kind == "dry" else "습식"
        ax2.plot(inv, Bv, ls, color=PAL[2], lw=2, label=f"B ({nm})")
        ax2.plot(inv, BAv, ls, color=PAL[3], lw=2, label=f"B/A ({nm})")
    ax2.set_yscale("log")
    ax2.set_xlabel("1000 / T (1/K)")
    ax2.set_ylabel("µm²/h (B),  µm/h (B/A)")
    ax2.set_title("온도가 오르면 둘 다 지수적으로 커짐", loc="left", pad=28)
    ax2.legend(fontsize=9, ncol=2)
    ax2.grid(alpha=0.25, which="both", lw=0.5)
    sec = ax2.secondary_xaxis("top", functions=(lambda v: 1000 / v - 273.15, lambda v: 1000 / (v + 273.15)))
    sec.set_xlabel("°C")
    plt.tight_layout()
    save(f, P, "factors")

    # 4. 산화막 전하
    f, ax = canvas(9.0, 4.8, (0, 16), (-0.6, 8.2))
    rect(ax, 0.5, 0, 15, 2.6, "si", lw=0.8)
    rect(ax, 0.5, 2.6, 15, 3.4, "ox", lw=0.8)
    rect(ax, 0.5, 6.0, 15, 1.4, "poly", lw=0.8)
    text(ax, 8.0, 6.7, "게이트", size=10)
    text(ax, 8.0, 1.0, "Si", size=10)
    rng = np.random.default_rng(5)
    for x, y in zip(rng.uniform(1.2, 4.5, 6), rng.uniform(3.3, 5.5, 6)):
        text(ax, x, y, "Na⁺", size=8.5, color=C["red"], weight="bold")
    for x, y, s in zip(rng.uniform(5.3, 9.0, 6), rng.uniform(3.6, 5.6, 6), "+−+−++"):
        text(ax, x, y, s, size=11, color=C["purple"], weight="bold")
    for x in np.arange(9.8, 12.8, 0.55):
        text(ax, x, 2.95, "+", size=11, color=C["blue"], weight="bold")
    for x in np.arange(13.0, 15.3, 0.45):
        text(ax, x, 2.6, "×", size=11, color=C["green"], weight="bold")
    for (x, s, c) in [(2.8, "Qm 이동 이온\n(Na⁺, K⁺)", "red"), (7.2, "Qot 산화막에\n갇힌 전하", "purple"),
                      (11.3, "Qf 계면 근처\n고정 전하", "blue"), (14.2, "Qit 계면\n트랩", "green")]:
        text(ax, x, -0.25, s, size=9, color=C[c], va="top")
    f.subplots_adjust(bottom=0.25)
    save(f, P, "oxide_charges")

    # 5. LOCOS vs STI
    f, axs = panels(2, 2, 6.0, 3.6, (0, 12), (-2.8, 3.4),
                    titles=["LOCOS: 질화막 밑으로 산화막이 파고듦 (버즈비크)", "STI: 홈을 파고 산화막으로 채움"],
                    size=10.5)
    ax = axs[0]
    rect(ax, 0, -2.6, 12, 2.6, "si", lw=0.8)
    xs = np.linspace(3.0, 9.0, 200)
    top = 0.55 + 0.55 * (1 - np.exp(-((xs - 3.0) / 0.6) ** 2)) * (1 - np.exp(-((xs - 9.0) / 0.6) ** 2))
    bot = -0.45 - 0.45 * (1 - np.exp(-((xs - 3.0) / 0.6) ** 2)) * (1 - np.exp(-((xs - 9.0) / 0.6) ** 2))
    xx = np.r_[2.2, xs, 9.8]
    tt_ = np.r_[0.06, top, 0.06]
    bb = np.r_[-0.02, bot, -0.02]
    poly(ax, list(zip(xx, tt_)) + list(zip(xx[::-1], bb[::-1])), "ox", lw=0.8, z=3)
    rect(ax, 0, 0, 2.6, 0.12, "ox", lw=0.5)
    rect(ax, 9.4, 0, 2.6, 0.12, "ox", lw=0.5)
    poly(ax, [(0, 0.12), (2.6, 0.12), (3.1, 0.6), (3.1, 1.1), (2.6, 0.72), (0, 0.72)], "nit", lw=0.7, z=4)
    poly(ax, [(12, 0.12), (9.4, 0.12), (8.9, 0.6), (8.9, 1.1), (9.4, 0.72), (12, 0.72)], "nit", lw=0.7, z=4)
    text(ax, 6.0, 0.2, "필드 산화막", size=9.5)
    arrow(ax, 2.3, 2.4, 2.75, 0.3, lw=0.8, ms=7)
    text(ax, 2.3, 2.7, "버즈비크 (새 부리)", size=9)
    text(ax, 1.2, -1.6, "Active", size=9.5)
    text(ax, 10.8, -1.6, "Active", size=9.5)
    ax = axs[1]
    rect(ax, 0, -2.6, 12, 2.6, "si", lw=0.8)
    rect(ax, 4.0, -1.8, 4.0, 1.85, "ox", lw=0.8)
    text(ax, 6.0, -0.9, "SiO₂", size=9.5)
    text(ax, 2.0, -1.6, "Active", size=9.5)
    text(ax, 10.0, -1.6, "Active", size=9.5)
    text(ax, 6.0, 1.6, "표면이 평평하고, 옆으로 먹어 들어가는 게 없음", size=9.5)
    save(f, P, "locos_vs_sti")
