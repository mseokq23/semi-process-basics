import numpy as np
from common import *

P = 15

# 1. plasma 속 입자
f, ax = canvas(9, 5.0, (0, 18), (0, 10))
ax.add_patch(FancyBboxPatch((0.5, 0.5), 17, 9, boxstyle="round,pad=0,rounding_size=0.8",
                            fc="#f3e5f5", ec="#9575cd", lw=1.4, zorder=0))
rng = np.random.default_rng(4)
for _ in range(40):
    x, y = rng.uniform(1.2, 16.8), rng.uniform(1.2, 8.8)
    circ(ax, x, y, 0.32, "#cfd8dc", lw=0.4)
for _ in range(9):
    x, y = rng.uniform(1.5, 16.5), rng.uniform(1.5, 8.5)
    circ(ax, x, y, 0.32, "#ef9a9a", lw=0.5, z=4)
    text(ax, x, y, "+", size=9, weight="bold", z=5)
for _ in range(9):
    x, y = rng.uniform(1.5, 16.5), rng.uniform(1.5, 8.5)
    circ(ax, x, y, 0.12, C["blue"], ec=C["blue"], z=5)
    a = rng.uniform(0, 2 * np.pi)
    arrow(ax, x, y, x + 1.3 * np.cos(a), y + 1.3 * np.sin(a), color="blue", lw=1.0, ms=7)
for _ in range(8):
    x, y = rng.uniform(1.5, 16.5), rng.uniform(1.5, 8.5)
    circ(ax, x, y, 0.3, "#a5d6a7", lw=0.5, z=4)
    text(ax, x + 0.35, y + 0.3, "*", size=10, color=C["green"], weight="bold", z=5)
legend_items = [("#cfd8dc", "중성 기체 (대부분)"), ("#ef9a9a", "ion (+)"), (C["blue"], "전자 (가볍고 빠름)"),
                ("#a5d6a7", "radical (반응성 큰 중성 조각)")]
hs = [Circle((0, 0), 1, fc=c, ec="#333333") for c, _ in legend_items]
ax.legend(hs, [s for _, s in legend_items], loc="upper center", bbox_to_anchor=(0.5, -0.0), ncol=4, fontsize=9.5)
save(f, P, "plasma_particles")

