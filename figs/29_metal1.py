import numpy as np
from common import *
import cmos

P = 29

# 1. 배선 층 구조
f, ax = canvas(11.5, 7.6, (0, 32), (-2.6, 19.2))
rect(ax, 0, -2.6, 24, 2.6, "sub", lw=0.6)
rect(ax, 0, 0, 24, 2.0, "ox", z=1.5, lw=0.6)
for gx in (3.0, 9.0, 15.0, 21.0):
    rect(ax, gx - 0.5, 0, 1.0, 0.7, "poly", lw=0.6)
    rect(ax, gx - 2.2, -0.45, 1.5, 0.45, "np", lw=0.5)
    rect(ax, gx + 0.7, -0.45, 1.5, 0.45, "np", lw=0.5)
    for xc in (gx - 1.45, gx + 1.45):
        rect(ax, xc - 0.2, 0, 0.4, 2.0, "w", lw=0.5, z=3)
y = 2.0
spans = {}
# (이름, 층 수, 선 두께, 선 폭, pitch, via 높이)
for name, nlev, t, w, pitch, vh in [("local", 3, 0.8, 0.8, 1.6, 0.45), ("mid", 2, 1.2, 1.4, 2.8, 0.6),
                                     ("global", 2, 2.2, 3.0, 6.0, 1.1)]:
    y_start = y
    for k in range(nlev):
        rect(ax, 0, y, 24, vh + t, "lowk" if name != "global" else "ox", z=1.5, lw=0.5)
        xs = np.arange(0.4, 24 - w, pitch)
        for j, x in enumerate(xs):
            rect(ax, x, y + vh, w, t, "cu", lw=0.5, z=3)
            if j % 2 == 0:
                vw = 0.4 if name == "local" else (0.6 if name == "mid" else 1.2)
                rect(ax, x + (w - vw) / 2, y, vw, vh, "cu", lw=0.4, z=3)
        y += vh + t
        rect(ax, 0, y, 24, 0.12, "nit", z=2, lw=0.4)
        y += 0.12
    spans[name] = (y_start, y)
rect(ax, 0, y, 24, 0.6, "nit", lw=0.6)
rect(ax, 8, y - 0.4, 8, 1.0, "al", lw=0.7, z=4)
text(ax, 12, y + 1.0, "pad (Al) + 보호막", size=9.5)
top = y + 0.6
labels = [(-2.6, 0.7, "FEOL: transistor"), (0.0, 2.0, "MOL: contact (W)"),
          (spans["local"][0], spans["local"][1], "local 배선\n(가늘고 촘촘)"),
          (spans["mid"][0], spans["mid"][1], "중간 배선"),
          (spans["global"][0], spans["global"][1], "global 배선\n(굵고 넓게: 전원, clock)")]
for (y0, y1, s_) in labels:
    ax.plot([24.5, 24.9, 24.9, 24.5], [y0 + 0.1, y0 + 0.1, y1 - 0.1, y1 - 0.1], color="#555555", lw=1.0)
    text(ax, 25.3, (y0 + y1) / 2, s_, size=9.3, ha="left")
ax.plot([30.3, 30.7, 30.7, 30.3], [2.1, 2.1, top - 0.1, top - 0.1], color=C["cu"], lw=1.4)
text(ax, 31.0, (2.0 + top) / 2, "BEOL", size=10.5, weight="bold", color=C["cu"], rotation=90)
legend(ax, ["cu", "lowk", "ox", "nit", "w", "al"], loc="upper center", ncol=6, size=9, bbox=(0.4, 0.0),
       names={"nit": "SiN / SiCN cap", "ox": "SiO₂"})
save(f, P, "interconnect_stack")

# 2. Schottky vs ohmic I-V
V = np.linspace(-0.6, 0.6, 400)
f, axs = plt.subplots(1, 2, figsize=(10.5, 3.6))
I_s = 1e-6 * (np.exp(V / 0.0259) - 1)
axs[0].plot(V, np.clip(I_s, -1, 1e-1) * 1e3, color=PAL[1], lw=2.2)
axs[0].set_ylim(-5, 60)
axs[0].set_title("Schottky 접합: 한쪽 방향만 잘 흐름 (diode)", loc="left", fontsize=11)
axs[1].plot(V, V / 10 * 1e3, color=PAL[0], lw=2.2)
axs[1].set_title("ohmic 접합: 양쪽으로 직선 (저항)", loc="left", fontsize=11)
for ax in axs:
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axvline(0, color="#999999", lw=0.8)
    ax.set_xlabel("전압 (V)")
    ax.set_ylabel("전류 (mA)")
    ax.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "iv_curves")

