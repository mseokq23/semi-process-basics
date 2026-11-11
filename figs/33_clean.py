import numpy as np
from common import *

P = 33

# 1. 오염 종류
f, ax = canvas(11.2, 3.9, (0, 26), (-2.2, 7.0))
rect(ax, 0, -2.2, 26, 2.2, "si", lw=0.6)
text(ax, 13.0, -1.3, "Si 웨이퍼", size=10)
# 파티클
circ(ax, 3.0, 1.05, 1.05, "#9e9e9e", lw=0.8)
text(ax, 3.0, 3.1, "파티클", size=10.5, weight="bold")
text(ax, 3.0, 4.6, "패턴 단락, 끊김\n막 속에 박힘", size=8.8, color="#444444")
# 유기물
xs = np.linspace(7.0, 11.5, 100)
ax.fill_between(xs, 0, 0.35 + 0.15 * np.sin(xs * 4), color="#c8a165", ec="#333333", lw=0.6, zorder=3)
text(ax, 9.25, 3.1, "유기물", size=10.5, weight="bold")
text(ax, 9.25, 4.6, "PR 찌꺼기, 손자국, 공기 중 탄화수소\n→ 막이 잘 안 붙음", size=8.8, color="#444444")
# 금속
for x, s in [(13.6, "Fe"), (14.8, "Cu"), (16.0, "Na⁺"), (17.2, "Ni")]:
    circ(ax, x, 0.3, 0.3, "#ffcc80", lw=0.6)
    text(ax, x, 0.3, s, size=7.5, weight="bold")
text(ax, 15.4, 3.1, "금속 오염", size=10.5, weight="bold")
text(ax, 15.4, 4.6, "산화막 신뢰성 저하, 누설 전류,\nNa⁺는 산화막 속을 움직여 Vt 변화", size=8.8, color="#444444")
# 자연 산화막
rect(ax, 19.5, 0, 6.0, 0.28, "ox", lw=0.6)
text(ax, 22.5, 3.1, "자연 산화막", size=10.5, weight="bold")
text(ax, 22.5, 4.6, "공기, 물에 닿으면 생기는 얇은 SiO₂\n→ 접촉 저항, 에피 불량", size=8.8, color="#444444")
for x in (3.0, 9.25, 15.4, 22.5):
    arrow(ax, x, 2.75, x, 1.4 if x == 3.0 else 0.8, color="#777777", lw=0.9, ms=7)
save(f, P, "contaminants")

# 2. RCA 세정 순서
steps = [("SPM", "H₂SO₄ + H₂O₂\n120 °C 근처", "유기물, PR 찌꺼기", "#fde2e2"),
         ("DHF", "묽은 HF\n상온", "자연 산화막\n(+ 그 안의 금속)", "#e3f2fd"),
         ("SC-1 (APM)", "NH₄OH + H₂O₂ + H₂O\n60 ~ 80 °C", "파티클, 유기물", "#e8f5e9"),
         ("SC-2 (HPM)", "HCl + H₂O₂ + H₂O\n60 ~ 80 °C", "금속", "#fff3e0"),
         ("린스 + 건조", "초순수(DIW)\n스핀, IPA", "약액 제거,\n얼룩 없이 말리기", "#ede7f6")]
f, ax = canvas(13.2, 3.6, (0, 31), (-0.6, 7.6))
for i, (name, chem, target, c) in enumerate(steps):
    x = 0.4 + i * 6.2
    box(ax, x, 3.4, 5.0, 3.6, "", fc=c, size=9)
    text(ax, x + 2.5, 6.35, name, size=10.5, weight="bold")
    text(ax, x + 2.5, 5.0, chem, size=8.8)
    text(ax, x + 2.5, 1.9, target, size=9.2, color=C["red"], weight="bold")
    arrow(ax, x + 2.5, 3.3, x + 2.5, 2.6, color="#777777", lw=0.9, ms=7)
    if i < len(steps) - 1:
        arrow(ax, x + 5.05, 5.2, x + 6.15, 5.2, lw=1.2, ms=9)
        text(ax, x + 5.6, 4.45, "린스", size=8, color="#555555")
text(ax, 15.5, 0.2, "빨간 글씨: 주로 없애는 것. 순서와 조합은 공정마다 다름", size=9, color="#555555")
save(f, P, "rca_flow")

# 3. SC-1 파티클 제거
tt = ["① 파티클이 표면에 붙어 있음", "② H₂O₂: 표면을 얇게 산화", "③ NH₄OH: 산화막을 조금 녹여 밑을 파냄",
      "④ 둘 다 − 전하 → 서로 밀어서 다시 안 붙음"]
