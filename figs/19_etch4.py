import numpy as np
from common import *

P = 19

# 1. ARDE (RIE lag)
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.2), gridspec_kw=dict(width_ratios=[1.2, 1]))
canvas(0, 0, (0, 16), (0, 8), ax=ax1)
ax1.set_title("같은 시간 식각: 좁을수록 얕음", loc="left", fontsize=11)
rect(ax1, 0.3, 0.3, 15.4, 6.6, "ox", lw=0.6)
x = 1.2
for w in (3.0, 1.8, 1.0, 0.6):
    AR_guess = 1
    depth = 5.6 / (1 + 0.55 * (5.6 / w) * 0.35)
    rect(ax1, x, 6.9 - depth, w, depth, "white", lw=0.6, z=3)
    text(ax1, x + w / 2, 6.9 - depth - 0.45, f"{depth:.1f}", size=9)
    x += w + 1.6
rect(ax1, 0.3, 6.9, 15.4, 0.7, "pr", lw=0.6, z=2)
text(ax1, 8.0, -0.15, "숫자 = 깊이 (상대값)", size=9, va="bottom")
ar = np.linspace(0, 40, 200)
ax2.plot(ar, 1 / (1 + 0.04 * ar), color=PAL[0], lw=2.2)
ax2.set_xlabel("종횡비 (깊이 / 폭)")
ax2.set_ylabel("식각률 (얕을 때 대비)")
ax2.set_ylim(0, 1.05)
ax2.set_title("깊어질수록 반응종이 바닥까지 잘 못 감 (개념)", loc="left", fontsize=11)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "arde")

# 2. loading 효과
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.0), gridspec_kw=dict(width_ratios=[1.2, 1]))
canvas(0, 0, (0, 16), (0, 7), ax=ax1)
ax1.set_title("micro loading: pattern이 빽빽한 곳이 덜 깎임", loc="left", fontsize=11)
rect(ax1, 0.3, 0.3, 15.4, 5.6, "ox", lw=0.6)
for x0 in np.arange(1.0, 7.5, 1.3):
    rect(ax1, x0, 2.6, 0.65, 3.3, "white", lw=0.6, z=3)
rect(ax1, 11.0, 2.0, 0.65, 3.9, "white", lw=0.6, z=3)
rect(ax1, 0.3, 5.9, 15.4, 0.6, "pr", lw=0.6, z=2)
text(ax1, 4.2, 1.6, "밀집: 반응종을 나눠 씀", size=9.5)
text(ax1, 11.3, 1.2, "고립", size=9.5)
A = np.linspace(0, 1, 200)
ax2.plot(A * 100, 1 / (1 + 1.5 * A), color=PAL[1], lw=2.2)
ax2.set_xlabel("wafer에서 식각되는 면적 비율 (%)")
ax2.set_ylabel("식각률 (상대값)")
ax2.set_title("macro loading: 깎을 면적이 넓으면 느려짐 (개념)", loc="left", fontsize=11)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "loading")

# 3. profile 불량
tt = ["정상 (수직)", "bowing (가운데가 부풂)", "taper (아래가 좁음)", "notching (바닥 옆이 파임)", "micro trench",
      "식각 멈춤 (Not open)"]
