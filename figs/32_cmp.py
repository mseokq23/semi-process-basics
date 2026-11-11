import numpy as np
from common import *
import cmos

P = 32

# 1. 평탄화 없이 쌓으면
f, axs = panels(2, 2, 5.4, 3.6, (0, 12), (-0.5, 7.4), titles=["평탄화 없이 쌓으면: 굴곡이 층마다 커짐",
                                                           "층마다 CMP: 매번 평평한 위에서 시작"], size=10.5)
LINES = [(2.3, 3.7), (7.3, 9.2)]
for k, ax in enumerate(axs):
    rect(ax, 0, -0.5, 12, 0.5, "si", lw=0.5)
    if k == 0:
        xs = np.linspace(0, 12, 1201)
        prof = np.zeros_like(xs)
        for i in range(3):
            tops = prof.copy()
            boxes = []
            for (a_, b_) in LINES:
                m = (xs >= a_) & (xs <= b_)
                base = prof[m].max()
                tops[m] = base + 0.45
                boxes.append((a_, base))
            r = 45
            dil = np.array([tops[max(0, j - r):j + r + 1].max() for j in range(len(xs))])
            new = np.convolve(dil, np.ones(31) / 31, mode="same")
            new[:20], new[-20:] = dil[:20], dil[-20:]
            new = np.maximum(new, tops) + 1.0
            ax.fill_between(xs, prof, new, color=C["ox"], ec="#333333", lw=0.6, zorder=2 + i * 0.1)
            for (a_, base) in boxes:
                rect(ax, a_, base, LINES[0][1] - LINES[0][0] if a_ == LINES[0][0] else LINES[1][1] - LINES[1][0],
                     0.45, "al", lw=0.5, z=3 + i * 0.1)
            prof = new
        text(ax, 6.0, 6.9, "위로 갈수록 단차 누적", size=9.5, color=C["red"])
    else:
        lvl = 0.0
        for i in range(3):
            rect(ax, 0, lvl, 12, 1.6, "ox", lw=0.6)
            for a_, b_ in LINES:
                rect(ax, a_, lvl + 1.6 - 0.5, b_ - a_, 0.5, "cu", lw=0.5, z=3)
            lvl += 1.6
        text(ax, 6.0, 6.9, "층이 몇 개든 표면이 평평", size=9.5, color=C["green"])
save(f, P, "why_cmp")