# 3. band 그림: 접촉 전 / Schottky / ohmic (금속-n형 Si)
CHI, EG, XI = 4.05, 1.12, 0.21          # 전자친화도, band gap, Ec-EF (n=1e16 근처)


def band_panel(ax, phim, title, contact=True):
    ax.set_title(title, loc="left", fontsize=10.5)
    ax.set_xlim(-3.2, 7.4)
    ax.set_ylim(-1.6, 5.8)
    ax.axis("off")
    VAC = 5.0
    if not contact:
        efm = VAC - phim
        rect(ax, -3.0, -1.4, 2.6, efm + 1.4, "al", lw=0.6, alpha=0.7)
        ax.plot([-3.0, -0.4], [VAC, VAC], color="#555555", lw=1.0, ls="--")
        ax.plot([-3.0, -0.4], [efm, efm], color=PAL[1], lw=1.6)
        text(ax, -1.7, efm - 0.32, "E_F (금속)", size=8.5, color=PAL[1])
        arrow(ax, -0.9, efm, -0.9, VAC, lw=0.9, ms=7, style="<|-|>")
        text(ax, -1.05, (efm + VAC) / 2, "φm", size=10, ha="right")
        ec = VAC - CHI
        ef = ec - XI
        ev = ec - EG
        ax.plot([1.0, 7.0], [VAC, VAC], color="#555555", lw=1.0, ls="--")
        text(ax, 4.0, VAC + 0.3, "진공 준위", size=8.5, color="#555555")
        ax.plot([1.0, 7.0], [ec, ec], color=C["ink"], lw=1.8)
        ax.plot([1.0, 7.0], [ev, ev], color=C["ink"], lw=1.8)
        ax.plot([1.0, 7.0], [ef, ef], color=PAL[1], lw=1.4, ls="--")
        text(ax, 7.1, ec, "Ec", size=9, ha="left")
        text(ax, 7.1, ev, "Ev", size=9, ha="left")
        text(ax, 7.1, ef - 0.12, "E_F", size=9, ha="left", color=PAL[1])
        arrow(ax, 1.5, ec, 1.5, VAC, lw=0.9, ms=7, style="<|-|>")
        text(ax, 1.65, (ec + VAC) / 2, "χ", size=11, ha="left", fontfamily="DejaVu Sans")
        arrow(ax, 5.6, ef, 5.6, VAC, lw=0.9, ms=7, style="<|-|>")
        text(ax, 5.75, (ef + VAC) / 2, "φs", size=10, ha="left")
        text(ax, 4.0, -1.3, "n형 Si", size=9.5)
        text(ax, -1.7, -1.3, "금속", size=9.5)
        return
    ef = 1.0
    bend = (phim - CHI) - XI                 # 계면 Ec - bulk Ec
    W = 2.6 if bend > 0 else 1.2
    x = np.linspace(0, 7.0, 300)
    ec = ef + XI + bend * np.clip(1 - x / W, 0, None) ** 2
    rect(ax, -3.0, -1.4, 3.0, ef + 1.4, "al", lw=0.6, alpha=0.7)
    ax.plot([-3.0, 0], [ef, ef], color=PAL[1], lw=1.6)
    ax.plot(x, ec, color=C["ink"], lw=1.8)
    ax.plot(x, ec - EG, color=C["ink"], lw=1.8)
    ax.plot([0, 7.0], [ef, ef], color=PAL[1], lw=1.4, ls="--")
    ax.plot([0, 0], [-1.4, 4.0], color="#555555", lw=0.8)
    text(ax, 7.1, ec[-1], "Ec", size=9, ha="left")
    text(ax, 7.1, ec[-1] - EG, "Ev", size=9, ha="left")
    text(ax, 7.1, ef - 0.12, "E_F", size=9, ha="left", color=PAL[1])
    text(ax, 3.6, -1.3, "n형 Si", size=9.5)
    text(ax, -1.5, -1.3, "금속", size=9.5)
    if bend > 0:
        arrow(ax, 0.35, ef, 0.35, ef + XI + bend, lw=1.0, ms=7, style="<|-|>", color=C["red"])
        text(ax, 0.2, ef + XI + bend + 0.45, "φB = φm − χ", size=10, ha="left", color=C["red"],
             fontfamily="DejaVu Sans")
        arrow(ax, 0.0, -0.75, W, -0.75, lw=0.9, ms=7, style="<|-|>", color="#555555")
        text(ax, W / 2, -0.45, "공핍층", size=8.5)
        circ(ax, 5.0, ec[-1] + 0.18, 0.13, "#1f77b4", lw=0.3)
        circ(ax, 5.6, ec[-1] + 0.18, 0.13, "#1f77b4", lw=0.3)
        arrow(ax, 4.6, ec[-1] + 1.6, 1.4, ec[-1] + 1.6, lw=1.0, ms=7, color=C["blue"])
        text(ax, 3.0, ec[-1] + 2.05, "전자가 장벽에 막힘", size=8.5, color=C["blue"])
    else:
        circ(ax, 0.5, ef + 0.08, 0.13, "#1f77b4", lw=0.3)
        circ(ax, 1.1, ef + 0.12, 0.13, "#1f77b4", lw=0.3)
        arrow(ax, 4.6, ec[-1] + 0.5, 0.6, ec[-1] + 0.5, lw=1.0, ms=7, color=C["blue"], style="<|-|>")
        text(ax, 2.9, ec[-1] + 0.95, "장벽 없이 양쪽으로 흐름", size=8.5, color=C["blue"])