f, axs = panels(4, 4, 3.3, 3.0, (0, 10), (-1.6, 6.0), titles=tt, size=9.6)
for k, ax in enumerate(axs):
    rect(ax, 0, -1.6, 10, 1.6, "si", lw=0.5)
    ox_t = 0.0 if k == 0 else 0.3
    if k >= 1:
        if k == 1:
            rect(ax, 0, 0, 10, ox_t, "ox", lw=0.5)
        else:
            xs = np.linspace(0, 10, 300)
            top = np.where(np.abs(xs - 5.0) < 1.1,
                           ox_t - 0.22 * np.clip(1 - np.abs(xs - 5.0) / 1.1, 0, 1) ** 0.5, ox_t - 0.1)
            ax.fill_between(xs, 0, top, color=C["ox"], ec="#333333", lw=0.5, zorder=2)
    py = 1.15 + (0.0 if k < 2 else (0.25 if k == 2 else 2.6))
    circ(ax, 5.0 if k < 3 else 6.8, py + ox_t * (k == 1), 0.95, "#9e9e9e", lw=0.8, z=4)
    if k == 1:
        for x in np.arange(0.8, 10, 1.6):
            text(ax, x, 1.9 if abs(x - 5.0) > 1.5 else 2.9, "H₂O₂", size=7.5, color=C["blue"])
    if k == 2:
        for x in (1.5, 3.2, 7.0, 8.6):
            text(ax, x, 1.2, "OH⁻", size=8, color=C["green"], weight="bold")
            arrow(ax, x, 0.95, x, 0.45, color=C["green"], lw=0.8, ms=6)
    if k == 3:
        for x in np.arange(0.6, 10, 0.9):
            text(ax, x, 0.55, "−", size=11, color=C["red"], weight="bold")
        for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
            text(ax, 6.8 + 1.2 * np.cos(a), py + 1.2 * np.sin(a), "−", size=10, color=C["red"], weight="bold")
        arrow(ax, 4.4, 2.2, 5.6, 3.3, color="#555555", lw=1.2, ms=9)
save(f, P, "sc1_liftoff")

# 4. 제타 전위 (개념)
pH = np.linspace(1, 13, 300)
f, ax = plot_ax(7.0, 4.0)
for name, iep, c in [("SiO₂", 2.5, PAL[0]), ("Si₃N₄", 6.0, PAL[2]), ("Al₂O₃", 9.0, PAL[3])]:
    ax.plot(pH, -60 * np.tanh((pH - iep) / 2.2), color=c, lw=2.2, label=f"{name} (0이 되는 pH ≈ {iep:g})")
ax.axhline(0, color="#555555", lw=0.9)
ax.axvspan(9.5, 11, color=C["green"], alpha=0.12)
ax.text(10.25, 52, "SC-1\n(pH 10 근처)", ha="center", fontsize=9)
ax.set_xlabel("pH")
ax.set_ylabel("표면 전위 (mV, 개념)")
ax.set_title("pH가 높으면 Si 표면과 대부분의 파티클이 둘 다 − 전하 (개념 그래프)", loc="left", fontsize=10.5)
ax.legend(fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3)
save(f, P, "zeta")

# 5. 배치 vs 매엽
f, axs = panels(2, 2, 6.2, 3.8, (0, 16), (-0.6, 9.4), titles=["배치식 (웨트 벤치): 여러 장을 조에 담금",
                                                           "매엽식: 한 장씩 돌리면서 뿌림"], size=10.5)
ax = axs[0]
for i, (s, c) in enumerate([("SPM", "#fde2e2"), ("린스", "#e3f2fd"), ("SC-1", "#e8f5e9"), ("린스", "#e3f2fd"),
                            ("SC-2", "#fff3e0"), ("건조", "#ede7f6")]):
    x = 0.3 + i * 2.6
    rect(ax, x, 0.0, 2.3, 3.6, c, lw=0.8)
    text(ax, x + 1.15, -0.35, s, size=8.8)
for j in range(7):
    rect(ax, 3.0 + j * 0.16, 0.6, 0.06, 2.6, "si", lw=0.3, z=4)
rect(ax, 2.85, 0.4, 1.4, 0.2, "#9e9e9e", lw=0.4, z=4)
arrow(ax, 4.4, 4.6, 6.6, 4.6, lw=1.2, ms=9)
text(ax, 5.6, 5.2, "카세트째로 옮김", size=9)
text(ax, 8.0, 7.6, "한 번에 25 ~ 50장 → 처리량 많고 약액 덜 씀\n앞 웨이퍼 오염이 약액에 남을 수 있음", size=8.8)
ax = axs[1]
rect(ax, 2.0, 1.0, 12.0, 0.4, "si", lw=0.7, z=4)
rect(ax, 7.6, -0.4, 0.8, 1.4, "#9e9e9e", lw=0.6)
text(ax, 8.0, 0.1, "", size=8)
ax.add_patch(FancyArrowPatch((5.5, 0.4), (10.5, 0.4), connectionstyle="arc3,rad=0.25", arrowstyle="-|>",
                             mutation_scale=12, color="#555555", lw=1.2))
text(ax, 8.0, -0.25, "", size=8)
rect(ax, 4.6, 4.2, 0.6, 2.4, "#78909c", lw=0.6)
poly(ax, [(4.6, 4.2), (5.2, 4.2), (5.5, 3.6), (4.3, 3.6)], "#78909c", lw=0.6)
for dx in np.linspace(-0.9, 0.9, 7):
    line(ax, [4.9, 4.9 + dx * 2.2], [3.5, 1.5], color=C["blue"], lw=0.8)
