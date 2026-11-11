import numpy as np
from common import *

P = 16

# 1. 식각 기본 순서
tt = ["① photo 끝난 상태", "② 식각: PR 없는 곳의 막 제거", "③ 과식각: 남은 막을 확실히 제거", "④ PR 제거 (ashing + 세정)"]
f, axs = panels(4, 4, 3.2, 2.6, (0, 10), (0, 5.4), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.6, "si", lw=0.6)
    pats = [(0.3, 3.4), (6.6, 9.7)]
    if k == 0:
        rect(ax, 0.3, 1.9, 9.4, 1.0, "ox", lw=0.6)
    else:
        for a, b in pats:
            rect(ax, a, 1.9, b - a, 1.0, "ox", lw=0.6)
    if k == 2:
        rect(ax, 3.4, 1.7, 3.2, 0.2, "white", lw=0.0)
        line(ax, [3.4, 3.4, 6.6, 6.6], [1.9, 1.7, 1.7, 1.9], lw=0.6)
    if k == 3:
        rect(ax, 3.4, 1.7, 3.2, 0.2, "white", lw=0.0)
        line(ax, [3.4, 3.4, 6.6, 6.6], [1.9, 1.7, 1.7, 1.9], lw=0.6)
    if k < 3:
        for a, b in pats:
            rect(ax, a, 2.9, b - a, 1.0, "pr", lw=0.6)
    if k == 1:
        for x in (4.2, 5.0, 5.8):
            arrow(ax, x, 5.2, x, 2.0, color="#555555", lw=1.1, ms=8)
    if k == 2:
        text(ax, 5.0, 1.15, "아래 Si가 살짝 파임", size=8.6, color=C["red"])
save(f, P, "etch_flow")

# 2. 등방성 / 이방성
f, axs = panels(3, 3, 3.8, 3.3, (0, 10), (0, 6.8), titles=["등방성 (습식, radical)", "이방성 (RIE)", "중간 (경사 측벽)"],
                size=11)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.4, "si", lw=0.6)
    if k == 0:
        th = np.linspace(np.pi / 2, 0, 40)
        r = 2.0
        poly(ax, [(0.3, 1.7), (3.6, 1.7)] + [(3.6 - r * np.cos(t), 3.7 - r * np.sin(t)) for t in th] + [(0.3, 3.7)],
             "ox", lw=0.6)
        poly(ax, [(9.7, 1.7), (6.4, 1.7)] + [(6.4 + r * np.cos(t), 3.7 - r * np.sin(t)) for t in th] + [(9.7, 3.7)],
             "ox", lw=0.6)
        rect(ax, 0.3, 3.7, 3.3, 0.8, "pr", lw=0.6)
        rect(ax, 6.4, 3.7, 3.3, 0.8, "pr", lw=0.6)
        bracket(ax, 1.6, 3.6, 4.7, "undercut", size=9, color=C["red"])
    elif k == 1:
        rect(ax, 0.3, 1.7, 3.3, 2.0, "ox", lw=0.6)
        rect(ax, 6.4, 1.7, 3.3, 2.0, "ox", lw=0.6)
        rect(ax, 0.3, 3.7, 3.3, 0.8, "pr", lw=0.6)
        rect(ax, 6.4, 3.7, 3.3, 0.8, "pr", lw=0.6)
    else:
        poly(ax, [(0.3, 1.7), (3.0, 1.7), (3.6, 3.7), (0.3, 3.7)], "ox", lw=0.6)
        poly(ax, [(9.7, 1.7), (7.0, 1.7), (6.4, 3.7), (9.7, 3.7)], "ox", lw=0.6)
        rect(ax, 0.3, 3.7, 3.3, 0.8, "pr", lw=0.6)
        rect(ax, 6.4, 3.7, 3.3, 0.8, "pr", lw=0.6)
text(axs[0], 5.0, 6.35, "옆으로도 같은 속도로 깎임", size=9)
text(axs[1], 5.0, 6.35, "아래로만 깎임 → 미세 pattern에 필수", size=9)
text(axs[2], 5.0, 6.35, "측벽 보호막이 조금 많을 때", size=9)
save(f, P, "iso_aniso")

# 3. 용어 정리 그림
f, ax = canvas(10.5, 5.2, (0, 21), (0, 10.4))
rect(ax, 0.5, 0.5, 20, 2.8, "si", lw=0.7)
rect(ax, 8.2, 2.85, 4.6, 0.45, "white", lw=0)
line(ax, [8.2, 8.2, 12.8, 12.8], [3.3, 2.85, 2.85, 3.3], lw=0.7)
poly(ax, [(0.5, 3.3), (8.2, 3.3), (8.5, 7.3), (0.5, 7.3)], "ox", lw=0.7)
poly(ax, [(20.5, 3.3), (12.8, 3.3), (12.5, 7.3), (20.5, 7.3)], "ox", lw=0.7)
rect(ax, 0.5, 7.3, 7.5, 1.2, "pr", lw=0.7)
rect(ax, 13.0, 7.3, 7.5, 1.2, "pr", lw=0.7)
bracket(ax, 8.0, 13.0, 8.9, "식각 전 CD (PR 기준)", size=9.5, color=C["blue"])
bracket(ax, 8.2, 12.8, 2.2, "식각 후 CD (바닥)", size=9.5, color=C["green"], below=True)
vdim(ax, 15.0, 3.3, 7.3, "식각 깊이 h", size=9.5)
text(ax, 10.5, 5.3, "종횡비\n= h / 폭", size=9.5)
arrow(ax, 6.0, 1.3, 9.0, 3.05, lw=0.8, ms=7)
text(ax, 4.0, 1.0, "과식각으로 파인 깊이\n→ 선택비가 클수록 작음", size=9, box="white")
text(ax, 10.5, 9.95, "식각 편차 (etch bias) = 식각 후 CD − 식각 전 CD", size=10)
save(f, P, "terms")

