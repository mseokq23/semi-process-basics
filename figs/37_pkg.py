import numpy as np
from common import *

P = 37

# 1. 패키징 순서
steps = [("백 그라인딩", "웨이퍼 뒷면을\n갈아서 얇게"), ("다이싱", "칩 단위로\n자르기"), ("다이 어태치", "기판에 칩\n붙이기"),
         ("본딩", "칩과 기판을\n전기로 연결"), ("몰딩", "수지로 덮어\n보호"), ("마킹, 볼 부착", "이름 새기고\n솔더볼 달기"),
         ("최종 테스트", "패키지 상태로\n다시 검사")]
f, ax = canvas(14.6, 2.9, (0, 44.5), (-0.6, 5.6))
for i, (s, d) in enumerate(steps):
    x = 0.3 + i * 6.3
    box(ax, x, 2.6, 5.3, 2.4, s, fc="#e8f5e9" if i < 4 else "#e3f2fd", size=10.2, weight="bold")
    text(ax, x + 2.65, 1.3, d, size=8.8, color="#444444")
    if i < len(steps) - 1:
        arrow(ax, x + 5.35, 3.8, x + 6.25, 3.8, lw=1.2, ms=9)
save(f, P, "pkg_flow")

# 2. 백 그라인딩
f, axs = panels(2, 2, 5.4, 3.0, (0, 12), (-0.8, 6.0), titles=["앞면에 보호 테이프 붙이고 뒤집어서 연마",
                                                           "두께 비교 (대략)"], size=10.5)
ax = axs[0]
rect(ax, 1.0, 0.3, 10.0, 0.5, "#fff59d", lw=0.6)
text(ax, 6.0, 0.05, "보호 테이프 (회로 면)", size=8.6, va="top")
rect(ax, 1.0, 0.8, 10.0, 1.6, "si", lw=0.7)
rect(ax, 1.0, 2.4, 10.0, 0.6, "si", lw=0.7, hatch="////", alpha=0.6)
text(ax, 6.0, 2.7, "갈아낼 부분", size=8.6)
rect(ax, 3.5, 3.4, 5.0, 0.6, "#78909c", lw=0.7)
rect(ax, 5.6, 4.0, 0.8, 1.6, "#9e9e9e", lw=0.6)
text(ax, 9.9, 4.6, "연마 휠 (회전)", size=9)
ax = axs[1]
for i, (s, t) in enumerate([("원래 300 mm 웨이퍼", 775), ("일반 패키지", 150), ("적층 메모리", 40)]):
    y = 4.4 - i * 1.7
    w = t / 775 * 7.0
    rect(ax, 4.6, y - 0.35, w, 0.7, "si", lw=0.6)
    text(ax, 4.4, y, s, size=9, ha="right")
    text(ax, 4.6 + w + 0.2, y, f"{t} µm", size=9, ha="left")
save(f, P, "back_grinding")

