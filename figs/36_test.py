import numpy as np
from common import *

P = 36

# 1. ellipsometer
f, ax = canvas(9.0, 4.4, (0, 20), (-3.4, 7.0))
rect(ax, 2, -1.6, 16, 1.6, "si", lw=0.6)
rect(ax, 2, 0, 16, 0.9, "ox", lw=0.6)
text(ax, 15.5, 0.45, "측정할 막 (두께 d, 굴절률 n)", size=9)
text(ax, 15.5, -0.8, "기판", size=9)
line(ax, [3.5, 9.0], [6.0, 0.9], color=C["red"], lw=2.0)
line(ax, [9.0, 14.5], [0.9, 6.0], color=C["red"], lw=2.0)
line(ax, [9.0, 9.9], [0.9, 0.0], color=C["red"], lw=1.2, ls="--")
line(ax, [9.9, 10.8], [0.0, 0.9], color=C["red"], lw=1.2, ls="--")
line(ax, [10.8, 15.0], [0.9, 4.8], color=C["red"], lw=1.2, ls="--")
box(ax, 1.0, 5.8, 3.4, 1.0, "광원 + 편광기", fc="#fff8e1", size=9)
box(ax, 13.8, 5.8, 4.6, 1.0, "검광자 + 검출기", fc="#e3f2fd", size=9)
text(ax, 10.0, -2.5, "막 윗면, 아랫면에서 반사된 빛이 섞이면서 편광 상태(Ψ, Δ)가 바뀜 → model에 맞춰 d, n 계산", size=9)
save(f, P, "ellipsometry")

# 2. CD-SEM
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 4.6), sharex=True, gridspec_kw=dict(height_ratios=[1, 1]))
canvas(0, 0, (0, 10), (-0.3, 3.2), ax=ax1)
ax1.set_aspect("auto")
rect(ax1, 0, -0.3, 10, 0.3, "si", lw=0.5)
poly(ax1, [(3.6, 0), (6.4, 0), (6.2, 1.8), (3.8, 1.8)], "pr", lw=0.7)
for x in np.linspace(1.0, 9.0, 9):
    arrow(ax1, x, 3.1, x, 2.2, color=C["blue"], lw=0.9, ms=6)
text(ax1, 5.0, 2.65, "e-beam을 가로로 훑음", size=9, color=C["blue"], box="white")
x = np.linspace(0, 10, 800)
sig = 0.25 + 0.15 * ((x > 3.8) & (x < 6.2))
for e in (3.7, 6.3):
    sig += 1.0 * np.exp(-((x - e) / 0.12) ** 2)
ax2.plot(x, sig, color="#222222", lw=1.8)
ax2.axvline(3.7, color=C["red"], lw=1.0, ls="--")
ax2.axvline(6.3, color=C["red"], lw=1.0, ls="--")
ax2.annotate("", xy=(6.3, 1.15), xytext=(3.7, 1.15), arrowprops=dict(arrowstyle="<|-|>", color=C["red"]))
ax2.text(5.0, 1.2, "CD", ha="center", va="bottom", color=C["red"], fontsize=10, weight="bold")
ax2.set_ylim(0, 1.5)
ax2.set_yticks([])
ax2.set_xlabel("위치")
ax2.set_ylabel("2차 전자 신호")
ax2.text(8.2, 0.75, "모서리에서 신호가 튐\n→ 두 봉우리 사이 = 선폭", fontsize=9, ha="center")
plt.tight_layout()
save(f, P, "cdsem")

# 3. 결함 검사 (die끼리 비교)
f, axs = panels(4, 4, 2.8, 3.0, (0, 10), (0, 10), titles=["die A", "die B", "die C", "B와 A, C를 비교"], size=10)
for k, ax in enumerate(axs):
    rect(ax, 0, 0, 10, 10, "white", lw=1.0)
    if k < 3:
        for y in (1.5, 4.0, 6.5):
            rect(ax, 1.0, y, 8.0, 1.0, "#90a4ae", lw=0.4)
        for xx in (2.0, 5.0, 8.0):
            rect(ax, xx - 0.4, 2.5, 0.8, 1.5, "#90a4ae", lw=0.4)
        if k == 1:
            circ(ax, 6.3, 5.5, 0.45, C["red"], lw=0.5)
    else:
        circ(ax, 6.3, 5.5, 0.45, C["red"], lw=0.5)
        ax.add_patch(Circle((6.3, 5.5), 1.2, fc="none", ec=C["red"], lw=1.2, ls="--"))
        text(ax, 5.0, 8.4, "다른 곳만 남음\n→ 결함 위치", size=9, color=C["red"])
