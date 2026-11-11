import numpy as np
from common import *

P = 22
KB = 8.617e-5

# 1. CVD 단계
f, ax = canvas(11, 4.8, (0, 22), (0, 9.6))
rect(ax, 0.5, 0.5, 21, 1.6, "si", lw=0.6)
text(ax, 11, 1.3, "웨이퍼 (가열)", size=10)
ax.fill_between([0.5, 21.5], [2.1, 2.1], [3.6, 5.2], color="#e3f2fd", alpha=0.8, zorder=0)
text(ax, 19.5, 4.1, "경계층", size=9.5, color=C["blue"])
for y in (7.0, 8.0):
    arrow(ax, 0.8, y, 6.0, y, color="#90a4ae", lw=1.4)
text(ax, 3.4, 8.6, "① 기체 흐름 (전구체 운반)", size=9.5)
steps = [(5.5, "② 경계층을\n지나 확산"), (9.2, "③ 표면에\n흡착"), (12.6, "④ 표면 반응,\n표면 이동"),
         (16.2, "⑤ 부산물\n탈착"), (19.8, "⑥ 배기")]
arrow(ax, 6.5, 6.5, 8.0, 2.8, color="blue", lw=1.3)
circ(ax, 9.2, 2.35, 0.25, "#ffb74d", lw=0.4)
for x in np.arange(11.6, 13.8, 0.45):
    circ(ax, x, 2.3, 0.2, "nit", lw=0.3)
arrow(ax, 16.2, 2.6, 16.8, 6.4, color="green", lw=1.3)
circ(ax, 16.2, 2.45, 0.2, "#c5e1a5", lw=0.3)
arrow(ax, 17.5, 7.5, 21.3, 7.5, color="#90a4ae", lw=1.4)
for x, s in steps:
    text(ax, x, 5.9 if x != 5.5 else 4.8, s, size=9.2, box="white")
save(f, P, "cvd_steps")

# 2. 온도에 따른 성장 속도 (Grove 모델)
T = np.linspace(500, 1200, 300) + 273.15
ks = 1e7 * np.exp(-1.6 / (KB * T))
f, ax = plot_ax(7.2, 4.4)
for hg, lab, c, ls in [(200.0, "저압: 확산이 빨라서 h_g 큼", PAL[1], "-"), (2.0, "대기압: h_g 작음", PAL[0], "--")]:
    G = ks * hg / (ks + hg)
    ax.semilogy(1000 / T, G, color=c, lw=2.2, label=lab, ls=ls)
ax.set_xlabel("1000 / T (1/K)")
ax.set_ylabel("성장 속도 (상대값)")
ax.text(1.02, 2e-3, "반응 속도 제한 (두 곡선 겹침):\n온도에 아주 민감\n→ 온도만 고르면 균일", fontsize=9.5)
ax.text(0.69, 0.25, "대기압은 여기서 꺾임:\n물질 전달 제한\n(기체 흐름에 민감)", fontsize=9.5, color=PAL[0])
ax.legend(fontsize=9, loc="lower left")
ax.set_title("G = k_s·h_g / (k_s + h_g) 로 그린 개념 그래프", loc="left", fontsize=11)
sec = ax.secondary_xaxis("top", functions=(lambda v: 1000 / v - 273.15, lambda v: 1000 / (v + 273.15)))
sec.set_xlabel("°C")
save(f, P, "growth_rate")

# 3. APCVD / LPCVD 장비
f, axs = panels(2, 2, 6.0, 4.0, (0, 12), (0, 8), titles=["APCVD: 대기압, 컨베이어로 연속 처리",
                                                       "LPCVD: 저압 퍼니스, 세워서 100장 이상"], size=11)
ax = axs[0]
rect(ax, 0.5, 1.0, 11.0, 0.5, "#9e9e9e", lw=0.6)
for x in (1.5, 4.5, 7.5, 10.0):
    rect(ax, x - 0.9, 1.5, 1.8, 0.25, "si", lw=0.4)
for x in (3.0, 6.0, 9.0):
    rect(ax, x - 1.0, 4.0, 2.0, 1.2, "#e3f2fd", lw=0.6)
    for dx in (-0.5, 0, 0.5):
        arrow(ax, x + dx, 4.0, x + dx, 2.2, color="blue", lw=1.0, ms=7)
arrow(ax, 1.0, 0.5, 11.0, 0.5, lw=1.2)
text(ax, 6.0, 0.05, "웨이퍼가 이동", size=9, va="bottom")
text(ax, 6.0, 6.2, "가스 분사 노즐", size=9.5)
text(ax, 6.0, 7.2, "빠르지만 피복성, 파티클이 약점", size=9.5, color="#555555")
ax = axs[1]
rect(ax, 1.0, 1.0, 10.0, 5.0, "#eef7fc", ec="#6a9fc0", lw=1.4)
for x in np.arange(1.8, 10.4, 0.35):
    line(ax, [x, x], [2.0, 5.0], color="#7f8c99", lw=1.6)
for y in (0.6, 6.4):
    for x in np.arange(1.2, 10.9, 0.5):
        line(ax, [x, x + 0.25], [y, y], color=C["red"], lw=2.0)
arrow(ax, 0.0, 3.5, 1.0, 3.5, color="blue", lw=1.4)
arrow(ax, 11.0, 3.5, 12.0, 3.5, color="#555555", lw=1.4)
text(ax, 0.5, 4.2, "가스", size=9, color=C["blue"])
text(ax, 11.6, 4.2, "펌프", size=9)
text(ax, 6.0, 7.2, "균일도, 피복성 좋음. 온도가 높음", size=9.5, color="#555555")
save(f, P, "apcvd_lpcvd")

# 4. 공정별 온도 (열 예산)
rows = [("열산화", 800, 1200), ("LPCVD Si₃N₄", 700, 800), ("LPCVD TEOS 산화막", 650, 720), ("LPCVD poly-Si", 580, 650),
        ("PECVD SiO₂, SiN", 200, 400), ("ALD (High-k 등)", 200, 350), ("Cu 배선 공정", 100, 400)]
f, ax = plot_ax(8.2, 4.2)
for k, (s, lo, hi) in enumerate(rows):
    y = len(rows) - k
    ax.plot([lo, hi], [y, y], lw=10, color=PAL[k % 6], solid_capstyle="butt")
    ax.text(hi + 15, y, s, va="center", fontsize=9.5)
ax.axvline(450, color=C["red"], lw=1.2, ls="--")
ax.text(455, 0.35, "배선이 생긴 뒤 상한 (대략 400~450 °C)", fontsize=9.5, color=C["red"])
ax.axvline(660, color="#999999", lw=1.0, ls=":")
ax.text(665, 7.6, "Al 녹는점 660 °C", fontsize=9, color="#666666")
ax.set_yticks([])
ax.set_xlim(0, 1500)
ax.set_ylim(0, 8.2)
ax.set_xlabel("공정 온도 (°C, 대략)")
ax.set_title("공정 순서가 뒤로 갈수록 낮은 온도만 쓸 수 있음", loc="left")
save(f, P, "thermal_budget")