# 2. 전자 충돌 반응
tt = ["ion화: e + Ar → Ar⁺ + 2e", "여기, 발광: e + Ar → Ar* → Ar + 빛", "해리: e + CF₄ → CF₃ + F + e"]
f, axs = panels(3, 3, 4.0, 2.6, (0, 10), (0, 5.4), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    circ(ax, 0.8, 2.7, 0.15, C["blue"], ec=C["blue"])
    arrow(ax, 1.0, 2.7, 3.2, 2.7, color="blue", lw=1.4)
    if k == 2:
        circ(ax, 4.2, 2.7, 0.55, "#cfd8dc", lw=0.5)
        for a in (0, 90, 180, 270):
            circ(ax, 4.2 + 0.85 * np.cos(np.deg2rad(a)), 2.7 + 0.85 * np.sin(np.deg2rad(a)), 0.3, "#a5d6a7", lw=0.4)
    else:
        circ(ax, 4.2, 2.7, 0.6, "#cfd8dc", lw=0.5)
        text(ax, 4.2, 2.7, "Ar", size=9.5)
    arrow(ax, 5.4, 2.7, 6.4, 2.7, lw=1.2)
    if k == 0:
        circ(ax, 7.6, 2.7, 0.6, "#ef9a9a", lw=0.5)
        text(ax, 7.6, 2.7, "Ar⁺", size=9.5)
        for y in (1.4, 4.0):
            circ(ax, 9.0, y, 0.15, C["blue"], ec=C["blue"])
        text(ax, 7.6, 0.6, "plasma를 유지하는 반응", size=9)
    elif k == 1:
        circ(ax, 7.6, 2.7, 0.6, "#fff59d", lw=0.5)
        text(ax, 7.6, 2.7, "Ar*", size=9.5)
        xs = np.linspace(8.3, 9.7, 40)
        ax.plot(xs, 3.6 + 0.15 * np.sin(xs * 18), color=C["purple"], lw=1.2)
        text(ax, 7.6, 0.6, "plasma가 빛나는 이유 (OES로 분석)", size=9)
    else:
        circ(ax, 7.4, 2.9, 0.5, "#cfd8dc", lw=0.5)
        text(ax, 7.4, 2.9, "CF₃", size=8.5)
        circ(ax, 8.9, 2.0, 0.35, "#a5d6a7", lw=0.5)
        text(ax, 8.9, 2.0, "F", size=9)
        text(ax, 7.6, 0.6, "식각에 쓰는 radical(F)이 생김", size=9)
save(f, P, "collisions")

# 3. Paschen 곡선
pd = np.logspace(-1, 2, 400)      # Torr·cm
f, ax = plot_ax(7.2, 4.4)
for (name, A, B), c in zip([("Ar", 12, 180), ("N₂", 12, 342), ("공기", 15, 365)], PAL):
    g = 0.01
    den = np.log(A * pd) - np.log(np.log(1 + 1 / g))
    V = np.where(den > 0, B * pd / den, np.nan)
    ax.plot(pd, V, color=c, lw=2.2, label=name)
    k = np.nanargmin(V)
    ax.plot(pd[k], V[k], "o", color=c)
    print(f"{name}: Vmin = {V[k]:.0f} V at pd = {pd[k]:.2f} Torr cm")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(100, 1e4)
ax.set_xlabel("압력 × 전극 간격, pd (Torr·cm)")
ax.set_ylabel("방전 시작 전압 (V)")
ax.text(0.13, 5000, "압력이 너무 낮음:\n전자가 부딪힐\n기체가 부족", fontsize=9, color="#555555")
ax.text(18, 3500, "압력이 너무 높음:\n충분히 가속되기 전에\n부딪힘", fontsize=9, color="#555555")
ax.set_title("Paschen 곡선 (Townsend 식, A·B는 교과서 근사값, γ = 0.01)", loc="left", fontsize=11)
ax.legend()
save(f, P, "paschen")

# 4. sheath와 전위 분포
x = np.linspace(0, 10, 500)


def prof(x, s1, s2, v1, v2, vp):
    y = np.full_like(x, vp)
    m1 = x < s1
    y[m1] = v1 + (vp - v1) * (x[m1] / s1) ** (4 / 3)
    m2 = x > 10 - s2
    y[m2] = v2 + (vp - v2) * ((10 - x[m2]) / s2) ** (4 / 3)
    return y


f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.2))
ax1.plot(x, prof(x, 0.8, 0.8, 0, 0, 20), color="#222222", lw=2.2)
ax1.axvspan(0, 0.8, color="#ffcdd2", alpha=0.6)
ax1.axvspan(9.2, 10, color="#ffcdd2", alpha=0.6)
ax1.text(5, 21.5, "plasma: 전위 일정 (Vp)", ha="center", fontsize=10)
ax1.text(0.4, 3, "sheath", ha="center", fontsize=9.5)
ax1.text(9.6, 3, "sheath", ha="center", fontsize=9.5)
ax1.set_ylim(-2, 26)
ax1.set_xlabel("위치 (전극 ↔ 전극)")
ax1.set_ylabel("전위 (V)")
ax1.set_title("양쪽 전극이 접지일 때", loc="left")
ax1.grid(alpha=0.25)
ax2.plot(x, prof(x, 2.2, 0.8, -300, 0, 20), color="#222222", lw=2.2)
ax2.axvspan(0, 2.2, color="#ffcdd2", alpha=0.6)
ax2.axvspan(9.2, 10, color="#ffcdd2", alpha=0.6)
ax2.text(3.0, -110, "두꺼운 sheath: ion이 여기서 크게 가속", ha="left", fontsize=9.5)
ax2.text(4.3, -260, "← ion이 wafer로 수직 충돌", fontsize=9.5, color=C["red"])
ax2.set_xlabel("위치 (작은 RF 전극 = wafer ↔ 큰 접지 전극)")
ax2.set_ylabel("전위 (V)")
ax2.set_title("작은 전극에 RF + blocking capacitor (self-bias)", loc="left", fontsize=11)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "sheath")