save(f, P, "defect_inspection")

# 4. SPC 관리도
rng = np.random.default_rng(11)
n = 32
mean, sd = 100.0, 1.0
x = mean + sd * rng.normal(size=n)
x[20:27] = mean + 0.9 + 0.5 * rng.random(7)
x[28] = mean + 3.6 * sd
f, ax = plot_ax(8.4, 3.8)
ax.plot(np.arange(1, n + 1), x, "o-", color=PAL[0], lw=1.2, ms=5)
for k, (y, s, c) in enumerate([(mean, "평균", "#333333"), (mean + 3 * sd, "UCL (+3σ)", C["red"]),
                                (mean - 3 * sd, "LCL (−3σ)", C["red"])]):
    ax.axhline(y, color=c, lw=1.2 if k else 1.0, ls="--" if k else "-")
    ax.text(n + 1.5, y + 0.15, s, va="bottom", fontsize=9, color=c)
ax.plot(29, x[28], "o", ms=12, mfc="none", mec=C["red"], mew=1.8)
ax.text(29, x[28] + 0.6, "관리 한계 벗어남", ha="center", fontsize=9, color=C["red"])
ax.axvspan(20.5, 27.5, color=C["orange"], alpha=0.15)
ax.text(23.5, 97.65, "7번 연속 평균 위\n→ 한쪽으로 치우침 (장비 변화 의심)", ha="center", fontsize=9, color=C["orange"])
ax.set_xlim(0, n + 6)
ax.set_ylim(95, 105.5)
ax.set_xlabel("lot 순서")
ax.set_ylabel("산화막 두께 (Å, 예시)")
ax.set_title("SPC 관리도: 한계를 넘거나 pattern이 보이면 원인 확인", loc="left", fontsize=11)
save(f, P, "spc_chart")

# 5. scribe line TEG
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.8), gridspec_kw=dict(width_ratios=[1, 1.25]))
canvas(0, 0, (-16, 16), (-16, 16), ax=ax1)
wafer_top(ax1, 0, 0, 15, c="#eceff1")
pitch = 3.0
for i in np.arange(-15, 15, pitch):
    for j in np.arange(-15, 15, pitch):
        if (i + pitch) ** 2 + (j + pitch) ** 2 < 14.5 ** 2 and i ** 2 + j ** 2 < 14.5 ** 2 and \
                (i + pitch) ** 2 + j ** 2 < 14.5 ** 2 and i ** 2 + (j + pitch) ** 2 < 14.5 ** 2:
            rect(ax1, i + 0.15, j + 0.15, pitch - 0.3, pitch - 0.3, "#b0bec5", lw=0.4)
rect(ax1, 0.0, 0.0, 6.0, 3.0, "none", ec=C["red"], lw=1.8, z=6)
ax1.set_title("wafer 위 die(chip)와 그 사이 scribe line", loc="left", fontsize=10.5)
canvas(0, 0, (0, 20), (0, 9), ax=ax2)
rect(ax2, 0, 0, 8.6, 9, "#b0bec5", lw=0.6)
rect(ax2, 11.4, 0, 8.6, 9, "#b0bec5", lw=0.6)
text(ax2, 4.3, 4.5, "die", size=11)
text(ax2, 15.7, 4.5, "die", size=11)
rect(ax2, 8.6, 0, 2.8, 9, "#fafafa", lw=0.4)
for y in np.arange(0.4, 8.6, 1.05):
    rect(ax2, 9.3, y, 0.7, 0.7, "#ffd54f", lw=0.5)
    rect(ax2, 10.2, y, 0.7, 0.7, "#ffd54f", lw=0.5)
tegs = [(7.6, "transistor (Vt, 전류)"), (5.6, "면저항 (25, 28편)"), (3.6, "contact / via chain (30편)"),
        (1.6, "capacitor (산화막 두께)")]
for y, s in tegs:
    text(ax2, 10.0, y + 0.55, "", size=8)
ax2.set_title("scribe line 확대: pad가 달린 test pattern (TEG)", loc="left", fontsize=10.5)
for k, (y, s) in enumerate(tegs):
    text(ax2, 21.0, y, s, size=9, ha="left")
    arrow(ax2, 20.9, y, 11.0, y, lw=0.7, ms=6, color="#555555")
