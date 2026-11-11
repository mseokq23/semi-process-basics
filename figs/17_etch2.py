import numpy as np
from common import *

P = 17


def stack(ax, prof="aniso"):
    rect(ax, 0.3, 0.3, 9.4, 1.4, "si", lw=0.6)
    if prof == "aniso":
        rect(ax, 0.3, 1.7, 3.3, 2.0, "ox", lw=0.6)
        rect(ax, 6.4, 1.7, 3.3, 2.0, "ox", lw=0.6)
    elif prof == "iso":
        th = np.linspace(np.pi / 2, 0, 40)
        poly(ax, [(0.3, 1.7), (3.6, 1.7)] + [(3.6 - 2 * np.cos(t), 3.7 - 2 * np.sin(t)) for t in th] + [(0.3, 3.7)], "ox", lw=0.6)
        poly(ax, [(9.7, 1.7), (6.4, 1.7)] + [(6.4 + 2 * np.cos(t), 3.7 - 2 * np.sin(t)) for t in th] + [(9.7, 3.7)], "ox", lw=0.6)
    elif prof == "sputter":
        poly(ax, [(0.3, 1.7), (3.6, 1.7), (3.6, 3.3), (3.3, 3.7), (0.3, 3.7)], "ox", lw=0.6)
        poly(ax, [(9.7, 1.7), (6.4, 1.7), (6.4, 3.3), (6.7, 3.7), (9.7, 3.7)], "ox", lw=0.6)
        rect(ax, 3.6, 1.7, 0.18, 1.4, "#9e9e9e", lw=0.3, z=4)
        rect(ax, 6.22, 1.7, 0.18, 1.4, "#9e9e9e", lw=0.3, z=4)
    th = 0.5 if prof == "sputter" else 0.8
    poly(ax, [(0.3, 3.7), (3.6 if prof != "sputter" else 3.3, 3.7), (3.6 if prof != "sputter" else 3.0, 3.7 + th), (0.3, 3.7 + th)], "pr", lw=0.6)
    poly(ax, [(9.7, 3.7), (6.4 if prof != "sputter" else 6.7, 3.7), (6.4 if prof != "sputter" else 7.0, 3.7 + th), (9.7, 3.7 + th)], "pr", lw=0.6)


# 1. 건식 식각 3종류
tt = ["물리적 (스퍼터 식각, 이온 밀링)", "화학적 (라디칼 = 플라즈마 식각)", "RIE (이온 + 라디칼)"]
f, axs = panels(3, 3, 3.9, 3.6, (0, 10), (0, 7.4), titles=tt, size=10.5)
stack(axs[0], "sputter")
stack(axs[1], "iso")
stack(axs[2], "aniso")
for x in (4.3, 5.0, 5.7):
    arrow(axs[0], x, 7.0, x, 2.0, color="red", lw=1.3, ms=8)
    arrow(axs[2], x, 7.0, x, 2.0, color="red", lw=1.3, ms=8)
rng = np.random.default_rng(2)
for ax in (axs[1], axs[2]):
    for _ in range(9):
        x, y = rng.uniform(1.0, 9.0), rng.uniform(5.2, 7.0)
        circ(ax, x, y, 0.16, "#81c784", lw=0.4)
text(axs[0], 5.0, -0.25, "Ar⁺로 때려서 떼어냄: 수직이지만\n선택비 낮고, 떨어진 게 옆에 다시 붙음", size=9, va="top")
text(axs[1], 5.0, -0.25, "라디칼이 화학 반응: 선택비 높지만\n등방성 (언더컷)", size=9, va="top")
text(axs[2], 5.0, -0.25, "라디칼이 반응 + 이온이 바닥만 도와줌\n→ 수직 + 적당한 선택비", size=9, va="top")
f.subplots_adjust(bottom=0.2)
save(f, P, "dry_types")

# 2. 이온-라디칼 시너지 (개념 그래프)
t = np.linspace(0, 900, 901)
er = np.where(t < 200, 0.5, np.where(t < 650, 5.8, 0.2))
f, ax = plot_ax(7.4, 4.0)
ax.plot(t, er, color="#222222", lw=2.4)
for x0, x1, s, c in [(0, 200, "XeF₂ 기체만", "#e8f5e9"), (200, 650, "XeF₂ + Ar⁺ 이온", "#fff3e0"),
                     (650, 900, "Ar⁺ 이온만", "#e3f2fd")]:
    ax.axvspan(x0, x1, color=c, zorder=0)
    ax.text((x0 + x1) / 2, 6.4, s, ha="center", fontsize=10)
ax.set_ylim(0, 7.2)
ax.set_xlabel("시간 (s)")
ax.set_ylabel("Si 식각률 (nm/min)")
ax.set_title("따로 하면 거의 안 깎이는데, 같이 하면 10배 이상 (1979년 실험을 대략 다시 그림)", loc="left", fontsize=10.5)
save(f, P, "synergy")

