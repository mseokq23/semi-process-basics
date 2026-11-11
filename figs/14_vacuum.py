import numpy as np
from common import *

P = 14
KB = 1.380649e-23

# 1. 평균자유행로
d = 3.7e-10                      # N2 분자 지름 (m)
T = 300.0
Pt = np.logspace(-8, 3, 300)     # Torr
lam = KB * T / (np.sqrt(2) * np.pi * d ** 2 * Pt * 133.322)
print("MFP (N2, 300K): " + ", ".join(f"{p:g} Torr -> {KB * T / (np.sqrt(2) * np.pi * d ** 2 * p * 133.322):.3g} m"
                                    for p in (760, 1, 0.1, 0.01, 1e-3, 1e-6)))
f, ax = plot_ax(7.6, 4.6)
ax.loglog(Pt, lam, color="#222222", lw=2.4)
marks = [("대기압 (APCVD)", 760), ("LPCVD", 0.3), ("식각 (RIE)", 0.05), ("sputter", 0.005), ("ion 주입 beamline", 1e-6)]
for (s, p), c in zip(marks, PAL):
    l = KB * T / (np.sqrt(2) * np.pi * d ** 2 * p * 133.322)
    ax.plot(p, l, "o", color=c, ms=8)
    ax.text(p * 1.6, l * 1.5, s, color=c, fontsize=9.5)
for v, s in [(0.3, "chamber 크기 (~30 cm)"), (1e-6, "1 µm")]:
    ax.axhline(v, color="#999999", lw=0.8, ls=":")
    ax.text(2e-8, v * 1.25, s, fontsize=9, color="#666666")
ax.set_xlabel("압력 (Torr)")
ax.set_ylabel("평균자유행로 λ (m)")
ax.set_title("N₂, 300 K: 압력이 낮을수록 분자가 안 부딪히고 멀리 감", loc="left")
save(f, P, "mfp")

# 2. 압력대별 공정
f, ax = plt.subplots(figsize=(11, 4.4))
ax.set_xscale("log")
ax.set_xlim(1e-9, 3e3)
bands = [(760, 1, "저진공", "#eef5fb"), (1, 1e-3, "중진공", "#dceaf7"), (1e-3, 1e-7, "고진공", "#c6dbef"),
         (1e-7, 1e-9, "초고진공", "#9ecae1")]
for hi, lo, s, c in bands:
    ax.axvspan(lo, hi, color=c, zorder=0)
    ax.text(np.sqrt(hi * lo), 7.55, s, ha="center", fontsize=10, fontweight="bold")
procs = [("APCVD", 700, 800), ("LPCVD", 0.1, 1), ("PECVD", 0.5, 10), ("ALD", 0.1, 5), ("RIE (CCP) 식각", 0.01, 0.5),
         ("ICP 식각", 1e-3, 0.05), ("sputter (PVD)", 1e-3, 1e-2), ("증발 (PVD)", 1e-7, 1e-5),
         ("ion 주입 beamline", 1e-7, 1e-5)]
for k, (s, lo, hi) in enumerate(procs):
    y = 6.6 - k * 0.72
    ax.plot([lo, hi], [y, y], color=PAL[k % 6], lw=9, solid_capstyle="butt")
    ax.text(hi * 1.8, y, s, va="center", fontsize=9.5)
ax.set_ylim(0, 8)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel("압력 (Torr), 1 Torr ≈ 133 Pa, 대기압 760 Torr")
ax.set_title("공정마다 쓰는 압력대 (대략적인 범위)", loc="left")
save(f, P, "pressure_map")