ax2.set_xlim(0, 30)
plt.tight_layout()
save(f, P, "teg")

# 6. 수율 model
AD = np.linspace(0, 3, 300)
f, ax = plot_ax(7.2, 4.2)
ax.plot(AD, np.exp(-AD), color=PAL[1], lw=2.2, label="Poisson: e^(−AD)")
mur = np.where(AD > 0, ((1 - np.exp(-AD)) / np.where(AD > 0, AD, 1)) ** 2, 1.0)
ax.plot(AD, mur, color=PAL[0], lw=2.2, label="Murphy")
for a, ls in [(2.0, "--"), (0.5, ":")]:
    ax.plot(AD, (1 + AD / a) ** (-a), ls, color=PAL[2], lw=2.0, label=f"음이항 (뭉침 α = {a:g})")
ax.set_xlabel("die 면적 × 결함 밀도 (A·D)")
ax.set_ylabel("수율")
ax.set_ylim(0, 1.02)
ax.set_title("결함이 같아도 die가 크면 수율이 떨어짐", loc="left", fontsize=11)
ax.legend(fontsize=9)
save(f, P, "yield_models")

# 7. die 크기와 수율 (같은 결함 분포)
rng = np.random.default_rng(26)
R, EDGE = 150.0, 3.0
D0 = 0.1                                   # 개/cm²
nd = rng.poisson(D0 * np.pi * (R / 10) ** 2)
r = R * np.sqrt(rng.random(nd))
th = 2 * np.pi * rng.random(nd)
dx, dy = r * np.cos(th), r * np.sin(th)
f, axs = plt.subplots(1, 2, figsize=(11.0, 5.4))
res = []
for ax, size in zip(axs, (10.0, 20.0)):
    canvas(0, 0, (-160, 160), (-160, 160), ax=ax)
    wafer_top(ax, 0, 0, R, c="#f5f5f5")
    good = tot = 0
    for i in np.arange(-R, R, size):
        for j in np.arange(-R, R, size):
            corners = [(i, j), (i + size, j), (i, j + size), (i + size, j + size)]
            if all(cx ** 2 + cy ** 2 <= (R - EDGE) ** 2 for cx, cy in corners):
                tot += 1
                hit = np.any((dx >= i) & (dx < i + size) & (dy >= j) & (dy < j + size))
                good += not hit
                ax.add_patch(Rectangle((i + 0.6, j + 0.6), size - 1.2, size - 1.2,
                                       fc="#ef9a9a" if hit else "#a5d6a7", ec="#555555", lw=0.3, zorder=3))
    ax.plot(dx, dy, "k.", ms=4, zorder=5)
    A = (size / 10) ** 2
    res.append((size, tot, good, good / tot, np.exp(-A * D0)))
    ax.set_title(f"die {size:.0f} × {size:.0f} mm: 양품 {good} / {tot} = {good / tot * 100:.0f}% "
                 f"(Poisson {np.exp(-A * D0) * 100:.0f}%)", loc="left", fontsize=10.5)
plt.suptitle(f"같은 결함 {nd}개 (검은 점, 0.1개/cm²)가 떨어진 wafer, 초록 = 양품 die", fontsize=11, y=0.99)
plt.tight_layout()
save(f, P, "die_size_yield")
for row in res:
    print("die %dmm: total %d good %d yield %.3f poisson %.3f" % row)
print("defects:", nd)

# 8. wafer map pattern
rng = np.random.default_rng(9)
pats = ["무작위", "가운데", "가장자리 ring", "scratch", "한쪽 몰림"]
f, axs = plt.subplots(1, 5, figsize=(14.5, 3.3))
for ax, name in zip(axs, pats):
    canvas(0, 0, (-16, 16), (-16, 16), ax=ax)
    wafer_top(ax, 0, 0, 15, c="#f5f5f5")
    for i in range(-15, 15, 2):
        for j in range(-15, 15, 2):
            cx, cy = i + 1, j + 1
            if (abs(i) + 2) ** 2 + (abs(j) + 2) ** 2 > 15 ** 2 and max(abs(i), abs(j)) > 9:
                if (i + 1) ** 2 + (j + 1) ** 2 > 13.4 ** 2:
                    continue
            rr = np.hypot(cx, cy)
            if name == "무작위":
                bad = rng.random() < 0.12
            elif name == "가운데":
                bad = rr < 6 and rng.random() < 0.8
            elif name == "가장자리 ring":
                bad = rr > 10.5 and rng.random() < 0.8
            elif name == "scratch":
                bad = abs(cy - (0.55 * cx + 1.0)) < 1.2 and -11 < cx < 9
            else:
                bad = (cx + cy > 9) and rng.random() < 0.75
            ax.add_patch(Rectangle((i + 0.1, j + 0.1), 1.8, 1.8, fc="#ef5350" if bad else "#a5d6a7",
                                   ec="white", lw=0.4, zorder=3))
    ax.set_title(name, fontsize=10.5)