# 3. 측벽 보호막
f, ax = canvas(7.6, 5.6, (0, 12), (0, 9))
rect(ax, 0.5, 0.5, 11, 1.6, "si", lw=0.6)
rect(ax, 0.5, 2.1, 3.5, 4.4, "ox", lw=0.6)
rect(ax, 8.0, 2.1, 3.5, 4.4, "ox", lw=0.6)
rect(ax, 4.0, 2.1, 4.0, 1.2, "ox", lw=0.6)
rect(ax, 0.5, 6.5, 3.5, 1.0, "pr", lw=0.6)
rect(ax, 8.0, 6.5, 3.5, 1.0, "pr", lw=0.6)
rect(ax, 4.0, 3.3, 0.18, 3.2, "#6d4c41", lw=0, z=4)
rect(ax, 7.82, 3.3, 0.18, 3.2, "#6d4c41", lw=0, z=4)
for x in (5.0, 6.0, 7.0):
    arrow(ax, x, 8.7, x, 3.45, color="red", lw=1.3, ms=8)
for (x, y) in [(5.4, 6.0), (6.6, 5.2), (4.8, 4.4), (6.2, 7.6)]:
    circ(ax, x, y, 0.16, "#81c784", lw=0.4)
text(ax, 2.2, 4.3, "측벽: 폴리머가 쌓여서\n라디칼을 막음", size=9.5, box="white")
arrow(ax, 3.4, 4.3, 4.1, 4.6, lw=0.8, ms=7)
text(ax, 9.9, 4.3, "바닥: 이온이 폴리머를\n떼어내서 계속 깎임", size=9.5, box="white")
arrow(ax, 8.6, 3.6, 7.0, 3.35, lw=0.8, ms=7)
text(ax, 6.0, 0.05, "이온은 수직으로만 오니까 바닥만 깎이고 옆은 보호됨 → 이방성", size=9.5, va="bottom")
save(f, P, "sidewall")

# 4. 식각 반응 단계
f, ax = canvas(10, 4.6, (0, 20), (0, 9.2))
rect(ax, 0.5, 0.5, 19, 2.0, "si", lw=0.6)
ax.add_patch(Ellipse((10, 7.3), 18, 2.6, fc="#f3e5f5", ec="#9575cd", lw=1.0))
text(ax, 10, 8.1, "플라즈마", size=10, color=C["purple"])
steps = [(2.5, "① 반응종 생성\nCF₄ → CF₃ + F"), (6.5, "② 표면으로 이동,\n흡착"), (10.5, "③ 반응\n(이온이 도와줌)"),
         (14.5, "④ 휘발성 생성물\n탈착 (SiF₄)"), (18.0, "⑤ 펌프로 배기")]
for x, s in steps:
    text(ax, x, 4.4, s, size=9.3, box="white", z=20)
arrow(ax, 6.5, 6.2, 6.5, 2.8, color="green", lw=1.4)
arrow(ax, 10.5, 6.2, 10.5, 2.8, color="red", lw=1.4)
arrow(ax, 14.5, 2.8, 14.5, 6.0, color="blue", lw=1.4)
arrow(ax, 16.2, 6.4, 19.6, 6.4, color="#555555", lw=1.4)
for x in (6.3, 6.7):
    circ(ax, x, 2.65, 0.14, "#81c784", lw=0.3)
circ(ax, 14.5, 3.1, 0.22, "#90caf9", lw=0.3)
save(f, P, "etch_steps")

# 5. 생성물이 잘 날아가는지
items = [("CO (PR + O₂)", -191), ("SiF₄ (Si + F)", -90), ("WF₆ (W + F)", 17), ("SiCl₄ (Si + Cl)", 58),
         ("TiCl₄ (Ti + Cl)", 136), ("AlCl₃ (Al + Cl)", 180), ("CuCl (Cu + Cl)", 1490)]
f, ax = plot_ax(8.0, 4.0)
ys = np.arange(len(items))[::-1]
cols = [PAL[0] if v < 200 else PAL[1] for _, v in items]
ax.barh(ys, [v + 200 for _, v in items], left=-200, color=cols, height=0.55)
ax.set_yticks(ys)
ax.set_yticklabels([s for s, _ in items])
ax.axvspan(20, 150, color="#c8e6c9", alpha=0.6, zorder=0)
ax.text(85, -0.75, "식각할 때 웨이퍼 온도 근처", ha="center", fontsize=9)
ax.set_ylim(-1.1, 6.5)
for y, (_, v) in zip(ys, items):
    ax.text(max(v, -200) + 20, y, f"{v} °C", va="center", fontsize=9)
ax.set_xlim(-220, 1700)
ax.set_xlabel("끓는점 / 승화점 (°C, 대략)")
ax.set_title("생성물이 기체로 잘 날아가야 식각됨 → Cu는 할로겐 생성물이 안 날아감", loc="left", fontsize=11)
save(f, P, "volatility")
