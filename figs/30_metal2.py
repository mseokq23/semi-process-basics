import numpy as np
from common import *

P = 30


def lined_hole(ax, x0, x1, ybot, ytop, t, c, X0=0.0, X1=10.0, z=4, lw=0.6):
    """구멍 안팎을 두께 t로 고르게 덮는 막"""
    outer = [(X0, ytop), (x0, ytop), (x0, ybot), (x1, ybot), (x1, ytop), (X1, ytop)]
    inner = [(X1, ytop + t), (x1 - t, ytop + t), (x1 - t, ybot + t), (x0 + t, ybot + t),
             (x0 + t, ytop + t), (X0, ytop + t)]
    poly(ax, outer + inner, c, z=z, lw=lw)


# 1. 금속 비저항
metals = [("Ag", 1.59, "가장 낮지만 부식, 확산 문제"), ("Cu", 1.68, "지금 배선 주력 (31편)"),
          ("Al", 2.65, "예전 배선, 지금은 pad"), ("W", 5.3, "contact plug"), ("Mo", 5.3, "차세대 후보"),
          ("Co", 6.2, "가는 배선, contact 일부"), ("Ru", 7.1, "차세대 후보"), ("Ti", 42, "접착층, barrier (TiN)")]
f, ax = plot_ax(8.4, 4.0)
ax.grid(False)
for i, (m, r, s) in enumerate(metals):
    y = len(metals) - 1 - i
    c = C["cu"] if m == "Cu" else (C["al"] if m == "Al" else (C["w"] if m == "W" else "#b0bec5"))
    ax.barh(y, r, color=c, edgecolor="#333333", lw=0.6, height=0.62)
    ax.text(r + 0.6, y, f"{r:g}   {s}", va="center", fontsize=9.2)
ax.set_yticks(range(len(metals)))
ax.set_yticklabels([m[0] for m in metals][::-1], fontsize=11)
ax.set_xlim(0, 75)
ax.set_xlabel("bulk 비저항 (µΩ·cm, 상온 대략값)")
ax.set_title("배선, contact에 쓰는 금속의 비저항", loc="left", fontsize=11)
save(f, P, "resistivity_bars")

# 2. Al spiking
f, axs = panels(2, 2, 5.4, 3.7, (0, 10), (-3.6, 3.2), titles=["Al을 Si에 바로 붙이면: spike가 접합을 뚫음",
                                                            "barrier(Ti/TiN)를 깔면: Si와 Al이 안 섞임"], size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0, -3.6, 10, 3.6, "pw", lw=0.6)
    rect(ax, 2.0, -0.7, 6.0, 0.7, "np", lw=0.6)
    rect(ax, 0, 0, 3.5, 1.2, "ox", lw=0.6)
    rect(ax, 6.5, 0, 3.5, 1.2, "ox", lw=0.6)
    if k == 0:
        poly(ax, [(0, 1.2), (3.5, 1.2), (3.5, 0), (6.5, 0), (6.5, 1.2), (10, 1.2), (10, 2.3), (0, 2.3)], "al", lw=0.7, z=4)
        for (x, d) in [(4.1, 1.6), (5.0, 1.1), (5.8, 1.9)]:
            poly(ax, [(x - 0.35, 0.0), (x + 0.35, 0.0), (x + 0.05, -d), (x - 0.1, -d)], "al", lw=0.7, z=4.2)
        text(ax, 8.4, -1.6, "n⁺ 접합을 뚫고\np형까지 → 단락", size=9.2, color=C["red"])
        text(ax, 5.0, 1.75, "Al", size=10, weight="bold")
        for (x, y) in [(4.4, 0.55), (5.3, 0.75), (5.9, 0.45)]:
            arrow(ax, x, y - 0.35, x, y + 0.2, color=C["blue"], lw=1.0, ms=7, z=6)
        text(ax, 2.0, 2.75, "Si가 Al 속으로 녹아 나감 (400 °C 이상)", size=8.8, color=C["blue"], ha="left")
    else:
        poly(ax, [(0, 1.2), (3.5, 1.2), (3.5, 0), (6.5, 0), (6.5, 1.2), (10, 1.2), (10, 1.45), (6.75, 1.45),
                  (6.75, 0.25), (3.25 + 0.0, 0.25), (3.25, 1.45), (0, 1.45)], "tin", lw=0.6, z=4.5)
        poly(ax, [(0, 1.45), (3.25, 1.45), (3.25, 0.25), (6.75, 0.25), (6.75, 1.45), (10, 1.45), (10, 2.4),
                  (0, 2.4)], "al", lw=0.7, z=4)
        text(ax, 5.0, 1.85, "Al", size=10, weight="bold")
        text(ax, 5.0, -0.35, "n⁺", size=9.5)
        text(ax, 8.4, 2.85, "Ti/TiN barrier", size=9.2, color=C["tin"], weight="bold")
    text(ax, 1.5, -2.6, "p형 Si", size=9.5)
