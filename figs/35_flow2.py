import numpy as np
from common import *
import cmos

P = 35

# 1. 단계별 단면 (B: 16단계 → 4장)
for g in range(4):
    st = cmos.B[g * 4:(g + 1) * 4]
    ytop = 4.3 if g < 2 else 7.0
    f, axs = panels(4, 2, 6.3, 2.55 if g < 2 else 3.2, (-0.3, 24.3), (-5.0, ytop), titles=[s for s, _ in st],
                    size=10.5)
    for ax, (_, d) in zip(axs, st):
        cmos.draw(ax, d, lab=True, size=8.5)
    if g == 0:
        legend(axs[3], ["nl", "pl", "pr", "nit"], loc="upper right", ncol=4, size=8.5, bbox=(1.0, 1.0),
               names=dict(nit="Si₃N₄"))
    if g == 1:
        legend(axs[2], ["np", "pp"], loc="upper right", ncol=2, size=8.5, bbox=(1.0, 1.0))
        legend(axs[3], ["sil"], loc="upper right", ncol=1, size=8.5, bbox=(1.0, 1.0))
    if g == 3:
        legend(axs[1], ["tin", "w", "ox"], loc="upper right", ncol=3, size=8.5, bbox=(1.0, 1.0),
               names=dict(ox="SiO₂ (PMD)"))
        legend(axs[3], ["cu", "lowk", "nit"], loc="upper right", ncol=3, size=8.5, bbox=(1.0, 1.0),
               names=dict(nit="SiN (보호막)"))
    save(f, P, f"b{g + 1}")

# 2. 완성 단면 + 층별 편 번호
f, ax = canvas(13.6, 7.0, (-9.0, 33.5), (-5.6, 8.4))
cmos.draw(ax, dict(cmos.FINAL), size=8.5)
L = [((0.5, -0.9), (-8.7, -1.0), "STI\n7, 17, 23, 32편"),
     ((2.5, -3.0), (-8.7, -3.6), "P-well / N-well\n26 ~ 28편"),
     ((2.0, -0.45), (-8.7, 1.2), "n⁺ 소스 / 드레인\n26 ~ 28편"),
     ((5.05, -0.18), (-8.7, 3.3), "LDD\n26편"),
     ((5.7, 0.05), (-8.7, 5.4), "게이트 산화막\n6 ~ 7편"),
     ((12.0, 6.3), (-8.7, 7.4), "보호막 (SiN)\n20편"),
     ((17.0, 0.9), (25.6, 1.0), "poly 게이트\n22, 18편"),
     ((18.85, 0.5), (25.6, -1.2), "스페이서\n20, 18편"),
     ((19.6, -0.06), (25.6, 3.0), "실리사이드\n29편"),
     ((20.5, -0.45), (25.6, -3.3), "p⁺ 소스 / 드레인\n26 ~ 28편"),
     ((15.0, 1.6), (25.6, 5.0), "W 플러그 + PMD\n23, 30, 32편"),
     ((13.5, 4.6), (25.6, 7.2), "Cu 배선, 비아 + Low-k\n31, 32편")]
for (px, py), (tx, ty), s in L:
    text(ax, tx, ty, s, size=8.8, ha="left", box="#fff8e1")
    x_end = tx + 6.6 if tx < 0 else tx - 0.2
    arrow(ax, x_end, ty, px, py, lw=0.8, ms=7, color="#555555")
text(ax, 6.0, -4.75, "NMOS", size=11, weight="bold")
text(ax, 18.0, -4.75, "PMOS", size=11, weight="bold")
save(f, P, "final_labeled")

# 3. 인버터 회로와 전달 특성
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.2), gridspec_kw=dict(width_ratios=[0.9, 1.1]))
canvas(0, 0, (0, 10), (0, 10), ax=ax1)
ax1.set_title("회로: 단면의 각 부분이 어디에 해당하는지", loc="left", fontsize=10.5)
line(ax1, [5, 5], [9.3, 7.6], lw=1.6)
text(ax1, 5, 9.65, "VDD (PMOS 소스, 오른쪽 M1)", size=9)
# PMOS
line(ax1, [5, 5], [7.6, 7.0], lw=1.6)
line(ax1, [5, 5.0], [7.0, 7.0], lw=1.6)
for (x0, x1, y0, y1) in [(5.0, 5.0, 7.0, 5.6)]:
    pass