f, axs = panels(6, 6, 2.3, 3.3, (0, 6), (0, 8.4), titles=tt, size=9.5)
for k, ax in enumerate(axs):
    rect(ax, 0.2, 0.2, 5.6, 1.0, "si" if k != 3 else "ox", lw=0.6)
    L, R_ = 2.2, 3.8
    ys = np.linspace(1.2, 6.8, 40)
    if k == 0:
        xl = np.full_like(ys, L)
    elif k == 1:
        xl = L - 0.45 * np.sin(np.pi * (ys - 1.2) / 5.6)
    elif k == 2:
        xl = L + 0.6 * (6.8 - ys) / 5.6
    else:
        xl = np.full_like(ys, L)
    xr = 6.0 - xl
    bot = 1.2
    if k == 5:
        bot = 3.6
        ys = np.linspace(3.6, 6.8, 30)
        xl = np.full_like(ys, L)
        xr = 6.0 - xl
    poly(ax, [(0.2, 1.2), (0.2, 6.8)] + list(zip(xl[::-1], ys[::-1])) + [(xl[0], bot)][:0] + [(L if k != 2 else xl[0], bot)][:0], "ox", lw=0.6)
    poly(ax, [(5.8, 1.2), (5.8, 6.8)] + list(zip(xr[::-1], ys[::-1])), "ox", lw=0.6)
    if k == 5:
        rect(ax, 0.2, 1.2, 5.6, 2.4, "ox", lw=0.0)
        line(ax, [L, R_], [3.6, 3.6], lw=0.6)
        rect(ax, 2.3, 3.6, 1.4, 0.25, "#6d4c41", lw=0)
        text(ax, 3.0, 2.4, "polymer가 쌓여서 멈춤", size=8.3)
    if k == 3:
        poly(ax, [(L, 1.2), (L - 0.7, 1.2), (L, 1.7)], "white", lw=0.6, z=3)
        poly(ax, [(R_, 1.2), (R_ + 0.7, 1.2), (R_, 1.7)], "white", lw=0.6, z=3)
    if k == 4:
        poly(ax, [(L, 1.2), (L + 0.35, 1.2), (L + 0.15, 0.8)], "white", lw=0.6, z=3)
        poly(ax, [(R_, 1.2), (R_ - 0.35, 1.2), (R_ - 0.15, 0.8)], "white", lw=0.6, z=3)
    rect(ax, 0.2, 6.8, 2.0, 0.7, "pr", lw=0.6)
    rect(ax, 3.8, 6.8, 2.0, 0.7, "pr", lw=0.6)
save(f, P, "profiles")

# 4. charging → notching
f, ax = canvas(8.4, 5.6, (0, 14), (0, 9.2))
rect(ax, 0.5, 0.5, 13, 1.6, "ox", lw=0.6)
text(ax, 2.0, 1.3, "절연막 (밑)", size=9)
rect(ax, 0.5, 2.1, 4.5, 4.0, "poly", lw=0.6)
rect(ax, 9.0, 2.1, 4.5, 4.0, "poly", lw=0.6)
rect(ax, 0.5, 6.1, 4.5, 1.6, "pr", lw=0.6)
rect(ax, 9.0, 6.1, 4.5, 1.6, "pr", lw=0.6)
for y in np.arange(6.3, 7.6, 0.4):
    text(ax, 5.25, y, "−", size=12, color=C["blue"], weight="bold")
    text(ax, 8.75, y, "−", size=12, color=C["blue"], weight="bold")
for x in np.arange(5.6, 8.6, 0.6):
    text(ax, x, 2.35, "+", size=12, color=C["red"], weight="bold")
for a in (-50, -20, 20, 50):
    arrow(ax, 7.0, 9.0, 7.0 + 2.6 * np.sin(np.deg2rad(a)), 9.0 - 2.6 * np.cos(np.deg2rad(a)), color="blue", lw=1.0, ms=7)
text(ax, 10.6, 8.6, "전자: 사방에서 → 위쪽 PR 벽에\n먼저 붙음 (−)", size=9, color=C["blue"], ha="left")
arrow(ax, 6.2, 8.8, 6.2, 3.0, color="red", lw=1.3)
ax.add_patch(FancyArrowPatch((7.6, 8.8), (5.25, 2.4), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>",
                             mutation_scale=10, color=C["red"], lw=1.3, zorder=9))
text(ax, 2.2, 8.6, "ion: 수직으로 와서 바닥이 (+)\n→ 뒤에 오는 ion이 옆으로 휨", size=9, color=C["red"], ha="center")
poly(ax, [(5.0, 2.1), (5.0, 2.6), (4.5, 2.1)], "white", lw=0.6, z=4)
poly(ax, [(9.0, 2.1), (9.0, 2.6), (9.5, 2.1)], "white", lw=0.6, z=4)
text(ax, 3.3, 3.0, "notching", size=10, color=C["red"], weight="bold")
save(f, P, "charging")

# 5. ALE
tt = ["① 개질: Cl₂가 표면 한 층에만 붙음", "② purge: 남은 Cl₂ 빼냄", "③ 제거: 낮은 energy Ar⁺로 개질층만 떼어냄",
      "④ purge → ①부터 반복"]