text(ax, 4.9, 7.1, "약액 / 초순수 노즐", size=9)
rect(ax, 10.2, 3.2, 1.6, 1.0, "#b39ddb", lw=0.6)
for yy in (2.9, 2.5, 2.1):
    ax.add_patch(Arc((11.0, yy), 1.4, 0.3, theta1=200, theta2=340, color="#7e57c2", lw=1.0))
text(ax, 11.0, 4.8, "메가소닉 (MHz 진동)", size=9)
text(ax, 8.0, 8.4, "웨이퍼마다 새 약액 → 오염 옮김 적음, 균일\n장당 시간이 걸려서 챔버를 여러 개 붙임", size=8.8)
save(f, P, "batch_vs_single")

# 6. 패턴 쓰러짐
f, axs = plt.subplots(1, 3, figsize=(13.0, 3.8), gridspec_kw=dict(width_ratios=[1, 1, 1.1]))
for k, ax in enumerate(axs[:2]):
    canvas(0, 0, (0, 10), (-0.6, 7.2), ax=ax)
    rect(ax, 0, -0.6, 10, 0.6, "si", lw=0.5)
    xs_ = [1.2, 3.4, 5.6, 7.8]
    if k == 0:
        ax.set_title("건조 중: 줄 사이에 남은 물이 양쪽을 당김", loc="left", fontsize=10.5)
        for x in xs_:
            rect(ax, x, 0, 0.9, 5.0, "ox", lw=0.7)
        for a, b in [(2.1, 3.4), (6.5, 7.8)]:
            xx = np.linspace(a, b, 60)
            meniscus = 3.0 - 0.6 * np.sqrt(np.clip(1 - ((xx - (a + b) / 2) / ((b - a) / 2)) ** 2, 0, 1))
            ax.fill_between(xx, 0, meniscus, color="#90caf9", zorder=1.5)
            arrow(ax, a + 0.15, 2.0, a + 0.75, 2.0, color=C["red"], lw=1.2, ms=8, style="<|-")
            arrow(ax, b - 0.75, 2.0, b - 0.15, 2.0, color=C["red"], lw=1.2, ms=8)
        text(ax, 5.0, 6.3, "모세관 힘", size=9.5, color=C["red"])
    else:
        ax.set_title("결과: 높고 가는 패턴끼리 붙어서 쓰러짐", loc="left", fontsize=10.5)
        for x, lean in [(1.2, 0.7), (3.4, -0.7), (5.6, 0.7), (7.8, -0.7)]:
            poly(ax, [(x, 0), (x + 0.9, 0), (x + 0.9 + lean, 5.0), (x + lean, 5.0)], "ox", lw=0.7)
ax = axs[2]
names = ["물", "IPA", "초임계 CO₂"]
gam = [72, 22, 0.5]
ax.bar(names, gam, color=[C["blue"], PAL[3], PAL[2]], edgecolor="#333333", lw=0.6)
for i, g in enumerate([72, 22, 0]):
    ax.text(i, gam[i] + 2, f"{g}", ha="center", fontsize=10)
ax.set_ylabel("표면장력 (mN/m, 상온)")
ax.set_ylim(0, 85)
ax.set_title("표면장력이 작은 액체로 바꿔서 말리기", loc="left", fontsize=10.5)
ax.grid(alpha=0.25, axis="y")
plt.tight_layout()
save(f, P, "pattern_collapse")

# 7. 워터마크
tt = ["① HF 후 표면은 물을 튕김 (소수성)", "② 물방울 속 O₂ + Si → 실리카가 녹아듦", "③ 마르면 얼룩만 남음 (워터마크)"]
f, axs = panels(3, 3, 3.6, 2.6, (0, 10), (-1.2, 4.6), titles=tt, size=9.8)
for k, ax in enumerate(axs):
    rect(ax, 0, -1.2, 10, 1.2, "si", lw=0.5)
    if k < 2:
        d_, R_ = 0.35, 1.9
        t0 = np.arcsin(d_ / R_)
        tt_ = np.linspace(t0, np.pi - t0, 80)
        poly(ax, list(zip(5.0 + R_ * np.cos(tt_), -d_ + R_ * np.sin(tt_))), "#90caf9", lw=0.6, z=3)
    if k == 0:
        text(ax, 5.0, 2.7, "H로 덮인 Si 표면", size=8.8)
    if k == 1:
        for (x, y) in [(4.2, 0.4), (5.0, 0.7), (5.8, 0.35)]:
            text(ax, x, y, "O₂", size=7.5, color=C["blue"], weight="bold", z=25)
        text(ax, 5.0, 2.7, "산화 → 녹아서 물방울 속으로", size=8.8)
    if k == 2:
        xs = np.linspace(3.6, 6.4, 60)
        ax.fill_between(xs, 0, 0.12 + 0.08 * np.sin((xs - 3.6) * 7), color="#bdbdbd", ec="#333333", lw=0.5, zorder=3)
        text(ax, 5.0, 1.4, "실리카 얼룩", size=9, color=C["red"], weight="bold")
save(f, P, "watermark")