plt.tight_layout()
save(f, P, "wafer_map_patterns")

# 9. EDS 흐름
steps = [("ET", "scribe TEG로\n공정 이상 확인"), ("WBI", "고온, 고전압으로\n초기 불량 걸러냄"),
         ("Hot / Cold", "고온, 저온에서\nchip마다 기능 검사"), ("repair", "memory: 불량 cell을\n여분 cell로 교체"),
         ("최종 test", "repair 결과 확인,\n등급 분류"), ("map / inking", "양품 정보를 저장\n→ packaging으로")]
f, ax = canvas(14.4, 2.9, (0, 38.5), (-0.4, 5.6))
for i, (s, d) in enumerate(steps):
    x = 0.3 + i * 6.4
    box(ax, x, 2.6, 5.4, 2.5, s, fc="#e3f2fd" if i != 3 else "#fff3e0", size=10.5, weight="bold")
    text(ax, x + 2.7, 1.3, d, size=8.8, color="#444444")
    if i < len(steps) - 1:
        arrow(ax, x + 5.45, 3.85, x + 6.35, 3.85, lw=1.2, ms=9)
save(f, P, "eds_flow")

# 10. probe card
f, ax = canvas(9.6, 4.6, (0, 20), (-1.8, 9.6))
rect(ax, 2.0, -1.4, 16.0, 1.2, "#9e9e9e", lw=0.7)
text(ax, 10.0, -0.8, "chuck (온도 조절, x-y-z 이동)", size=9, color="white")
rect(ax, 3.0, -0.2, 14.0, 0.5, "si", lw=0.6)
for x in np.arange(5.0, 15.5, 1.5):
    rect(ax, x - 0.3, 0.3, 0.6, 0.2, "al", lw=0.4)
rect(ax, 3.5, 3.0, 13.0, 0.9, "#558b2f", lw=0.7)
text(ax, 10.0, 3.45, "probe card (PCB)", size=9, color="white")
for x in np.arange(5.0, 15.5, 1.5):
    line(ax, [x + 0.9, x + 0.25, x], [3.0, 1.2, 0.55], color="#424242", lw=1.4)
rect(ax, 5.0, 4.6, 10.0, 2.2, "#cfd8dc", lw=0.8)
text(ax, 10.0, 5.7, "tester head: 신호를 넣고 응답을 읽음", size=9.5)
line(ax, [10.0, 10.0], [3.9, 4.6], color="#555555", lw=2.0)
text(ax, 10.0, 8.4, "바늘을 chip pad에 대고 wafer 상태로 chip마다 전기 검사", size=10)
text(ax, 17.2, 0.05, "wafer", size=9, ha="left")
save(f, P, "probe_card")

# 11. shmoo plot
V = np.arange(0.60, 1.21, 0.05)
F = np.arange(0.5, 3.01, 0.1)
f, ax = plot_ax(7.0, 4.6)
ax.grid(False)
for v in V:
    for fr in F:
        fmax = 4.2 * (v - 0.42) ** 0.9
        ok = fr <= fmax and v <= 1.15
        ax.add_patch(Rectangle((v - 0.022, fr - 0.045), 0.044, 0.09, fc="#a5d6a7" if ok else "#ef9a9a",
                               ec="white", lw=0.4))
ax.plot(0.9, 2.0, "*", ms=16, color="#1a237e")
ax.text(0.915, 2.08, "목표 조건", fontsize=9.5, color="#1a237e")
ax.set_xlim(0.57, 1.23)
ax.set_ylim(0.45, 3.05)
ax.set_xlabel("전원 전압 (V)")
ax.set_ylabel("동작 주파수 (GHz)")
ax.set_title("shmoo plot: 초록 통과, 빨강 실패 (예시)", loc="left", fontsize=11)
save(f, P, "shmoo")
