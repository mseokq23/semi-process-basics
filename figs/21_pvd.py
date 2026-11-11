import numpy as np
from common import *

P = 21

# 1. 증발 장치
f, ax = canvas(7.2, 6.0, (0, 12), (0, 10))
ax.add_patch(FancyBboxPatch((0.6, 0.6), 10.8, 8.8, boxstyle="round,pad=0,rounding_size=1.0", fc="#fafafa",
                            ec="#555555", lw=1.2))
ax.add_patch(Arc((6.0, 4.0), 9.0, 9.0, theta1=35, theta2=145, color="#455a64", lw=3))
for a in np.deg2rad([50, 70, 90, 110, 130]):
    x, y = 6.0 + 4.5 * np.cos(a), 4.0 + 4.5 * np.sin(a)
    rect(ax, x - 0.45, y - 0.08, 0.9, 0.16, "si", lw=0.4, z=4)
    line(ax, [6.0, x], [2.2, y - 0.2], color="#ffb74d", lw=1.0, ls="--")
rect(ax, 5.2, 1.2, 1.6, 1.0, "#9e9e9e", lw=0.6)
ax.add_patch(Ellipse((6.0, 2.2), 1.4, 0.4, fc="#ffcc80", ec="#e65100", lw=0.8, zorder=5))
ax.add_patch(Arc((4.6, 2.0), 2.6, 2.6, theta1=-10, theta2=170, color=C["blue"], lw=1.6, zorder=6))
rect(ax, 2.6, 1.2, 0.9, 0.6, "#bbdefb", lw=0.5)
text(ax, 3.05, 0.95, "전자총", size=8.8)
text(ax, 6.0, 0.95, "원료 (도가니)", size=8.8)
text(ax, 6.0, 9.0, "웨이퍼를 돔에 붙여 놓음", size=9.5)
arrow(ax, 11.4, 2.0, 12.0, 2.0, lw=1.2)
text(ax, 6.0, 5.2, "고진공 → 원자가 곧게 날아감", size=9.5, box="white")
save(f, P, "evaporation")

# 2. 스퍼터 원리
f, ax = canvas(9, 5.6, (0, 16), (0, 10))
rect(ax, 1.0, 8.2, 14.0, 0.9, "#b0bec5", lw=0.8)
text(ax, 8.0, 8.65, "타겟 (음극, 증착할 재료)", size=10)
rect(ax, 2.0, 0.6, 12.0, 0.6, "#9e9e9e", lw=0.6)
rect(ax, 3.0, 1.2, 10.0, 0.25, "si", lw=0.5)
text(ax, 8.0, 0.9, "웨이퍼 (양극 쪽)", size=9, color="white")
ax.add_patch(Ellipse((8.0, 5.0), 13, 4.6, fc="#f3e5f5", ec="none", alpha=0.9, zorder=0))
for x in (4.0, 7.0, 10.0, 12.5):
    circ(ax, x, 5.6, 0.3, "#ef9a9a", lw=0.5)
    text(ax, x, 5.6, "+", size=9, weight="bold")
    arrow(ax, x, 6.0, x + 0.3, 8.1, color="red", lw=1.3)
for x0, ang in [(4.3, -110), (7.3, -70), (10.3, -95), (12.8, -60), (5.5, -130)]:
    a = np.deg2rad(ang)
    circ(ax, x0 + 0.2, 8.0, 0.18, "#78909c", lw=0.4, z=6)
    arrow(ax, x0 + 0.2, 7.9, x0 + 0.2 + 5.5 * np.cos(a), 7.9 + 5.5 * np.sin(a), color="#607d8b", lw=1.0, ms=7, ls="--")
text(ax, 13.9, 5.6, "Ar⁺", size=10, color=C["red"])
text(ax, 2.8, 3.4, "튀어나온 원자\n(여러 방향)", size=9.5, color="#455a64", box="white")
save(f, P, "sputter")

# 3. 스퍼터 수율
data = [("Si", 0.5), ("Ti", 0.51), ("Ta", 0.57), ("W", 0.57), ("Mo", 0.80), ("Al", 1.05), ("Pt", 1.40),
        ("Cu", 2.35), ("Au", 2.40), ("Ag", 3.12)]
f, ax = plot_ax(7.6, 3.8)
ax.bar([d[0] for d in data], [d[1] for d in data], color=[PAL[1] if d[0] in ("Cu", "Al", "W", "Ti", "Ta") else
                                                          "#9e9e9e" for d in data])
ax.set_ylabel("스퍼터 수율 (원자 / 이온)")
ax.set_title("Ar⁺ 500 eV 한 개가 떼어내는 원자 수 (문헌 대략값, 빨강 = 배선에 쓰는 금속)", loc="left", fontsize=10.5)
save(f, P, "sputter_yield")

# 4. 마그네트론
f, ax = canvas(9, 5.4, (0, 16), (0, 9.6))
for x, s in [(2.5, "S"), (8.0, "N"), (13.5, "S")]:
    rect(ax, x - 1.0, 7.8, 2.0, 1.4, "#90a4ae" if s == "S" else "#ef9a9a", lw=0.6)
    text(ax, x, 8.5, s, size=11, weight="bold")