f, axs = plt.subplots(1, 3, figsize=(14.5, 4.3))
band_panel(axs[0], 4.8, "접촉 전 (금속, n형 Si 따로)", contact=False)
band_panel(axs[1], 4.8, "φm > φs → Schottky (장벽 생김)")
band_panel(axs[2], 4.1, "φm < φs → ohmic (이상적인 경우)")
plt.tight_layout()
save(f, P, "band_schottky_ohmic")

# 4. doping 농도와 장벽 두께
EPS = 11.7 * 8.854e-14
Q = 1.602e-19


def wdep(N, phi=0.6):
    return np.sqrt(2 * EPS * phi / (Q * N)) * 1e7        # nm


f, axs = plt.subplots(1, 2, figsize=(11.5, 3.9))
for ax, N, xi, xmax, title in [(axs[0], 1e17, 0.13, 160, "낮은 doping (10¹⁷): 장벽이 두꺼움 → 넘어가야만 흐름"),
                               (axs[1], 1e20, -0.05, 8, "높은 doping (10²⁰): 장벽이 얇음 → 뚫고 지나감 (tunneling)")]:
    W = wdep(N)
    phib = 0.65
    x = np.linspace(0, xmax, 400)
    ec = xi + (phib - xi) * np.clip(1 - x / W, 0, None) ** 2
    ax.plot(x, ec, color=C["ink"], lw=2.0)
    ax.axhline(0, color=PAL[1], lw=1.3, ls="--")
    ax.axvspan(-xmax * 0.25, 0, color=C["al"], alpha=0.6)
    ax.set_xlim(-xmax * 0.25, xmax)
    ax.set_ylim(-0.25, 0.95)
    ax.set_xlabel("계면에서 거리 (nm)")
    ax.set_ylabel("energy (eV, E_F 기준)")
    ax.set_title(title, loc="left", fontsize=10.5)
    ax.text(-xmax * 0.125, 0.85, "금속", ha="center", fontsize=9.5)
    ax.text(xmax * 0.97, 0.03, "E_F", ha="right", va="bottom", color=PAL[1], fontsize=9.5)
    ax.annotate("", xy=(W, -0.17), xytext=(0, -0.17), arrowprops=dict(arrowstyle="<|-|>", color="#555555", lw=0.9))
    ax.text(W / 2, -0.12, f"공핍층 ≈ {W:.0f} nm" if W > 10 else f"공핍층 ≈ {W:.1f} nm",
            ha="center", va="bottom", fontsize=9.5)
    if N < 1e18:
        ax.annotate("", xy=(W * 0.15, 0.78), xytext=(W * 0.9, 0.2),
                    arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.4, connectionstyle="arc3,rad=-0.4"))
        ax.text(W * 0.85, 0.62, "열 energy로\n넘어가는 전자만", fontsize=9, color=C["blue"])
    else:
        ax.annotate("", xy=(-xmax * 0.05, 0.02), xytext=(W * 1.6, 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.6))
        ax.text(W * 1.1, 0.3, "얇은 장벽을\n그대로 통과", fontsize=9, color=C["blue"])
    ax.grid(alpha=0.2)
plt.tight_layout()
save(f, P, "tunneling_doping")

# 5. 비접촉저항 vs doping
KT = 0.02585
A_STAR = 110.0                      # n-Si 리처드슨 상수 (A/cm²K²)
N = np.logspace(15, 21, 400)
f, ax = plot_ax(7.6, 4.6)
for phib, c in [(0.4, PAL[0]), (0.6, PAL[1]), (0.8, PAL[2])]:
    e00 = 1.86e-11 * np.sqrt(N / (0.26 * 11.7))
    e0 = e00 / np.tanh(e00 / KT)
    rho = 8.617e-5 / (A_STAR * 300) * np.exp(phib / e0)
    ax.loglog(N, rho, color=c, lw=2.2, label=f"장벽 {phib} eV")