save(f, P, "al_spiking")

# 3. electromigration
f, axs = plt.subplots(2, 1, figsize=(10.5, 5.6))
rng = np.random.default_rng(7)
for k, ax in enumerate(axs):
    canvas(0, 0, (-1.5, 17.5), (-1.6, 2.9), ax=ax)
    rect(ax, 0, 0, 16, 1.4, "al", lw=0.8)
    if k == 0:
        ax.set_title("넓은 배선 (결정립이 여러 개): 결정립 경계를 따라 원자가 쓸려감", loc="left", fontsize=10.5)
        xs = np.linspace(0.8, 15.2, 13)
        for x in xs:
            pts = [(x + rng.uniform(-0.4, 0.4), 0.0), (x + rng.uniform(-0.5, 0.5), 0.7),
                   (x + rng.uniform(-0.4, 0.4), 1.4)]
            ax.plot(*zip(*pts), color="#5f6b78", lw=0.9, zorder=5)
            ax.plot([pts[1][0], pts[1][0] + rng.uniform(0.5, 1.0)], [0.7, 0.7 + rng.choice([-0.7, 0.7])],
                    color="#5f6b78", lw=0.9, zorder=5)
        # void, hillock
        ax.add_patch(Ellipse((1.6, 0.8), 1.2, 0.8, fc="white", ec="#333333", lw=0.8, zorder=6))
        text(ax, 1.6, -0.55, "void (끊어짐)", size=9.5, color=C["red"], weight="bold")
        poly(ax, [(13.6, 1.4), (14.0, 2.1), (14.6, 2.3), (15.0, 1.4)], "al", lw=0.8, z=6)
        text(ax, 14.3, -0.55, "hillock (튀어나옴)", size=9.5, color=C["red"], weight="bold")
        for x in (4.5, 7.5, 10.5):
            arrow(ax, x, 1.0, x + 1.6, 1.0, color=C["red"], lw=1.5, ms=10, z=8)
        text(ax, 9.0, 2.35, "Al 원자 이동 (전자에 떠밀림)", size=9.5, color=C["red"])
    else:
        ax.set_title("좁은 배선 (대나무 구조) + Cu 첨가: 이어진 경계가 없어서 원자 이동이 느림", loc="left", fontsize=10.5)
        for x in np.arange(1.6, 16, 2.4):
            xa = x + rng.uniform(-0.3, 0.3)
            xb = xa + rng.uniform(-0.3, 0.3)
            ax.plot([xa, xb], [0, 1.4], color="#5f6b78", lw=0.9, zorder=5)
            for fy in (0.2, 0.5, 0.8, 1.1):
                circ(ax, xa + (xb - xa) * fy / 1.4 * 1.4, fy, 0.09, C["cu"], lw=0.2, z=6)
        text(ax, 8.0, 2.3, "결정립 경계가 배선을 가로지르기만 함, 점: 경계에 모인 Cu", size=9.5)
    arrow(ax, 4.0, -1.2, 12.0, -1.2, color=C["blue"], lw=1.4, ms=10)
    text(ax, 8.0, -0.85, "전자 흐름 → (전류는 반대 방향)", size=9.2, color=C["blue"])
    text(ax, -0.8, 0.7, "−", size=14, weight="bold")
    text(ax, 16.8, 0.7, "+", size=14, weight="bold")
plt.tight_layout()
save(f, P, "em_mechanism")

# 4. Black 식
J = np.logspace(np.log10(0.5), np.log10(5), 100)
KB = 8.617e-5
Ea, n = 0.7, 2


def mttf(J, Tc):
    return J ** (-n) * np.exp(Ea / (KB * (Tc + 273.15)))


ref = mttf(1.0, 105)
f, ax = plot_ax(7.2, 4.2)
for Tc, c in [(85, PAL[0]), (105, PAL[3]), (125, PAL[1])]:
    ax.loglog(J, mttf(J, Tc) / ref, color=c, lw=2.2, label=f"{Tc} °C")