# 3. 다이싱
tt = ["블레이드: 회전 톱날로 자름", "스텔스 레이저: 안쪽만 개질 → 테이프를 늘려 쪼갬", "플라즈마: 스크라이브 라인을 식각"]
f, axs = panels(3, 3, 4.2, 3.2, (0, 10), (-1.0, 6.4), titles=tt, size=10)
for k, ax in enumerate(axs):
    rect(ax, 0, -1.0, 10, 0.5, "#fff59d", lw=0.5)
    if k == 0:
        rect(ax, 0.5, -0.5, 4.0, 1.4, "si", lw=0.7)
        rect(ax, 5.5, -0.5, 4.0, 1.4, "si", lw=0.7)
        ax.add_patch(Circle((5.0, 3.0), 2.0, fc="#cfd8dc", ec="#333333", lw=0.8, zorder=3))
        rect(ax, 4.75, 0.9, 0.5, 0.2, "#cfd8dc", lw=0.0, z=2)
        text(ax, 5.0, 3.0, "블레이드", size=9)
        for (x, y) in [(4.4, 0.85), (5.6, 0.82)]:
            poly(ax, [(x - 0.12, y), (x + 0.12, y), (x, y - 0.25)], "white", lw=0.4, z=4)
        text(ax, 8.3, 5.7, "가장자리 깨짐(치핑),\n자르는 폭이 넓음", size=8.6, color=C["red"])
    elif k == 1:
        rect(ax, 0.5, -0.5, 9.0, 1.4, "si", lw=0.7)
        for x in (5.0,):
            for y in np.linspace(-0.2, 0.6, 5):
                circ(ax, x, y, 0.1, "#5d4037", lw=0.0, z=4)
        poly(ax, [(4.6, 5.2), (5.4, 5.2), (5.05, 0.25), (4.95, 0.25)], "#ef9a9a", lw=0.0, z=2.5, alpha=0.7)
        text(ax, 5.0, 5.6, "레이저 (Si를 투과하는 파장)", size=8.6, color=C["red"])
        arrow(ax, 2.0, -0.8, 0.5, -0.8, lw=1.0, ms=7)
        arrow(ax, 8.0, -0.8, 9.5, -0.8, lw=1.0, ms=7)
        text(ax, 2.3, 3.4, "표면 손상,\n칩 손실 거의 없음", size=8.6, color=C["green"])
    else:
        for (a, b) in [(0.5, 4.75), (5.25, 9.5)]:
            rect(ax, a, -0.5, b - a, 1.4, "si", lw=0.7)
            rect(ax, a, 0.9, b - a, 0.5, "pr", lw=0.5)
        for x in np.linspace(4.85, 5.15, 3):
            arrow(ax, x, 4.0, x, 1.1, color="#555555", lw=0.8, ms=6)
        text(ax, 5.0, 4.6, "보쉬 식각 (19편)", size=8.6)
        text(ax, 2.4, 3.0, "얇은 웨이퍼, 좁은 라인,\n칩 모양 자유", size=8.6, color=C["green"])
save(f, P, "dicing")

# 4. 와이어 본딩 vs 플립칩
f, axs = panels(2, 2, 5.8, 3.6, (0, 14), (-1.6, 7.0), titles=["와이어 본딩: 칩 위를 보고 붙이고 금속선으로 연결",
                                                           "플립칩: 칩을 뒤집어 범프로 바로 연결"], size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 1.0, 0.0, 12.0, 1.0, "#558b2f", lw=0.7)
    text(ax, 7.0, 0.5, "패키지 기판", size=9, color="white")
    for x in np.arange(1.8, 12.6, 1.3):
        circ(ax, x, -0.45, 0.42, "#bdbdbd", lw=0.6)
    if k == 0:
        rect(ax, 4.0, 1.0, 6.0, 0.25, "#e0e0e0", lw=0.5)
        rect(ax, 4.0, 1.25, 6.0, 1.3, "si", lw=0.7)
        text(ax, 7.0, 1.9, "칩 (회로 면 위)", size=9)
        for side in (-1, 1):
            x0 = 7.0 + side * 2.8
            x1 = 7.0 + side * 5.0
            xs = np.linspace(x0, x1, 40)
            ys = 2.55 + 1.6 * np.sin(np.linspace(0, np.pi, 40)) * np.linspace(1, 0.5, 40) - np.linspace(0, 1.55, 40)
            ax.plot(xs, ys, color="#c9a227", lw=1.6, zorder=6)
        poly(ax, [(1.6, 1.0), (12.4, 1.0), (12.4, 4.8), (1.6, 4.8)], "#616161", lw=0.6, z=1.5, alpha=0.35)
        text(ax, 7.0, 4.3, "몰딩 수지 (EMC)", size=9)
        text(ax, 11.6, 5.4, "금 / 구리 선", size=8.6, color="#8d6e00")
    else:
        rect(ax, 3.0, 2.0, 8.0, 1.3, "si", lw=0.7)
        text(ax, 7.0, 2.65, "칩 (회로 면 아래)", size=9)
        rect(ax, 3.0, 1.0, 8.0, 1.0, "#ffe082", lw=0.0, z=1.8, alpha=0.6)
        for x in np.arange(3.6, 10.6, 0.9):
            circ(ax, x, 1.5, 0.35, "#9e9e9e", lw=0.5, z=3)
        text(ax, 12.2, 2.0, "범프 +\n언더필", size=8.6)
        text(ax, 7.0, 4.6, "선이 짧아 빠르고, 칩 전체 면적에\n입출력을 배치 가능", size=9, color=C["green"])
    text(ax, 7.0, -1.25, "솔더볼 → 메인보드", size=8.6)