# 4. 습식 식각 단계
f, ax = canvas(9.5, 4.0, (0, 19), (0, 8))
rect(ax, 0.5, 0.5, 18, 2.2, "ox", lw=0.7)
rect(ax, 0.5, 2.7, 18, 4.8, "#e3f2fd", lw=0.0, alpha=0.6)
text(ax, 17.8, 7.0, "식각액", size=10, ha="right", color=C["blue"])
for x, y in [(2.5, 6.0), (3.3, 5.0), (2.0, 4.2)]:
    circ(ax, x, y, 0.3, "#ef9a9a", lw=0.5)
arrow(ax, 3.2, 4.8, 4.6, 3.1, color="red", lw=1.4)
text(ax, 3.0, 1.6, "① 반응물이 표면까지\n이동 (확산)", size=9.5)
circ(ax, 9.5, 3.05, 0.3, "#ef9a9a", lw=0.5)
circ(ax, 10.2, 3.0, 0.3, "#90a4ae", lw=0.5)
text(ax, 9.8, 1.6, "② 표면에서 반응", size=9.5)
circ(ax, 15.6, 4.2, 0.3, "#fff59d", lw=0.5)
circ(ax, 16.4, 5.4, 0.3, "#fff59d", lw=0.5)
arrow(ax, 15.0, 3.1, 16.0, 5.6, color="green", lw=1.4)
text(ax, 15.8, 1.6, "③ 생성물이 녹아서\n멀어짐", size=9.5)
save(f, P, "wet_steps")

# 5. KOH 이방성 식각
f, axs = panels(2, 2, 5.2, 3.4, (0, 10), (0, 6.2), titles=["좁은 창: V 홈", "넓은 창: 평평한 바닥 + 경사면"], size=11)
ang = np.deg2rad(54.74)
for k, ax in enumerate(axs):
    w = 3.0 if k == 0 else 5.4
    a, b = 5 - w / 2, 5 + w / 2
    depth = (w / 2) * np.tan(ang) if k == 0 else 2.2
    bot = 4.4 - depth
    if k == 0:
        pts = [(0.3, 0.3), (9.7, 0.3), (9.7, 4.4), (b, 4.4), (5.0, bot), (a, 4.4), (0.3, 4.4)]
    else:
        dx = depth / np.tan(ang)
        pts = [(0.3, 0.3), (9.7, 0.3), (9.7, 4.4), (b, 4.4), (b - dx, bot), (a + dx, bot), (a, 4.4), (0.3, 4.4)]
    poly(ax, pts, "si", lw=0.7)
    rect(ax, 0.3, 4.4, a - 0.3, 0.4, "nit", lw=0.6)
    rect(ax, b, 4.4, 9.7 - b, 0.4, "nit", lw=0.6)
    ax.add_patch(Arc((b, 4.4), 1.6, 1.6, theta1=180 + 0, theta2=180 + 54.74, color=C["red"], lw=1.2, zorder=8))
    text(ax, b - 1.2, 4.0, "54.7°", size=9.5, color=C["red"])
text(axs[0], 5.0, 5.6, "(111)면은 거의 안 깎여서 멈춤", size=9.5)
text(axs[1], 5.0, 5.6, "(100) wafer, KOH / TMAH", size=9.5)
save(f, P, "koh")

# 6. 균일도 지도
n = 200
xx, yy = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, n))
rr = np.hypot(xx, yy)
er = 100 * (1 + 0.06 * (1 - rr ** 2) - 0.02 * xx)
er[rr > 1] = np.nan
f, ax = plt.subplots(figsize=(6.2, 5.0))
im = ax.imshow(er, extent=[-150, 150, -150, 150], origin="lower", cmap="RdYlBu_r")
plt.colorbar(im, ax=ax, label="식각률 (nm/min, 예시)")
ax.set_xlabel("x (mm)")
ax.set_ylabel("y (mm)")
mx, mn, av = np.nanmax(er), np.nanmin(er), np.nanmean(er)
ax.set_title(f"균일도 = (최대 − 최소) / (2 × 평균) = {100 * (mx - mn) / (2 * av):.1f} %", loc="left", fontsize=11)
save(f, P, "uniformity")