rect(ax, 0.8, 6.8, 14.4, 1.0, "#b0bec5", lw=0.8)
for xc in (5.25, 10.75):
    for r in (1.6, 2.4):
        ax.add_patch(Arc((xc, 6.8), 2 * r + 0.0, 2 * r * 0.9, theta1=180, theta2=360, color="#5c6bc0", lw=1.0,
                         ls="--", zorder=5))
    ax.add_patch(Ellipse((xc, 5.5), 3.4, 1.0, fc="#ce93d8", ec="none", alpha=0.85, zorder=4))
    poly(ax, [(xc - 1.6, 6.8), (xc - 0.6, 7.35), (xc + 0.6, 7.35), (xc + 1.6, 6.8)], "white", lw=0.6, z=6)
text(ax, 8.0, 4.0, "자석이 전자를 타겟 앞에 가둠 → 플라즈마가 진해지고 증착이 빨라짐", size=9.5)
text(ax, 8.0, 3.2, "자기장이 센 곳만 많이 깎여서 타겟에 홈(레이스트랙)이 생김", size=9.5)
rect(ax, 3.0, 0.6, 10.0, 0.3, "si", lw=0.5)
text(ax, 8.0, 1.3, "웨이퍼", size=9)
save(f, P, "magnetron")

# 5. 반응성 스퍼터 히스테리시스 (개념)
q = np.linspace(0, 10, 300)
up = np.where(q < 6.0, 1.0 - 0.03 * q, 0.25 - 0.005 * (q - 6))
down = np.where(q > 3.5, 0.25 - 0.005 * (q - 6), 1.0 - 0.03 * q)
f, ax = plot_ax(7.0, 4.0)
ax.plot(q, up, color=PAL[0], lw=2.2, label="N₂ 늘릴 때")
ax.plot(q, down, "--", color=PAL[1], lw=2.2, label="N₂ 줄일 때")
ax.text(1.0, 0.75, "금속 모드\n(타겟 표면이 금속, 빠름)", fontsize=9.5)
ax.text(6.6, 0.4, "포이즌 모드\n(타겟 표면이 질화막, 느림)", fontsize=9.5)
ax.set_xlabel("반응 가스(N₂) 유량 (상대값)")
ax.set_ylabel("증착 속도 (상대값)")
ax.set_title("반응성 스퍼터 (Ti + N₂ → TiN) 개념 그래프", loc="left")
ax.legend(fontsize=9)
save(f, P, "reactive")

# 6. PVD 피복성, 리프트오프
tt = ["증발: 직진성 강함 → 측벽 거의 안 덮임", "스퍼터: 여러 방향 → 오버행", "이온화 PVD: 바닥까지 끌어당김",
      "리프트오프: 증발의 직진성을 이용"]
f, axs = panels(4, 4, 3.3, 3.2, (0, 10), (0, 6.6), titles=tt, size=9.6)
for k, ax in enumerate(axs[:3]):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "ox", lw=0.6)
    rect(ax, 0.3, 1.1, 3.7, 3.6, "ox", lw=0.6)
    rect(ax, 6.0, 1.1, 3.7, 3.6, "ox", lw=0.6)
rect(axs[0], 0.3, 4.7, 3.7, 0.5, "al", lw=0.5)
rect(axs[0], 6.0, 4.7, 3.7, 0.5, "al", lw=0.5)
rect(axs[0], 4.0, 1.1, 2.0, 0.5, "al", lw=0.5)
for x in (2.0, 5.0, 8.0):
    arrow(axs[0], x, 6.4, x, 5.4 if x != 5.0 else 1.8, color="#607d8b", lw=1.0, ms=7)
poly(axs[1], [(0.3, 4.7), (4.0, 4.7), (4.0, 1.1), (6.0, 1.1), (6.0, 4.7), (9.7, 4.7), (9.7, 5.3), (6.15, 5.3),
              (5.65, 4.95), (5.92, 4.5), (5.95, 1.25), (4.05, 1.25), (4.08, 4.5), (4.35, 4.95), (3.85, 5.3),
              (0.3, 5.3)], "al", lw=0.5, z=6)
poly(axs[2], [(0.3, 4.7), (4.0, 4.7), (4.0, 1.1), (6.0, 1.1), (6.0, 4.7), (9.7, 4.7), (9.7, 5.2), (5.85, 5.2),
              (5.85, 1.5), (4.15, 1.5), (4.15, 5.2), (0.3, 5.2)], "al", lw=0.5, z=6)
for x in (4.6, 5.0, 5.4):
    arrow(axs[2], x, 6.4, x, 1.7, color="red", lw=1.0, ms=7)
ax = axs[3]
rect(ax, 0.3, 0.3, 9.4, 1.0, "ox", lw=0.6)
poly(ax, [(0.3, 1.3), (3.6, 1.3), (3.9, 3.4), (0.3, 3.4)], "pr", lw=0.6)
poly(ax, [(9.7, 1.3), (6.4, 1.3), (6.1, 3.4), (9.7, 3.4)], "pr", lw=0.6)
rect(ax, 0.3, 3.4, 3.6, 0.4, "al", lw=0.5)
rect(ax, 6.1, 3.4, 3.6, 0.4, "al", lw=0.5)
rect(ax, 3.9, 1.3, 2.2, 0.4, "al", lw=0.5)
text(ax, 5.0, 5.2, "PR을 녹이면 위 금속도 같이 떨어짐\n→ 구멍 자리에만 금속이 남음", size=8.8)
save(f, P, "pvd_coverage")
