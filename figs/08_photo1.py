import numpy as np
from common import *

P = 8


def base(ax, pr=None, exposed=None, z=2):
    """Si + 패터닝할 막(SiO₂) + PR"""
    rect(ax, 0.3, 0.4, 9.4, 1.8, "si", lw=0.7)
    rect(ax, 0.3, 2.2, 9.4, 0.6, "ox", lw=0.7)
    if pr == "full":
        rect(ax, 0.3, 2.8, 9.4, 1.0, "pr", lw=0.7)
    elif pr == "pattern":
        for x0, x1 in [(0.3, 3.0), (4.4, 5.6), (7.0, 9.7)]:
            rect(ax, x0, 2.8, x1 - x0, 1.0, "pr", lw=0.7)
    if exposed:
        for x0, x1 in exposed:
            rect(ax, x0, 2.8, x1 - x0, 1.0, "#c39bd3", lw=0.5, z=3)


def hotplate(ax):
    rect(ax, 0.0, 0.0, 10.0, 0.4, "#e57373", lw=0.6)
    for x in np.arange(1.0, 9.5, 1.6):
        xs = np.linspace(0, 0.5, 20)
        ax.plot(x + 0.15 * np.sin(xs * 20), 4.3 + xs * 1.6, color=C["red"], lw=1.0, alpha=0.7, zorder=8)


tt = ["① 표면 처리: 탈수 베이크 + HMDS", "② PR 스핀 코팅", "③ 소프트 베이크 (용매 날리기)",
      "④ 정렬 + 노광", "⑤ PEB (노광 후 베이크)", "⑥ 현상 (양성 PR: 빛 받은 곳 녹음)",
      "⑦ 하드 베이크", "⑧ 검사 (선폭, 오버레이, 결함)"]
f, axs = panels(8, 4, 3.4, 2.9, (0, 10), (0, 7.4), titles=tt, size=10)
a = axs
base(a[0])
for x in np.arange(0.6, 9.6, 0.45):
    circ(a[0], x, 2.95, 0.09, "#7cb342", lw=0.3)
text(a[0], 5.0, 5.0, "HMDS 증기", size=9, color=C["green"])
base(a[1], "full")
rect(a[1], 4.6, 5.3, 0.8, 1.2, "#bdbdbd", lw=0.6)
arrow(a[1], 5.0, 5.2, 5.0, 4.0, color="pink", lw=1.4)
a[1].add_patch(Arc((5.0, 0.15), 6.0, 0.6, theta1=200, theta2=340, color=C["blue"], lw=1.4, zorder=8))
text(a[1], 8.2, 5.6, "수천 rpm", size=9, color=C["blue"])
base(a[2], "full")
hotplate(a[2])
base(a[3], "full", exposed=[(3.0, 4.4), (5.6, 7.0)])
for x0, x1 in [(0.3, 3.0), (4.4, 5.6), (7.0, 9.7)]:
    rect(a[3], x0, 5.6, x1 - x0, 0.35, "#444444", lw=0.4)
rect(a[3], 0.3, 5.6, 9.4, 0.35, "none", lw=0.6)
for x in (3.4, 4.0, 6.0, 6.6):
    arrow(a[3], x, 7.1, x, 3.95, color="#8e44ad", ls="--", ms=8, lw=1.1)
text(a[3], 9.8, 6.4, "마스크", size=8.8, ha="right")
base(a[4], "full", exposed=[(3.0, 4.4), (5.6, 7.0)])
hotplate(a[4])
base(a[5], "pattern")
base(a[6], "pattern")
hotplate(a[6])
base(a[7], "pattern")
bracket(a[7], 4.4, 5.6, 4.15, "CD", size=9.5, color=C["blue"])
text(a[7], 5.0, 6.1, "통과 → 식각 / 이온주입\n불합격 → PR 벗기고 다시 (리워크)", size=8.8)
save(f, P, "photo_steps")

# 2. HMDS: 접촉각
f, axs = panels(2, 2, 5.2, 3.0, (0, 10), (0, 5.4),
                titles=["처리 전: 표면 -OH가 물을 끌어당김 (친수성)", "HMDS 후: 표면이 -CH₃로 덮임 (소수성)"],
                size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.5, 0.8, 9.0, 1.2, "ox", lw=0.7)
    if k == 0:
        th = np.linspace(0, np.pi, 60)
        ax.fill(5 + 3.4 * np.cos(th), 2.0 + 0.9 * np.sin(th), color="#9ecae1", zorder=3, ec="#3182bd")
        text(ax, 5.0, 3.6, "접촉각 작음 → 물이 퍼짐", size=9.5)
        for x in np.arange(1.0, 9.2, 0.7):
            text(ax, x, 1.4, "OH", size=7.5, color="#555555")
    else:
        ax.add_patch(Circle((5.0, 3.0), 1.2, fc="#9ecae1", ec="#3182bd", zorder=3))
        rect(ax, 3.4, 2.0, 3.2, 0.16, "white", lw=0, z=4)
        text(ax, 5.0, 4.75, "접촉각 큼 → PR이 잘 붙고 현상액이 계면으로 덜 스며듦", size=9.2)
        for x in np.arange(1.0, 9.2, 0.7):
            text(ax, x, 1.4, "CH₃", size=7.5, color="#555555")
save(f, P, "hmds")