ax.plot([1.0], [1.0], "o", color="#222222")
ax.text(1.05, 1.25, "기준", fontsize=9)
ax.set_xticks([0.5, 1, 2, 5])
ax.set_xticklabels(["0.5", "1", "2", "5"])
ax.minorticks_off()
ax.set_xlabel("전류 밀도 J (MA/cm²)")
ax.set_ylabel("상대 수명 (MTTF)")
ax.set_title("Black 식: 전류 밀도 2배 → 수명 1/4, 온도 20 °C ↑ → 수명 약 1/3 (Ea 0.7 eV, n 2)",
             loc="left", fontsize=10)
ax.legend(fontsize=9.5)
save(f, P, "black_eq")

# 5. Al 배선 만드는 순서 (식각 방식)
tt = ["① W plug까지 완성된 절연막", "② Ti/TiN + Al-Cu + TiN 연속 증착 (PVD)", "③ photo: 배선 모양으로 PR",
      "④ 염소 계열 plasma로 금속 식각", "⑤ PR 제거 + 부식 방지 처리", "⑥ 절연막(IMD)으로 채우고 CMP"]
f, axs = panels(6, 3, 4.1, 2.75, (0, 10), (-0.6, 5.0), titles=tt, size=10)
L = [(1.6, 3.4), (6.6, 8.4)]
for k, ax in enumerate(axs):
    rect(ax, 0, -0.6, 10, 0.6, "sub", lw=0.5)
    rect(ax, 0, 0, 10, 2.0, "ox", lw=0.6)
    for x in (2.5, 7.5):
        rect(ax, x - 0.3, 0, 0.6, 2.0, "w", lw=0.5, z=3)
    if k == 1:
        rect(ax, 0, 2.0, 10, 0.15, "tin", lw=0.5)
        rect(ax, 0, 2.15, 10, 1.0, "al", lw=0.6)
        rect(ax, 0, 3.15, 10, 0.12, "tin", lw=0.5)
        text(ax, 5.0, 2.65, "Al-Cu", size=9)
    if k == 2:
        rect(ax, 0, 2.0, 10, 0.15, "tin", lw=0.5)
        rect(ax, 0, 2.15, 10, 1.0, "al", lw=0.6)
        rect(ax, 0, 3.15, 10, 0.12, "tin", lw=0.5)
        for a, b in L:
            rect(ax, a, 3.27, b - a, 0.9, "pr", lw=0.6)
    if k >= 3:
        for a, b in L:
            rect(ax, a, 2.0, b - a, 0.15, "tin", lw=0.5, z=4)
            rect(ax, a, 2.15, b - a, 1.0, "al", lw=0.6, z=4)
            rect(ax, a, 3.15, b - a, 0.12, "tin", lw=0.5, z=4)
            if k == 3:
                rect(ax, a, 3.27, b - a, 0.6, "pr", lw=0.6)
    if k == 3:
        for x in np.arange(0.4, 10, 0.6):
            if not any(a - 0.1 < x < b + 0.1 for a, b in L):
                arrow(ax, x, 4.6, x, 3.4, color="#555555", lw=0.9, ms=6)
        text(ax, 5.0, 4.5, "Cl₂ + BCl₃", size=9, color="#444444", box="white")
    if k == 4:
        text(ax, 5.0, 4.1, "남은 Cl을 빨리 없애야 Al이 안 부식됨 (18편)", size=8.6, color=C["red"])
    if k == 5:
        rect(ax, 0, 2.0, 10, 2.0, "ox", lw=0.6, z=3.5)
        for a, b in L:
            rect(ax, a, 2.0, b - a, 0.15, "tin", lw=0.5, z=4)
            rect(ax, a, 2.15, b - a, 1.0, "al", lw=0.6, z=4)
            rect(ax, a, 3.15, b - a, 0.12, "tin", lw=0.5, z=4)
save(f, P, "al_flow")