f, axs = panels(4, 4, 3.4, 2.8, (0, 10), (0, 6.0), titles=tt, size=9.8)
for k, ax in enumerate(axs):
    for i in range(4):
        for j in range(12):
            y = 0.6 + i * 0.6
            if k == 3 and i == 3:
                continue
            circ(ax, 0.75 + j * 0.78, y, 0.28, "#cfd8dc", lw=0.4)
    if k in (0, 1, 2):
        for j in range(12):
            circ(ax, 0.75 + j * 0.78, 2.95, 0.15, "#81c784", lw=0.3, z=4)
    if k == 0:
        for x, y in [(2.0, 4.8), (4.5, 5.2), (7.0, 4.6), (8.5, 5.3)]:
            circ(ax, x - 0.15, y, 0.15, "#81c784", lw=0.3)
            circ(ax, x + 0.15, y, 0.15, "#81c784", lw=0.3)
    if k == 2:
        for x in (2.0, 5.0, 8.0):
            arrow(ax, x, 5.6, x, 3.4, color="red", lw=1.2, ms=7)
        text(ax, 5.0, 4.4, "SiClₓ 같이 날아감", size=8.6, box="white")
save(f, P, "ale_cycle")

E = np.linspace(0, 100, 300)
epc = np.where(E < 20, 0.55 * E / 20, 0.55) + np.where(E > 60, 0.03 * (E - 60), 0)
f, ax = plot_ax(6.8, 3.8)
ax.plot(E, epc, color=PAL[0], lw=2.4)
ax.axvspan(20, 60, color="#c8e6c9", alpha=0.6)
ax.text(40, 1.3, "ALE 창: 한 cycle에\n한 층 정도만 깎임", ha="center", fontsize=9.5)
ax.text(8, 0.85, "개질층도\n못 떼어냄", fontsize=9, ha="center")
ax.text(82, 0.45, "아래 Si까지\nsputter됨", fontsize=9, ha="center")
ax.set_ylim(0, 1.8)
ax.set_xlabel("ion energy (eV)")
ax.set_ylabel("cycle당 식각 두께 (nm)")
ax.set_title("ALE 창 (개념)", loc="left")
save(f, P, "ale_window")

# 6. Bosch 공정
tt = ["① SF₆ 식각 (등방성, 짧게)", "② C₄F₈ 보호막 (전체에)", "③ 바닥 보호막만 제거 → 다시 식각",
      "④ 반복 → 깊은 홈 (scallop)"]
f, axs = panels(4, 4, 3.0, 4.2, (0, 8), (0, 11), titles=tt, size=9.8)


def bosch(ax, n, pas=False, last_open=False):
    rect(ax, 0.3, 0.3, 7.4, 9.0, "si", lw=0.6)
    L, R_ = 3.0, 5.0
    pts_l, pts_r = [], []
    y = 9.3
    for i in range(n):
        th = np.linspace(np.pi / 2, -np.pi / 2, 20)
        for t in th:
            pts_l.append((L - 0.35 * np.cos(t), y - 0.8 + 0.8 * np.sin(t)))
            pts_r.append((R_ + 0.35 * np.cos(t), y - 0.8 + 0.8 * np.sin(t)))
        y -= 1.6
    bot = y
    poly(ax, [(L, 9.3)] + pts_l + [(L, bot), (R_, bot)] + pts_r[::-1][::-1][:0] + list(reversed(pts_r)) + [(R_, 9.3)],
         "white", lw=0.6, z=3)
    if pas:
        ax.plot([p[0] for p in pts_l], [p[1] for p in pts_l], color="#6d4c41", lw=2.2, zorder=4)
        ax.plot([p[0] for p in pts_r], [p[1] for p in pts_r], color="#6d4c41", lw=2.2, zorder=4)
        if not last_open:
            line(ax, [L, R_], [bot, bot], color="#6d4c41", lw=2.2)
    rect(ax, 0.3, 9.3, 2.7, 0.8, "pr", lw=0.6, z=5)
    rect(ax, 5.0, 9.3, 2.7, 0.8, "pr", lw=0.6, z=5)


bosch(axs[0], 1)
bosch(axs[1], 1, pas=True)
bosch(axs[2], 2, pas=True, last_open=True)
bosch(axs[3], 5, pas=False)
for x in (3.5, 4.0, 4.5):
    arrow(axs[2], x, 10.9, x, 7.9, color="red", lw=1.0, ms=7)
text(axs[3], 4.0, 0.9, "MEMS, TSV(37편)", size=9, box="white")
save(f, P, "bosch")