# 3. 스핀 코팅
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.0), gridspec_kw=dict(width_ratios=[1.1, 1]))
canvas(0, 0, (0, 12), (0, 7.4), ax=ax1)
rect(ax1, 5.4, 0.2, 1.2, 1.6, "#9e9e9e", lw=0.6)
rect(ax1, 1.0, 1.8, 10.0, 0.35, "si", lw=0.7)
poly(ax1, [(1.0, 2.15), (11.0, 2.15), (11.0, 2.3), (1.0, 2.3)], "pr", lw=0.4)
rect(ax1, 5.65, 4.6, 0.7, 1.6, "#bdbdbd", lw=0.6)
arrow(ax1, 6.0, 4.5, 6.0, 2.5, color="pink", lw=2)
for sgn in (-1, 1):
    arrow(ax1, 6 + sgn * 4.6, 2.35, 6 + sgn * 5.6, 2.9, color="pink", lw=1.2, ms=8)
ax1.add_patch(Arc((6.0, 1.0), 3.0, 0.7, theta1=200, theta2=340, color=C["blue"], lw=1.5, zorder=8))
text(ax1, 6.0, 0.05, "척이 웨이퍼를 진공으로 잡고 회전", size=9)
text(ax1, 6.0, 7.05, "PR 떨어뜨리기 → 퍼짐 → 남는 건 밖으로 튐 → 용매 증발", size=9.5)
w = np.linspace(1000, 6000, 200)
for k, c, lab in [(1.0, PAL[0], "점도 낮은 PR"), (2.2, PAL[1], "점도 높은 PR")]:
    ax2.plot(w, k * np.sqrt(3000 / w), color=c, lw=2, label=lab)
ax2.set_xlabel("회전 속도 (rpm)")
ax2.set_ylabel("PR 두께 (µm)")
ax2.set_title("빨리 돌릴수록 얇아짐 (회전 속도의 제곱근에 반비례)", loc="left", fontsize=11)
ax2.grid(alpha=0.25)
ax2.legend()
plt.tight_layout()
save(f, P, "spin_coat")

# 4. 정재파
f, axs = panels(3, 3, 3.6, 3.2, (0, 10), (-0.4, 6.6),
                titles=["노광 직후: 측벽 물결 (정재파)", "PEB 후: 물결이 펴짐", "BARC를 깔면: 반사가 줄어듦"],
                size=10.5)
z = np.linspace(0, 3.0, 300)
for k, ax in enumerate(axs):
    rect(ax, 0.5, -0.2, 9.0, 1.0, "si", lw=0.6)
    y0 = 0.8
    if k == 2:
        rect(ax, 0.5, 0.8, 9.0, 0.35, "#8d6e63", lw=0.5)
        text(ax, 8.6, 0.97, "BARC", size=8, color="white")
        y0 = 1.15
    amp = [0.28, 0.07, 0.06][k]
    edge = 0.25 * (z / 3.0) + amp * np.sin(2 * np.pi * z / 0.75)
    xl = 3.0 + edge
    xr = 7.0 - edge
    for xe, side in [(xl, "L"), (xr, "R")]:
        if side == "L":
            pts = [(0.5, y0)] + list(zip(xe, y0 + z)) + [(0.5, y0 + 3.0)]
        else:
            pts = [(9.5, y0)] + list(zip(xe, y0 + z)) + [(9.5, y0 + 3.0)]
        poly(ax, pts, "pr", lw=0.7)
save(f, P, "standing_wave")

# 5. 트랙 + 스캐너
f, ax = canvas(11, 4.2, (0, 22), (0, 8.4))
rect(ax, 0.5, 0.8, 12.5, 6.4, "#f7f7f7", lw=1.0)
text(ax, 6.75, 7.6, "트랙 (코팅, 베이크, 현상)", size=11, weight="bold")
mods = [("FOUP\n투입", 1.0, 5.0, "#e0e0e0"), ("HMDS", 3.4, 5.0, "#e8f5e9"), ("코터", 5.8, 5.0, "#fce4ec"),
        ("소프트\n베이크", 8.2, 5.0, "#ffebee"), ("PEB", 8.2, 1.4, "#ffebee"), ("현상", 5.8, 1.4, "#ede7f6"),
        ("하드\n베이크", 3.4, 1.4, "#ffebee"), ("FOUP\n회수", 1.0, 1.4, "#e0e0e0")]
for s, x, y, c in mods:
    box(ax, x, y, 2.0, 1.6, s, fc=c, size=9.5)
order = [0, 1, 2, 3]
for i in range(3):
    arrow(ax, mods[i][1] + 2.05, 5.8, mods[i + 1][1] - 0.05, 5.8, lw=1.1, ms=9)
for i in range(4, 7):
    arrow(ax, mods[i][1] - 0.05, 2.2, mods[i + 1][1] + 2.05, 2.2, lw=1.1, ms=9)
box(ax, 15.0, 1.8, 6.4, 4.6, "스캐너 (노광기)", fc="#e3f2fd", size=11, weight="bold")
arrow(ax, 10.25, 5.8, 15.0, 5.0, lw=1.3, color="blue")
arrow(ax, 15.0, 3.0, 10.25, 2.2, lw=1.3, color="blue")
text(ax, 12.6, 6.0, "노광하러", size=9, color=C["blue"])
text(ax, 12.6, 1.8, "노광 끝", size=9, color=C["blue"])
save(f, P, "track_scanner")