# 6. contact 채우기: PVD Al vs CVD W
f, axs = panels(2, 2, 4.8, 3.9, (0, 10), (-1.2, 6.2), titles=["PVD Al: 입구가 먼저 막혀서 속이 빔",
                                                            "CVD W: 사방에서 고르게 자라서 꽉 참"], size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0, -1.2, 10, 1.2, "sil", lw=0.5)
    rect(ax, 0, 0, 4.2, 4.5, "ox", lw=0.6)
    rect(ax, 5.8, 0, 4.2, 4.5, "ox", lw=0.6)
    if k == 0:
        poly(ax, [(0, 4.5), (4.2, 4.5), (4.2, 3.6), (4.65, 4.0), (4.85, 4.6), (5.15, 4.6), (5.35, 4.0),
                  (5.8, 3.6), (5.8, 4.5), (10, 4.5), (10, 5.5), (0, 5.5)], "al", lw=0.7, z=4)
        poly(ax, [(4.2, 0.0), (5.8, 0.0), (5.8, 0.25), (5.4, 0.35), (4.6, 0.35), (4.2, 0.25)], "al", lw=0.6, z=4)
        poly(ax, [(4.2, 0.3), (4.36, 0.3), (4.3, 3.4), (4.2, 3.5)], "al", lw=0.5, z=4)
        poly(ax, [(5.8, 0.3), (5.64, 0.3), (5.7, 3.4), (5.8, 3.5)], "al", lw=0.5, z=4)
        text(ax, 5.0, 2.0, "void", size=9.5, color=C["red"], weight="bold")
        text(ax, 7.9, 5.95, "윗부분이 튀어나와 입구를 막음", size=8.8, color="#444444")
    else:
        rect(ax, 4.2, 0, 1.6, 4.5, "tin", lw=0.5, z=4)
        rect(ax, 4.3, 0.1, 1.4, 4.4, "w", lw=0.5, z=4.1)
        rect(ax, 0, 4.5, 10, 0.1, "tin", lw=0.5, z=4)
        rect(ax, 0, 4.6, 10, 0.8, "w", lw=0.5, z=4)
        line(ax, [5.0, 5.0], [1.0, 4.4], color="#2b2b2b", lw=0.8, ls=":", z=6)
        text(ax, 6.6, 2.4, "가운데 얇은\nseam은 남을 수 있음", size=8.6, color="#444444", ha="left")
    text(ax, 2.0, -0.6, "silicide", size=9, color="white")
save(f, P, "al_vs_w_fill")

# 7. W plug 단계
tt = ["① contact 식각 (silicide까지)", "② Ti (PVD) + TiN (CVD / ALD)", "③ W 핵 생성층 (WF₆ + SiH₄ / B₂H₆)",
      "④ W 본 증착 (WF₆ + H₂)", "⑤ W CMP → plug"]
f, axs = panels(5, 3, 3.9, 3.3, (0, 10), (-1.2, 6.0), titles=tt, size=10)
x0, x1, yb, yt = 4.2, 5.8, 0.0, 4.5
T1, T2 = 0.18, 0.16
for k, ax in enumerate(axs):
    rect(ax, 0, -1.2, 10, 1.2, "np", lw=0.5)
    rect(ax, 0, -0.18, 10, 0.18, "sil", lw=0.5, z=2.5)
    poly(ax, [(0, 0), (x0, 0), (x0, yt), (x1, yt), (x1, 0), (10, 0), (10, yt), (0, yt)], "ox", lw=0.6)
    rect(ax, 0, 0, x0, yt, "ox", lw=0.6)
    rect(ax, x1, 0, 10 - x1, yt, "ox", lw=0.6)
    if k in (1, 2, 3):
        lined_hole(ax, x0, x1, yb, yt, T1, "tin")
    if k in (2, 3):
        lined_hole(ax, x0 + T1, x1 - T1, yb + T1, yt + T1, T2, "#5f6b78", X0=0, X1=10, z=4.2)
    if k == 3:
        rect(ax, x0 + T1 + T2, yb + T1 + T2, (x1 - x0) - 2 * (T1 + T2), yt - yb, "w", lw=0.5, z=4.1)
        rect(ax, 0, yt + T1 + T2, 10, 0.7, "w", lw=0.6, z=4.1)
    if k == 4:
        rect(ax, x0, yb, x1 - x0, yt - yb, "tin", lw=0.5, z=4)
        rect(ax, x0 + T1, yb + T1, x1 - x0 - 2 * T1, yt - yb - T1, "w", lw=0.5, z=4.1)
    if k == 1:
        text(ax, 7.9, 5.3, "Ti: 접착, 산화막 제거\nTiN: F 차단", size=8.8, color=C["tin"])
    if k == 2:
        text(ax, 7.9, 5.3, "얇게 먼저 깔아서\nW가 고르게 자라게", size=8.8, color="#444444")
    if k == 3:
        text(ax, 7.9, 5.75, "빠르게 채움", size=8.8, color="#444444")
    if k == 4:
        text(ax, 7.9, 5.3, "위쪽 W, TiN을 갈아내고\n구멍 안만 남김", size=8.8, color="#444444")
    text(ax, 1.4, -0.65, "n⁺", size=9, color="white")
save(f, P, "w_plug_steps")