save(f, P, "wire_vs_flip")

# 5. 패키지 변화
f, ax = canvas(14.6, 3.4, (0, 44), (-1.6, 7.4))
items = ["DIP", "QFP", "BGA", "WLP", "2.5D", "3D 적층"]
for i, s in enumerate(items):
    cx = 3.5 + i * 7.3
    if s == "DIP":
        rect(ax, cx - 2.0, 2.0, 4.0, 1.4, "emc", lw=0.6)
        for x in np.linspace(cx - 1.6, cx + 1.6, 5):
            line(ax, [x, x], [2.0, 0.4], color="#9e9e9e", lw=2.0)
    elif s == "QFP":
        rect(ax, cx - 1.8, 1.5, 3.6, 1.0, "emc", lw=0.6)
        for side in (-1, 1):
            line(ax, [cx + side * 1.8, cx + side * 2.3, cx + side * 2.4, cx + side * 2.9], [2.0, 2.0, 1.0, 1.0],
                 color="#9e9e9e", lw=1.6)
    elif s == "BGA":
        rect(ax, cx - 2.4, 1.2, 4.8, 0.4, "#558b2f", lw=0.6)
        rect(ax, cx - 1.6, 1.6, 3.2, 1.0, "emc", lw=0.6)
        for x in np.linspace(cx - 2.0, cx + 2.0, 7):
            circ(ax, x, 0.95, 0.25, "#bdbdbd", lw=0.4)
    elif s == "WLP":
        rect(ax, cx - 1.5, 1.4, 3.0, 0.9, "si", lw=0.6)
        for x in np.linspace(cx - 1.2, cx + 1.2, 5):
            circ(ax, x, 1.15, 0.25, "#bdbdbd", lw=0.4)
    elif s == "2.5D":
        rect(ax, cx - 2.8, 0.7, 5.6, 0.4, "#558b2f", lw=0.6)
        rect(ax, cx - 2.5, 1.2, 5.0, 0.35, "#b0bec5", lw=0.6)
        rect(ax, cx - 2.3, 1.6, 2.2, 1.0, "si", lw=0.6)
        for j in range(4):
            rect(ax, cx + 0.4, 1.6 + j * 0.42, 1.8, 0.38, "#90caf9", lw=0.4)
    else:
        rect(ax, cx - 2.2, 0.7, 4.4, 0.4, "#558b2f", lw=0.6)
        for j in range(5):
            rect(ax, cx - 1.6, 1.2 + j * 0.45, 3.2, 0.4, "si" if j == 0 else "#90caf9", lw=0.4)
        for x in (cx - 0.8, cx, cx + 0.8):
            line(ax, [x, x], [1.2, 3.4], color=C["cu"], lw=1.4)
    text(ax, cx, 4.3, s, size=10.5, weight="bold")
desc = ["핀을 기판 구멍에 꽂음", "네 변에 다리", "아래 면 전체에 볼", "웨이퍼 상태로 포장\n칩 크기 = 패키지 크기",
        "인터포저 위에 나란히", "칩을 위로 쌓고\nTSV로 연결"]
for i, d in enumerate(desc):
    text(ax, 3.5 + i * 7.3, -0.6, d, size=8.6, color="#444444")