line(ax1, [4.6, 4.6], [7.4, 5.2], lw=2.2)
line(ax1, [4.6, 5.0, 5.0], [7.0, 7.0, 7.6], lw=1.6)
line(ax1, [4.6, 5.0, 5.0], [5.6, 5.6, 5.0], lw=1.6)
line(ax1, [4.25, 4.25], [7.2, 5.4], lw=1.6)
circ(ax1, 4.1, 6.3, 0.15, "white", lw=1.2)
text(ax1, 6.3, 6.3, "PMOS (N-well)", size=9.5, ha="left")
# NMOS
line(ax1, [5, 5], [5.0, 4.0], lw=1.6)
line(ax1, [4.6, 4.6], [4.4, 2.2], lw=2.2)
line(ax1, [4.6, 5.0, 5.0], [4.0, 4.0, 5.0], lw=1.6)
line(ax1, [4.6, 5.0, 5.0], [2.6, 2.6, 1.6], lw=1.6)
line(ax1, [4.25, 4.25], [4.2, 2.4], lw=1.6)
text(ax1, 6.3, 3.3, "NMOS (P-well)", size=9.5, ha="left")
line(ax1, [5, 5], [1.6, 0.9], lw=1.6)
line(ax1, [4.3, 5.7], [0.9, 0.9], lw=1.6)
line(ax1, [4.6, 5.4], [0.6, 0.6], lw=1.6)
text(ax1, 5, 0.2, "GND (NMOS 소스, 왼쪽 M1)", size=9)
# 입력, 출력
line(ax1, [3.95, 3.0, 3.0, 4.25], [6.3, 6.3, 3.3, 3.3], lw=1.6)
line(ax1, [2.0, 3.0], [4.8, 4.8], lw=1.6)
circ(ax1, 3.0, 4.8, 0.08, "#222222", lw=0.5)
text(ax1, 1.6, 4.8, "IN", size=10.5, weight="bold", ha="right")
text(ax1, 1.6, 4.1, "(poly 게이트)", size=8.6, ha="right")
line(ax1, [5.0, 7.6], [5.0, 5.0], lw=1.6)
circ(ax1, 5.0, 5.0, 0.08, "#222222", lw=0.5)
text(ax1, 7.8, 5.0, "OUT", size=10.5, weight="bold", ha="left")
text(ax1, 7.8, 4.3, "(두 드레인 + 가운데 M1)", size=8.6, ha="left")
# 전달 특성
VDD, VTN, VTP, KN, KP, LAM = 3.3, 0.7, -0.7, 1.0, 1.0, 0.05


def i_n(vgs, vds):
    if vgs <= VTN:
        return 0.0
    vov = vgs - VTN
    if vds < vov:
        return KN * (vov * vds - vds ** 2 / 2) * (1 + LAM * vds)
    return KN / 2 * vov ** 2 * (1 + LAM * vds)


def i_p(vsg, vsd):
    if vsg <= -VTP:
        return 0.0
    vov = vsg + VTP
    if vsd < vov:
        return KP * (vov * vsd - vsd ** 2 / 2) * (1 + LAM * vsd)
    return KP / 2 * vov ** 2 * (1 + LAM * vsd)


vin = np.linspace(0, VDD, 331)
vout = []
for vi in vin:
    lo, hi = 0.0, VDD
    for _ in range(60):
        mid = (lo + hi) / 2
        if i_p(VDD - vi, VDD - mid) - i_n(vi, mid) > 0:
            lo = mid
        else:
            hi = mid
    vout.append((lo + hi) / 2)
ax2.plot(vin, vout, color=PAL[0], lw=2.4)
ax2.plot([0, VDD], [0, VDD], ":", color="#999999", lw=1.0)
ax2.set_xlabel("입력 전압 (V)")
ax2.set_ylabel("출력 전압 (V)")
ax2.set_title("전달 특성: 입력 0 → 출력 VDD, 입력 VDD → 출력 0 (단순 모델)", loc="left", fontsize=10.5)
ax2.text(0.15, 2.85, "NMOS 꺼짐\nPMOS 켜짐", fontsize=9)
ax2.text(2.35, 0.35, "NMOS 켜짐\nPMOS 꺼짐", fontsize=9)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "inverter_circuit")