# 2. 초점 심도와 단차
x = np.linspace(0, 12, 600)
surf = 0.25 * np.tanh((x - 3) * 3) - 0.25 * np.tanh((x - 7) * 3) + 0.15 * np.tanh((x - 9.5) * 2)
f, axs = plt.subplots(1, 2, figsize=(11.6, 3.4), sharey=True)
for ax, s, title in [(axs[0], surf * 2.4, "단차가 크면: 일부가 초점 범위 밖"), (axs[1], surf * 0.3, "평탄화 후: 전부 초점 범위 안")]:
    ax.fill_between(x, -1.6, s, color=C["ox"], ec="#333333", lw=0.8)
    ax.axhspan(-0.45, 0.45, color=C["green"], alpha=0.15)
    ax.axhline(0.45, color=C["green"], lw=1.0, ls="--")
    ax.axhline(-0.45, color=C["green"], lw=1.0, ls="--")
    ax.text(11.9, 0.52, "초점 심도 (DoF)", ha="right", fontsize=9.5, color=C["green"])
    bad = (s > 0.45) | (s < -0.45)
    ax.plot(x[bad], s[bad], ".", color=C["red"], ms=2.5)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlim(0, 12)
    ax.set_title(title, loc="left", fontsize=10.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
axs[0].text(5.0, 1.25, "빨간 부분: 패턴이 흐려짐 (11편)", fontsize=9.5, color=C["red"], ha="center")
plt.tight_layout()
save(f, P, "dof_topography")

# 3. 평탄화 정도
tt = ["① 원래 모양", "② 매끄럽게만 (smoothing)", "③ 국부 평탄화", "④ 전체 평탄화 (CMP)"]
f, axs = panels(4, 4, 3.1, 2.3, (0, 10), (-0.4, 4.0), titles=tt, size=10)
for k, ax in enumerate(axs):
    rect(ax, 0, -0.4, 10, 0.4, "si", lw=0.5)
    for a, b in [(1.0, 2.0), (2.6, 3.6), (6.0, 9.0)]:
        rect(ax, a, 0, b - a, 0.8, "al", lw=0.5, z=3)
    xx = np.linspace(0, 10, 400)
    raw = 1.6 + 0.8 * (((xx > 0.8) & (xx < 3.8)) | ((xx > 5.8) & (xx < 9.2)))
    if k == 0:
        top = raw
    elif k == 1:
        top = np.convolve(raw, np.ones(25) / 25, mode="same")
        top[:12], top[-12:] = raw[:12], raw[-12:]
    elif k == 2:
        top = 1.6 + 0.8 * ((xx > 0.6) & (xx < 9.4)) * 1.0
        top = np.convolve(top, np.ones(31) / 31, mode="same")
        top[:15], top[-15:] = 1.6, 1.6
        top = np.where((xx > 3.8) & (xx < 5.8), top - 0.25, top)
    else:
        top = np.full_like(xx, 1.9)
    ax.fill_between(xx, 0, top, color=C["ox"], ec="#333333", lw=0.7, zorder=2)
save(f, P, "planarity")

# 4. CMP 장비
f, ax = canvas(10.5, 4.6, (0, 22), (-1.4, 8.4))
ax.add_patch(Ellipse((10, 1.2), 17.0, 2.2, fc="#b0bec5", ec="#333333", lw=0.8, zorder=2))
rect(ax, 1.5, -0.6, 17.0, 1.8, "#b0bec5", lw=0.0, z=1.9)
ax.add_patch(Ellipse((10, -0.6), 17.0, 2.2, fc="#90a4ae", ec="#333333", lw=0.8, zorder=1.8))
ax.add_patch(Ellipse((10, 1.6), 17.0, 2.2, fc="#ffe0b2", ec="#333333", lw=0.8, zorder=2.2))
text(ax, 10, 1.6, "패드 (폴리우레탄)", size=9.5, z=21)
text(ax, 10, -0.9, "플래튼 (회전)", size=9.5)
rect(ax, 5.0, 2.3, 4.0, 0.8, "#78909c", lw=0.8, z=4)
rect(ax, 5.3, 2.05, 3.4, 0.25, "si", lw=0.6, z=4.1)
rect(ax, 6.6, 3.1, 0.8, 2.6, "#9e9e9e", lw=0.7, z=4)
text(ax, 7.0, 6.2, "캐리어 헤드: 웨이퍼를\n아래로 누르면서 회전", size=9.2)
arrow(ax, 4.3, 3.3, 4.3, 2.4, color=C["red"], lw=1.4, ms=10)
text(ax, 3.9, 3.7, "압력", size=9, color=C["red"])
text(ax, 7.0, 1.95, "웨이퍼 (면이 아래)", size=8.2, va="top", z=22)
line(ax, [12.0, 12.0, 13.0], [6.2, 4.0, 3.6], color="#555555", lw=2.2)
for yy in (3.1, 2.7, 2.35):
    circ(ax, 13.05, yy, 0.09, "#fff59d", lw=0.4, z=5)
text(ax, 12.0, 6.7, "슬러리 공급\n(연마 입자 + 화학액)", size=9.2)
ax.add_patch(Ellipse((15.6, 2.25), 2.4, 0.6, fc="#bdbdbd", ec="#333333", lw=0.8, zorder=4))
rect(ax, 15.3, 2.55, 0.6, 2.0, "#9e9e9e", lw=0.7, z=4)
text(ax, 17.9, 4.8, "컨디셔너 (다이아몬드 디스크):\n패드 표면을 계속 거칠게 유지", size=9.2)
ax.add_patch(FancyArrowPatch((11.5, 0.75), (16.6, 1.15), connectionstyle="arc3,rad=0.12", arrowstyle="-|>",
                             mutation_scale=13, color="#555555", lw=1.3, zorder=6))
text(ax, 14.0, 0.45, "회전", size=9, color="#555555", z=21)
save(f, P, "cmp_tool")

# 5. 단차 줄어드는 모습 (간단 모델)
K_V = 200.0                                 # 평평한 막 기준 제거 속도 (nm/min)
rho_up, hc = 0.5, 250.0
h0 = 600.0
dt = 0.005
t = np.arange(0, 6, dt)
zu, zd = np.zeros_like(t), np.zeros_like(t)
zu[0], zd[0] = 1600.0, 1000.0
for i in range(1, len(t)):
    h = zu[i - 1] - zd[i - 1]
    if h >= hc:
        pu, pd = 1 / rho_up, 0.0
    else:
        pu = 1 / (rho_up + (1 - rho_up) * (1 - h / hc))
        pd = pu * (1 - h / hc)
    zu[i] = zu[i - 1] - K_V * pu * dt
    zd[i] = zd[i - 1] - K_V * pd * dt
f, ax = plot_ax(7.2, 4.2)
ax.plot(t, zu, color=PAL[1], lw=2.2, label="튀어나온 곳 높이")
ax.plot(t, zd, color=PAL[0], lw=2.2, label="들어간 곳 높이")
ax.fill_between(t, zd, zu, color="#eeeeee")
ax.text(0.9, 1120, "단차", fontsize=10)
ax.set_xlabel("연마 시간 (분)")
ax.set_ylabel("막 높이 (nm)")
ax.set_title("튀어나온 곳이 압력을 더 받아서 먼저 깎임 → 단차가 줄어듦 (간단 모델)", loc="left", fontsize=10.5)
ax.legend(fontsize=9.5)
save(f, P, "step_height")

# 6. STI CMP
steps = [("① HDP 산화막으로 트렌치 채운 직후", dict(pad="active", sti="fill")),
         ("② CMP: 질화막이 드러나면 멈춤", dict(pad="active", sti="cmp")),
         ("③ 질화막 제거 (인산) → STI 완성", dict(sti="final"))]
f, axs = panels(3, 3, 4.4, 2.4, (0.0, 14.0), (-2.2, 2.9), titles=[s for s, _ in steps], size=10)
for ax, (_, st) in zip(axs, steps):
    cmos.draw(ax, st, lab=False)
text(axs[1], 7.0, 2.35, "세리아 슬러리: 산화막은 잘, 질화막은 거의 안 깎음", size=8.4, color=C["red"])
text(axs[0], 6.0, 0.4, "질화막", size=8.4)
text(axs[0], 12.0, -0.9, "STI", size=8.4)
save(f, P, "sti_cmp")

# 7. Cu CMP 단계
tt = ["① 도금 직후: Cu가 넘쳐 있음", "② 1단계: Cu 제거, 배리어에서 멈춤", "③ 2단계: 배리어 제거 + 살짝 더 연마"]
f, axs = panels(3, 3, 4.2, 2.6, (0, 14), (-0.6, 4.6), titles=tt, size=10)
lines_ = [(1.0, 1.6), (2.4, 3.0), (4.6, 9.6), (10.6, 11.0), (11.4, 11.8), (12.2, 12.6), (13.0, 13.4)]
TOP, T = 2.0, 0.12
for k, ax in enumerate(axs):
    rect(ax, 0, -0.6, 14, 0.6, "nit", lw=0.5)
    top = TOP if k < 2 else TOP - 0.1
    rect(ax, 0, 0, 14, top, "lowk", lw=0.6)
    for a, b in lines_:
        rect(ax, a, 0.3, b - a, top - 0.3 + (T if k < 2 else 0), "tin", lw=0.4, z=3)
        rect(ax, a + T * 0.6, 0.3 + T * 0.6, b - a - 1.2 * T, top - 0.3 - T * 0.6 + (T if k < 2 else 0), "cu",
             lw=0.0, z=3.1)
    if k < 2:
        edges = [0.0] + [v for ab in lines_ for v in ab] + [14.0]
        for j in range(0, len(edges), 2):
            rect(ax, edges[j], TOP, edges[j + 1] - edges[j], T, "tin", lw=0.4, z=3.2)
    if k == 0:
        rect(ax, 0, TOP + T, 14, 1.3, "cu", lw=0.5, z=3.1)
    if k == 1:
        text(ax, 7.0, 3.0, "Cu와 배리어 높이가 같아짐", size=8.6, color="#444444")
    if k == 2:
        text(ax, 7.0, 3.0, "절연막과 Cu가 같은 높이 (배선 분리)", size=8.6, color="#444444")
save(f, P, "cu_cmp_steps")

# 8. 디싱과 이로전
f, ax = canvas(11.6, 3.9, (0, 26), (-1.4, 6.6))
rect(ax, 0, -1.4, 26, 1.4, "nit", lw=0.5)
TOP = 3.0
xx = np.linspace(0, 26, 1300)
top = np.full_like(xx, TOP)
dense = (xx > 15.0) & (xx < 24.0)
top = np.where(dense, TOP - 0.45 * np.sin(np.pi * np.clip((xx - 15.0) / 9.0, 0, 1)) ** 0.5, top)
ax.fill_between(xx, 0, top, color=C["lowk"], ec="#333333", lw=0.7, zorder=2)
# 넓은 배선: 디싱
a, b = 5.0, 12.0
xs = np.linspace(a, b, 100)
dish = TOP - 0.6 * np.sin(np.pi * (xs - a) / (b - a))
rect(ax, a, 0.6, b - a, TOP - 0.6, "tin", lw=0.4, z=3)
ax.fill_between(xs, 0.72, dish, color=C["cu"], ec="#333333", lw=0.6, zorder=3.1)
ax.fill_between(xs[1:-1], dish[1:-1], TOP + 0.01, color="white", zorder=3.2)
rect(ax, a, 0.6, 0.12, TOP - 0.6, "tin", lw=0.3, z=3.3)
rect(ax, b - 0.12, 0.6, 0.12, TOP - 0.6, "tin", lw=0.3, z=3.3)
rect(ax, 1.5, 0.6, 1.0, TOP - 0.6, "tin", lw=0.4, z=3)
rect(ax, 1.62, 0.72, 0.76, TOP - 0.72, "cu", lw=0.0, z=3.1)
for x0 in np.arange(15.4, 23.6, 0.9):
    xm = x0 + 0.25
    tl = TOP - 0.45 * np.sin(np.pi * (xm - 15.0) / 9.0) ** 0.5
    rect(ax, x0, 0.6, 0.5, tl - 0.6, "tin", lw=0.3, z=3)
    rect(ax, x0 + 0.08, 0.68, 0.34, tl - 0.68, "cu", lw=0.0, z=3.1)
line(ax, [0, 26], [TOP, TOP], color="#555555", lw=0.9, ls="--", z=6)
text(ax, 25.8, TOP + 0.3, "원래 목표 높이", size=9, ha="right", color="#555555")
text(ax, 8.5, 4.6, "디싱: 넓은 Cu가 접시처럼 파임\n(Cu가 더 무르고 패드가 휘어 들어감)", size=9.5, color=C["red"])
arrow(ax, 8.5, 3.95, 8.5, TOP - 0.45, color=C["red"], lw=1.0, ms=8)
text(ax, 19.5, 4.6, "이로전: 촘촘한 곳은 절연막까지\n같이 깎여 전체가 낮아짐", size=9.5, color=C["red"])
arrow(ax, 19.5, 3.95, 19.5, TOP - 0.35, color=C["red"], lw=1.0, ms=8)
text(ax, 2.0, 4.0, "좁은 배선:\n거의 괜찮음", size=8.8)
save(f, P, "dishing_erosion")

# 9. 더미 패턴
f, axs = panels(2, 2, 4.8, 4.6, (0, 10), (0, 10), titles=["더미 없이: 밀도 차이가 큼", "더미 추가: 밀도가 고르게"], size=10.5)
rng = np.random.default_rng(2)
for k, ax in enumerate(axs):
    rect(ax, 0, 0, 10, 10, "white", lw=1.0)
    for i in range(10):
        rect(ax, 0.6 + i * 0.45, 5.6, 0.25, 3.8, "cu", lw=0.3)
    rect(ax, 6.0, 6.0, 3.4, 3.2, "cu", lw=0.5)
    rect(ax, 0.8, 1.0, 0.4, 3.4, "cu", lw=0.3)
    rect(ax, 0.8, 1.0, 3.4, 0.4, "cu", lw=0.3)
    if k == 1:
        for x in np.arange(2.0, 9.6, 0.8):
            for y in np.arange(0.6, 5.0, 0.8):
                if x < 4.4 and y < 1.6:
                    continue
                rect(ax, x, y, 0.4, 0.4, "#c7a27c", lw=0.2)
        for y in np.arange(0.6, 5.0, 0.8):
            if y > 1.6:
                rect(ax, 1.4, y, 0.4, 0.4, "#c7a27c", lw=0.2)
        text(ax, 5.0, 5.15, "연한 사각형: 회로와 상관없는 더미 금속", size=8.8, box="white")
    else:
        text(ax, 5.4, 2.8, "텅 빈 영역 → 패드가 눌려 들어가서\n주변이 더 깎이거나 두께가 달라짐", size=8.8, box="white")
save(f, P, "dummy_fill")