# 5. self-bias
t = np.linspace(0, 3, 600)
Vrf, Vp = 300, 20
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.0))
ax1.plot(t, Vrf * np.sin(2 * np.pi * t), "--", color="#999999", lw=1.4, label="capacitor 없을 때")
Vdc = Vrf - 15
ax1.plot(t, -Vdc + Vrf * np.sin(2 * np.pi * t), color=PAL[0], lw=2.2, label="self-bias 생긴 뒤")
ax1.axhline(-Vdc, color=PAL[1], lw=1.2)
ax1.text(2.05, -Vdc + 20, "평균 = −Vdc", color=PAL[1], fontsize=10)
ax1.axhline(Vp, color=C["green"], lw=1.0, ls=":")
ax1.text(0.02, Vp + 15, "plasma 전위", color=C["green"], fontsize=9.5)
ax1.set_xlabel("시간 (RF 주기)")
ax1.set_ylabel("전극 전압 (V)")
ax1.set_title("전자가 더 많이 들어오니까 전극이 (−)로 충전됨", loc="left", fontsize=11)
ax1.legend(fontsize=9, loc="lower right")
ax1.grid(alpha=0.25)
r = np.linspace(1, 5, 100)
for n, c in zip((1, 2, 4), PAL):
    ax2.plot(r, r ** n, color=c, lw=2, label=f"n = {n}")
ax2.set_yscale("log")
ax2.set_xlabel("면적비 A_접지 / A_RF")
ax2.set_ylabel("sheath 전압비 V_RF / V_접지")
ax2.set_title("작은 전극 쪽 sheath 전압이 훨씬 큼 (V ∝ 1/Aⁿ)", loc="left", fontsize=11)
ax2.text(1.2, 200, "이론 n = 4, 실험은 보통 1 ~ 2.5", fontsize=9.5)
ax2.legend()
ax2.grid(alpha=0.25, which="both", lw=0.5)
plt.tight_layout()
save(f, P, "self_bias")

# 6. CCP vs ICP
f, axs = panels(2, 2, 5.6, 4.8, (0, 10), (0, 9.9), titles=["CCP (평행판)", "ICP (유도 결합)"], size=11.5)
for k, ax in enumerate(axs):
    rect(ax, 0.6, 0.6, 8.8, 7.4, "#fafafa", lw=1.0)
    rect(ax, 2.0, 1.2, 6.0, 0.6, "#9e9e9e", lw=0.6)
    rect(ax, 2.6, 1.8, 4.8, 0.15, "si", lw=0.5)
    text(ax, 5.0, 1.45, "아래 전극 + wafer", size=8.8, color="white")
    ax.add_patch(Ellipse((5.0, 4.4), 6.6 if k == 0 else 7.2, 2.6 if k == 0 else 3.6,
                         fc="#e1bee7" if k == 0 else "#ce93d8", ec="none", alpha=0.8, zorder=1))
    circ(ax, 1.0, 0.0 + 1.5, 0.0, "white", lw=0)
    rect(ax, 0.2, 0.9, 1.0, 0.6, "#fff3e0", lw=0.6)
    text(ax, 0.7, 1.2, "RF", size=8.5)
    line(ax, [1.2, 2.0], [1.2, 1.2], lw=1.2)
    if k == 0:
        rect(ax, 2.0, 7.0, 6.0, 0.5, "#9e9e9e", lw=0.6)
        text(ax, 5.0, 7.25, "위 전극 (접지)", size=8.8, color="white")
        text(ax, 5.0, 4.4, "plasma\n10⁹ ~ 10¹⁰ cm⁻³", size=9.5)
        text(ax, 5.0, -0.3, "한 전원으로 밀도와 ion energy를 같이 정함\n(유전막 식각, PECVD)", size=9.2, va="top")
    else:
        rect(ax, 1.4, 8.0, 7.2, 0.4, "#b3e5fc", lw=0.6)
        text(ax, 5.0, 9.45, "유전체 창 위 coil (source RF)", size=8.8)
        for x in np.arange(2.0, 8.4, 1.0):
            circ(ax, x, 8.75, 0.18, "#e69138", lw=0.4)
        text(ax, 5.0, 4.4, "고밀도 plasma\n10¹¹ ~ 10¹² cm⁻³", size=9.5)
        text(ax, 0.7, 2.35, "bias", size=8.2)
        text(ax, 5.0, -0.3, "source: 밀도, bias: ion energy를 따로 조절\n(도체 식각, HDP-CVD)", size=9.2, va="top")
f.subplots_adjust(bottom=0.18)
save(f, P, "ccp_icp")