# 3. 진공 시스템 구성
f, ax = canvas(12, 5.8, (0, 24.4), (-1.0, 10.6))
box(ax, 0.4, 4.0, 3.2, 3.0, "load lock", fc="#eef1f4", size=10)
rect(ax, 3.6, 5.0, 0.3, 1.0, "#555555", lw=0.3)
text(ax, 3.75, 2.4, "slit valve", size=8.5)
arrow(ax, 3.75, 2.65, 3.75, 4.9, lw=0.7, ms=6)
box(ax, 3.9, 2.8, 7.0, 5.4, "", fc="#e3f2fd", size=10)
text(ax, 7.4, 7.5, "공정 chamber", size=11, weight="bold")
rect(ax, 5.2, 3.4, 4.4, 0.5, "#9e9e9e", lw=0.5)
rect(ax, 5.6, 3.9, 3.6, 0.15, "si", lw=0.5)
text(ax, 7.4, 4.6, "wafer", size=9)
box(ax, 6.2, 9.0, 2.4, 1.2, "MFC", fc="#fff3e0", size=9.5)
arrow(ax, 7.4, 9.0, 7.4, 8.25, lw=1.2)
text(ax, 9.0, 9.6, "공정 gas (유량 제어)", size=9, ha="left")
line(ax, [10.9, 11.6], [7.3, 7.3], lw=1.0)
circ(ax, 12.05, 7.3, 0.45, "#ffffff", lw=0.8)
text(ax, 12.05, 7.3, "CM", size=8.5)
text(ax, 12.7, 7.3, "압력계 (capacitance manometer)", size=8.5, ha="left")
rect(ax, 10.9, 3.6, 1.6, 1.2, "#cfd8dc", lw=0.6)
text(ax, 11.7, 4.2, "throttle\nvalve", size=8.3)
rect(ax, 12.5, 3.6, 1.2, 1.2, "#b0bec5", lw=0.6)
text(ax, 13.1, 4.2, "gate\nvalve", size=8.0)
box(ax, 13.7, 2.9, 3.0, 2.6, "turbomolecular\npump (TMP)", fc="#e8f5e9", size=9.5)
line(ax, [16.7, 18.6], [4.2, 4.2], lw=2.0)
text(ax, 17.65, 4.6, "foreline", size=8.5)
box(ax, 18.6, 2.9, 2.8, 2.6, "건식 pump", fc="#fff8e1", size=9.5)
arrow(ax, 21.4, 4.2, 22.6, 4.2, lw=1.4)
box(ax, 21.6, -0.8, 2.6, 1.6, "scrubber", fc="#fce4ec", size=9.5)
arrow(ax, 22.9, 4.2, 22.9, 0.8, lw=1.4)
text(ax, 15.2, 2.45, "고진공 담당", size=9, color=C["green"])
text(ax, 20.0, 2.45, "대기압 ~ 저진공 담당", size=9, color=C["orange"])
text(ax, 19.6, 0.0, "독성·가연성 gas는 배출 전에 처리 →", size=8.8, ha="center")
save(f, P, "vacuum_system")

# 4. pump, gauge 동작 범위
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 3.6), sharex=True)
for ax, rows, title in [
    (ax1, [("건식 pump", 1e-3, 760), ("turbomolecular pump", 1e-9, 1e-2), ("cryo pump", 1e-10, 1e-3)], "pump"),
    (ax2, [("Pirani gauge", 1e-3, 100), ("capacitance manometer", 1e-4, 1000), ("ion gauge", 1e-10, 1e-3)], "압력계")]:
    for k, (s, lo, hi) in enumerate(rows):
        ax.plot([lo, hi], [k, k], lw=12, color=PAL[k], solid_capstyle="butt")
        ax.text(np.sqrt(lo * hi), k + 0.38, s, ha="center", fontsize=10)
    ax.set_xscale("log")
    ax.set_xlim(1e-11, 3e3)
    ax.set_ylim(-0.6, 2.9)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("압력 (Torr)")
    ax.set_title(title + " 동작 범위 (대략)", loc="left")
    ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
save(f, P, "pump_gauge_range")

# 5. turbomolecular pump 원리
f, ax = canvas(8, 5.0, (0, 16), (0, 10))
rect(ax, 2.0, 0.6, 12.0, 8.4, "#fafafa", lw=1.0)
for k, y in enumerate(np.arange(7.6, 1.2, -1.3)):
    rot = k % 2 == 0
    for x in np.arange(2.6, 13.6, 1.0):
        if rot:
            line(ax, [x, x + 0.6], [y, y - 0.5], color=C["blue"], lw=2.4)
        else:
            line(ax, [x + 0.6, x], [y, y - 0.5], color="#888888", lw=2.4)
    text(ax, 14.3, y - 0.25, "회전 날개" if rot else "고정 날개", size=8.5, ha="left",
         color=C["blue"] if rot else "#666666")
arrow(ax, 4.0, 8.4, 11.0, 8.4, color="blue", lw=1.3)
text(ax, 7.5, 8.75, "수만 rpm으로 회전", size=9, color=C["blue"])
for x, y in [(5.2, 9.5), (8.8, 9.6), (11.5, 9.4)]:
    circ(ax, x, y, 0.18, "#e57373", lw=0.4)
arrow(ax, 1.2, 8.5, 1.2, 1.4, color="red", lw=1.6)
text(ax, 0.9, 5.0, "기체 분자가\n아래로 밀려남", size=9, ha="right", color=C["red"])
text(ax, 8.0, 0.1, "아래쪽(foreline)은 건식 pump가 받아줘야 함", size=9.5, va="bottom")
save(f, P, "turbo")