arrow(ax, 1.0, 6.4, 43.0, 6.4, lw=1.4, ms=10, color=C["blue"])
text(ax, 22.0, 6.95, "작게, 얇게, 입출력은 많게, 칩끼리는 가깝게", size=10, color=C["blue"])
save(f, P, "package_evolution")

# 6. TSV
tt = ["① 깊은 구멍 식각 (보쉬)", "② 절연 라이너 (산화막)", "③ 배리어 + Cu 시드", "④ Cu 도금으로 채움",
      "⑤ CMP 후 배선층 계속", "⑥ 뒷면 갈아서 TSV 노출 + 범프"]
f, axs = panels(6, 3, 3.6, 3.6, (0, 10), (-1.4, 8.6), titles=tt, size=10)
for k, ax in enumerate(axs):
    bottom = 0.0 if k < 5 else 2.6
    rect(ax, 0, bottom, 10, 7.0 - bottom, "si", lw=0.6)
    if k >= 4:
        rect(ax, 0, 7.0, 10, 1.0, "lowk", lw=0.5)
        rect(ax, 3.4, 7.25, 3.2, 0.5, "cu", lw=0.4)
    hx0, hx1, hb = 4.2, 5.8, 1.8
    if k == 0:
        rect(ax, hx0, hb, hx1 - hx0, 7.0 - hb, "white", lw=0.6, z=3)
        for y in np.arange(hb + 0.2, 7.0, 0.5):
            ax.add_patch(Arc((hx0, y), 0.3, 0.5, theta1=270, theta2=90, color="#555555", lw=0.6, zorder=4))
            ax.add_patch(Arc((hx1, y), 0.3, 0.5, theta1=90, theta2=270, color="#555555", lw=0.6, zorder=4))
        text(ax, 7.9, 5.2, "깊이 수십 µm\n지름 수 µm", size=8.6)
    if k >= 1:
        hb_ = hb if k < 5 else bottom
        rect(ax, hx0, hb_, hx1 - hx0, 7.0 - hb_, "ox", lw=0.5, z=3)
        if k >= 2:
            rect(ax, hx0 + 0.18, hb_ + (0.18 if k < 5 else 0), hx1 - hx0 - 0.36, 7.0 - hb_ - (0.18 if k < 5 else 0),
                 "tin", lw=0.4, z=3.1)
        if k == 1 or k == 2:
            rect(ax, hx0 + (0.18 if k == 1 else 0.3), hb_ + (0.18 if k == 1 else 0.3),
                 hx1 - hx0 - (0.36 if k == 1 else 0.6), 7.0 - hb_, "white", lw=0.4, z=3.2)
        if k >= 3:
            rect(ax, hx0 + 0.3, hb_ + (0.3 if k < 5 else 0), hx1 - hx0 - 0.6, 7.0 - hb_ - (0.3 if k < 5 else 0),
                 "cu", lw=0.4, z=3.2)
        if k == 3:
            rect(ax, 0, 7.0, 10, 0.7, "cu", lw=0.5, z=3.3)
    if k == 5:
        circ(ax, 5.0, bottom - 0.45, 0.6, "#bdbdbd", lw=0.6, z=4)
        rect(ax, 0, bottom, 10, 0.12, "nit", lw=0.3, z=3.5)
        text(ax, 8.2, 1.4, "얇아진 웨이퍼", size=8.6)
save(f, P, "tsv_steps")

# 7. HBM 2.5D 패키지
f, ax = canvas(12.0, 5.6, (0, 30), (-2.2, 12.6))
rect(ax, 1.0, -0.2, 28.0, 1.6, "#558b2f", lw=0.7)
text(ax, 15.0, 0.6, "패키지 기판", size=9.5, color="white")
for x in np.arange(2.0, 28.5, 1.4):
    circ(ax, x, -0.75, 0.45, "#bdbdbd", lw=0.5)