ax.axvspan(1e15, 3e17, color="#eeeeee", zorder=0)
ax.axvspan(3e19, 1e21, color="#e8f0fa", zorder=0)
ax.text(2e16, 3e-9, "넘어가는 영역\n(열전자 방출)", ha="center", fontsize=9)
ax.text(1.7e20, 3e-9, "뚫고 가는 영역\n(tunneling)", ha="center", fontsize=9)
ax.set_ylim(1e-9, 1e12)
ax.set_xlabel("계면 doping 농도 (cm⁻³)")
ax.set_ylabel("비접촉저항 ρc (Ω·cm²)")
ax.set_title("doping이 진할수록 접촉 저항이 급격히 감소 (개념 계산)", loc="left", fontsize=11)
ax.legend(fontsize=9, loc="upper right")
save(f, P, "rc_vs_doping")

# 6. contact 크기와 저항
w = np.linspace(10, 200, 300)
f, ax = plot_ax(7.2, 4.2)
for rc, c in [(1e-7, PAL[1]), (1e-8, PAL[0]), (1e-9, PAL[2])]:
    ax.loglog(w, rc / (w * 1e-7) ** 2, color=c, lw=2.2, label=f"ρc = {rc:.0e} Ω·cm²")
ax.axhline(100, color="#999999", lw=0.9, ls="--")
ax.text(11, 120, "100 Ω", fontsize=9, color="#555555")
ax.set_xlabel("정사각형 contact 한 변 (nm)")
ax.set_ylabel("contact 하나의 저항 (Ω)")
ax.set_title("R = ρc / 면적: contact이 작아지면 저항이 제곱으로 커짐", loc="left", fontsize=11)
ax.legend(fontsize=9)
save(f, P, "contact_scaling")

# 7. salicide 단계 (NMOS 하나만 확대)
base = dict(sti="final", wells=True, gates=True, ldd="np", spacer=True, sd="np")
steps = [("① source / drain까지 완성 (Si, poly가 드러남)", dict(base)),
         ("② 금속 (Co, Ni 등) 얇게 증착", dict(base, metal_blanket=True)),
         ("③ 1차 열처리: Si에 닿은 곳만 silicide", dict(base, sil=True, metal_left=True)),
         ("④ 반응 안 한 금속만 습식 제거 + 2차 열처리", dict(base, sil=True))]
f, axs = panels(4, 2, 5.6, 2.55, (0.2, 11.8), (-1.25, 2.55), titles=[s for s, _ in steps], size=10)
for ax, (_, st) in zip(axs, steps):
    cmos.draw(ax, st, lab=False)
text(axs[0], 2.8, -0.85, "n⁺ (Si)", size=8.5)
text(axs[0], 8.7, -0.85, "n⁺ (Si)", size=8.5)
text(axs[0], 6.0, 2.15, "poly", size=8.5)
text(axs[1], 8.6, 1.0, "금속이 전부 덮음", size=8.5, color="#444444")
text(axs[2], 2.8, -0.75, "silicide", size=8.5, color=C["purple"], weight="bold")
text(axs[2], 6.0, 2.2, "silicide", size=8.5, color=C["purple"], weight="bold")
text(axs[2], 9.4, 1.15, "spacer, STI 위는\n반응 안 함", size=8.2, color="#444444")
text(axs[3], 9.4, 1.15, "자기 정렬:\nmask 없이 Si 위에만", size=8.2, color=C["purple"])
save(f, P, "salicide_steps")

# 8. silicide 형성 온도 (대략)
rows = [("TiSi₂", [(600, 750, "C49 상 (고저항)", "#f6d7a7"), (750, 900, "C54 상 (저저항)", "#9b88cf")]),
        ("CoSi₂", [(450, 600, "CoSi (고저항)", "#f6d7a7"), (600, 850, "CoSi₂ (저저항)", "#9b88cf")]),
        ("NiSi", [(250, 350, "Ni₂Si", "#f6d7a7"), (350, 650, "NiSi (저저항)", "#9b88cf"),
                  (700, 900, "NiSi₂ / 뭉침", "#e57373")])]
f, ax = plot_ax(8.6, 3.2)
ax.grid(False)
for i, (name, segs) in enumerate(rows):
    y = len(rows) - 1 - i
    for (a, b, s, c) in segs:
        ax.barh(y, b - a, left=a, height=0.55, color=c, edgecolor="#333333", lw=0.7)
        ax.text((a + b) / 2, y, s, ha="center", va="center", fontsize=8.6)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=11)
ax.set_xlim(200, 950)
ax.set_xlabel("열처리 온도 (°C)")
ax.set_title("silicide별로 생기는 상과 온도 (대략적인 범위)", loc="left", fontsize=11)
save(f, P, "silicide_window")