rect(ax, 2.5, 1.9, 25.0, 1.0, "#b0bec5", lw=0.7)
text(ax, 15.0, 2.4, "실리콘 인터포저 (미세 배선 + TSV)", size=9.2)
for x in np.arange(3.2, 27.0, 1.2):
    circ(ax, x, 1.65, 0.22, "#9e9e9e", lw=0.4)
    line(ax, [x, x], [1.9, 2.9], color=C["cu"], lw=0.8, z=3)
rect(ax, 3.5, 3.3, 11.0, 2.4, "si", lw=0.8)
text(ax, 9.0, 4.5, "GPU / SoC", size=11, weight="bold")
rect(ax, 17.0, 3.3, 8.0, 0.9, "#cfd8dc", lw=0.7)
text(ax, 21.0, 3.75, "베이스 다이 (로직)", size=8.8)
for j in range(8):
    y = 4.4 + j * 0.85
    rect(ax, 17.0, y, 8.0, 0.65, "#90caf9", lw=0.5)
for x in (18.5, 20.0, 22.0, 23.5):
    line(ax, [x, x], [3.3, 11.05], color=C["cu"], lw=1.2, z=4)
text(ax, 21.0, 11.75, "HBM: DRAM 8단 적층", size=10, weight="bold")
text(ax, 27.3, 7.6, "TSV +\n마이크로 범프", size=8.8, ha="left")
arrow(ax, 27.2, 7.6, 23.7, 7.6, lw=0.8, ms=7, color="#555555")
ax.annotate("", xy=(17.0, 4.6), xytext=(14.5, 4.6), arrowprops=dict(arrowstyle="<|-|>", color=C["red"], lw=1.3))
text(ax, 9.0, 6.7, "GPU와 HBM을 인터포저 배선으로\n짧고 넓게 연결", size=8.8, color=C["red"])
save(f, P, "hbm")

# 8. 마이크로 범프 vs 하이브리드 본딩
f, axs = panels(2, 2, 5.6, 3.6, (0, 12), (-0.6, 7.2), titles=["마이크로 범프: 솔더로 붙임 (피치 수십 µm)",
                                                           "하이브리드 본딩: Cu끼리, 산화막끼리 직접 (피치 수 µm 이하)"],
                size=10.5)
for k, ax in enumerate(axs):
    if k == 0:
        rect(ax, 0.5, 0.0, 11.0, 2.0, "si", lw=0.7)
        rect(ax, 0.5, 4.2, 11.0, 2.0, "si", lw=0.7)
        for x in (2.5, 6.0, 9.5):
            rect(ax, x - 0.6, 2.0, 1.2, 0.4, "cu", lw=0.4)
            rect(ax, x - 0.6, 3.8, 1.2, 0.4, "cu", lw=0.4)
            ax.add_patch(Ellipse((x, 3.1), 1.6, 1.4, fc="#bdbdbd", ec="#333333", lw=0.5, zorder=3))
        rect(ax, 0.5, 2.0, 11.0, 2.2, "#ffe082", lw=0.0, z=1.5, alpha=0.5)
        text(ax, 6.0, 6.8, "사이를 언더필로 채움", size=8.8)
    else:
        rect(ax, 0.5, 0.0, 11.0, 2.0, "si", lw=0.7)
        rect(ax, 0.5, 2.0, 11.0, 1.1, "ox", lw=0.5)
        rect(ax, 0.5, 3.1, 11.0, 1.1, "ox", lw=0.5)
        rect(ax, 0.5, 4.2, 11.0, 2.0, "si", lw=0.7)
        for x in np.arange(1.3, 11.0, 1.5):
            rect(ax, x - 0.4, 2.0, 0.8, 2.2, "cu", lw=0.4, z=3)
        line(ax, [0.5, 11.5], [3.1, 3.1], color="#555555", lw=0.8, ls="--", z=4)
        text(ax, 6.0, 6.8, "범프 없이 면끼리 붙이고 열처리 → 간격을 훨씬 좁게", size=8.8)
save(f, P, "hybrid_bonding")
