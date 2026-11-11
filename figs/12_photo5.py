import numpy as np
from common import *
import importlib

aerial = importlib.import_module("11_photo4").aerial
P = 12

# 1. 조명 모양
f, axs = panels(4, 4, 2.8, 3.0, (-1.25, 1.25), (-1.3, 1.25),
                titles=["일반 (원형)", "annular (고리)", "dipole (2극)", "quadrupole (4극)"], size=11)
for ax in axs:
    ax.add_patch(Circle((0, 0), 1.0, fc="#263238", ec="#333333", lw=1.0))
axs[0].add_patch(Circle((0, 0), 0.7, fc="#ffe082", ec="none"))
axs[1].add_patch(Wedge((0, 0), 0.85, 0, 360, width=0.3, fc="#ffe082", ec="none"))
for x in (-0.65, 0.65):
    axs[2].add_patch(Circle((x, 0), 0.22, fc="#ffe082", ec="none"))
for a in (45, 135, 225, 315):
    axs[3].add_patch(Circle((0.65 * np.cos(np.deg2rad(a)), 0.65 * np.sin(np.deg2rad(a))), 0.2,
                            fc="#ffe082", ec="none"))
for ax in axs:
    ax.text(0, -1.22, "노란 부분에서만 빛이 나옴", ha="center", fontsize=8.6)
save(f, P, "illumination")

# 2. 사입사 조명 원리
f, axs = panels(2, 2, 5.6, 5.0, (0, 10), (0, 10),
                titles=["수직 조명: 0차만 들어감 → pattern X", "비스듬한 조명: 0차 + 1차가 같이 들어감 → pattern O"],
                size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 1.0, 8.4, 8.0, 0.25, "#e3f2fd", lw=0.6)
    for x0 in np.arange(1.0, 9.0, 0.5):
        rect(ax, x0, 8.4, 0.25, 0.12, "#424242", lw=0.2)
    ax.add_patch(Ellipse((5.0, 5.0), 5.6, 0.8, fc="#e1f5fe", ec="#4fc3f7", lw=1.2, zorder=4))
    rect(ax, 1.5, 0.6, 7.0, 0.5, "si", lw=0.6)
    tilt = 0 if k == 0 else np.deg2rad(-25)
    arrow(ax, 5.0 + np.tan(tilt) * 1.2, 9.9, 5.0, 8.7, color="orange", lw=2)
    for m in (-1, 0, 1):
        ang = tilt + m * np.deg2rad(50)
        x_lens = 5.0 - np.tan(ang) * 3.4
        col = "#8e44ad" if m == 0 else C["blue"]
        if abs(x_lens - 5.0) < 2.7:
            line(ax, [5.0, x_lens], [8.4, 5.0], color=col, lw=1.6)
            line(ax, [x_lens, 5.0], [5.0, 1.1], color=col, lw=1.6)
            text(ax, (5.0 + x_lens) / 2 + 0.6, 7.0, "0차" if m == 0 else f"{m:+d}차", size=9.5, color=col)
        else:
            xe, ye = 5.0 - 2.4 * np.sin(ang), 8.4 - 2.4 * np.cos(ang)
            line(ax, [5.0, xe], [8.4, ye], color=col, lw=1.4, ls="--")
            text(ax, xe, ye - 0.3, "×", size=14, color=C["red"], weight="bold")
text(axs[1], 5.0, 0.05, "두 beam만 겹쳐도 간섭 무늬(pattern)가 생김 → 같은 lens로 더 작은 pitch", size=9.2, va="bottom")
save(f, P, "oai")

# 3. OPC (mask → 흐려짐 → 문턱값으로 PR 모양)
N = 400
px = 2.5  # nm
xx, yy = np.meshgrid(np.arange(N) * px, np.arange(N) * px)


def rects_to_mask(rs):
    m = np.zeros((N, N))
    for x0, y0, x1, y1 in rs:
        m[(xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)] = 1
    return m


def blur(m, s=28):
    k = np.exp(-((np.fft.fftfreq(N, px)[None, :]) ** 2 + (np.fft.fftfreq(N, px)[:, None]) ** 2)
               * 2 * (np.pi * s) ** 2)
    return np.real(np.fft.ifft2(np.fft.fft2(m) * k))


target = [(150, 650, 700, 710), (150, 450, 700, 510), (150, 250, 420, 310), (360, 110, 420, 310)]
bb = 5
opc = [(140, 650 - bb, 710, 710 + bb), (140, 625, 180, 735), (670, 625, 710, 735),
       (140, 450 - bb, 710, 510 + bb), (140, 425, 180, 535), (670, 425, 710, 535),
       (140, 250 - bb, 420 + bb, 310 + bb), (140, 225, 180, 335),
       (360 - bb, 100, 420 + bb, 310 + bb), (335, 100, 445, 140),
       (412, 302, 448, 338)]
notch = [(355, 245, 372, 262)]
f, axs = plt.subplots(1, 2, figsize=(12, 5.6))
for ax, (title, rs) in zip(axs, [("보정 없음: mask = 원하는 모양", target), ("OPC: 모서리, 선 끝을 미리 보정", opc)]):
    m = rects_to_mask(rs)
    if rs is opc:
        for x0, y0, x1, y1 in notch:
            m[(xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)] = 0
    im = blur(m, s=34)
    ax.imshow(m, origin="lower", extent=[0, N * px, 0, N * px], cmap="Greys", vmin=0, vmax=2.2)
    ax.contour(xx, yy, im, levels=[0.5], colors=[C["red"]], linewidths=2.2)
    for x0, y0, x1, y1 in target:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec=C["blue"], ls="--", lw=1.0, zorder=5))
    ax.set_xlim(60, 800)
    ax.set_ylim(60, 800)
    ax.set_title(title, fontsize=11, loc="left")
    ax.set_xticks([])
    ax.set_yticks([])
axs[0].text(430, 70, "회색: mask, 파란 점선: 원하는 모양, 빨간 선: 실제로 찍힌 PR", ha="center", fontsize=9.5)
axs[0].text(712, 665, "선 끝이\n짧아짐", fontsize=9.5, color=C["red"])
axs[0].text(440, 300, "모서리가\n둥글어짐", fontsize=9.5, color=C["red"])
plt.tight_layout()
save(f, P, "opc")

# 4. 위상 반전 mask
p = 0.9
f, axs = plt.subplots(2, 2, figsize=(12, 5.2), gridspec_kw=dict(height_ratios=[1, 2.4]))
for k, (name, ph) in enumerate([("일반 mask (binary)", False), ("교대 위상 반전 mask (Alt-PSM)", True)]):
    ax = axs[0, k]
    canvas(0, 0, (0, 4 * p), (0, 1.0), ax=ax)
    ax.set_aspect("auto")
    rect(ax, 0, 0.45, 4 * p, 0.45, "#e3f2fd", lw=0.6)
    for j in range(4):
        rect(ax, j * p + p / 2, 0.33, p / 2, 0.12, "#424242", lw=0.3)
        if ph and j % 2 == 1:
            rect(ax, j * p, 0.45, p / 2, 0.15, "#ffffff", lw=0.5)
            text(ax, j * p + p / 4, 0.75, "180°", size=8.5, color=C["red"])
    ax.set_title(name, fontsize=11, loc="left")
    x, m, E = aerial(p, phase=ph)
    ax = axs[1, k]
    ax.plot(x, np.real(E), "--", color=PAL[0], lw=1.4, label="전기장 (진폭)")
    ax.plot(x, np.abs(E) ** 2, color=PAL[1], lw=2.2, label="세기 (PR이 느끼는 것)")
    ax.set_xlim(0, 4 * p)
    ax.set_ylim(-1.1, 1.3)
    ax.axhline(0, color="#999999", lw=0.6)
    ax.set_xlabel("위치 (λ/NA 단위), pitch 0.9")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9, loc="lower right")
axs[1, 0].text(1.8, 0.55, "pitch가 한계보다 작아서 평평함", ha="center", fontsize=10, color=PAL[1])
axs[1, 1].text(1.8, 1.12, "이웃끼리 위상이 반대 → 사이에서 0으로 상쇄", ha="center", fontsize=10, color=PAL[1])
plt.tight_layout()
save(f, P, "psm")

# 5. 액침
f, axs = panels(2, 2, 5.4, 4.2, (0, 10), (0, 8), titles=["건식: 큰 각도 빛은 lens 밖으로 못 나옴",
                                                       "액침: lens와 wafer 사이를 물로 채움"], size=10.5)
for k, ax in enumerate(axs):
    poly(ax, [(1.0, 4.0), (9.0, 4.0), (9.0, 6.0), (7.5, 7.6), (2.5, 7.6), (1.0, 6.0)], "#e1f5fe", ec="#4fc3f7", lw=1.2)
    text(ax, 6.0, 6.9, "마지막 lens (n ≈ 1.56)", size=9.5)
    rect(ax, 1.0, 1.0, 8.0, 0.6, "si", lw=0.6)
    if k == 1:
        rect(ax, 1.0, 1.6, 8.0, 2.4, "#bbdefb", lw=0.4, alpha=0.8)
        text(ax, 8.6, 2.6, "물\nn = 1.44", size=9.2, ha="right")
    line(ax, [3.0, 5.0], [7.0, 4.0], color="#8e44ad", lw=1.6)
    if k == 0:
        line(ax, [5.0, 6.6], [4.0, 6.4], color="#8e44ad", lw=1.4, ls="--")
        text(ax, 6.8, 5.9, "전반사", size=9.5, color=C["red"], ha="left")
    else:
        line(ax, [5.0, 5.0 + 2.4 * 0.62], [4.0, 1.6], color="#8e44ad", lw=1.6)
text(axs[0], 5.0, 0.3, "NA는 최대 1 미만 (공기 n = 1)", size=9.5)
text(axs[1], 5.0, 0.3, "NA = n·sinθ → 최대 약 1.35", size=9.5)
save(f, P, "immersion")


# 6. SADP
def sadp(ax, k):
    rect(ax, 0.3, 0.3, 9.4, 1.2, "si", lw=0.6)
    rect(ax, 0.3, 1.5, 9.4, 0.8, "poly", lw=0.6)
    mand = [(1.2, 2.75), (5.2, 6.75)]
    t = 0.45
    if k in (0, 1, 2):
        for a, b in mand:
            rect(ax, a, 2.3, b - a, 1.6, "#5d4037", lw=0.6)
    if k == 1:
        from cmos import conformal
        conformal(ax, [(a, b, 3.9) for a, b in mand], t, "ox", base=2.3, x0=0.3, x1=9.7)
    if k in (2, 3, 4):
        for a, b in mand:
            rect(ax, a - t, 2.3, t, 1.6, "ox", lw=0.6)
            rect(ax, b, 2.3, t, 1.6, "ox", lw=0.6)
    if k == 4:
        rect(ax, 0.3, 1.5, 9.4, 0.8, "white", lw=0)
        for a, b in mand:
            for x0 in (a - t, b):
                rect(ax, x0, 1.5, t, 0.8, "poly", lw=0.6)
        line(ax, [0.3, 9.7], [1.5, 1.5], lw=0.6)
    if k == 5:
        rect(ax, 0.3, 1.5, 9.4, 0.8, "white", lw=0)
        line(ax, [0.3, 9.7], [1.5, 1.5], lw=0.6)
        for a, b in mand:
            for x0 in (a - t, b):
                rect(ax, x0, 1.5, t, 0.8, "poly", lw=0.6)
        bracket(ax, 0.75, 2.75, 2.7, "새 pitch = 원래의 절반", size=9, color=C["blue"])


tt = ["① mandrel(희생 pattern) 만들기", "② spacer 막을 고르게 증착", "③ etch back → 옆벽 spacer만 남김",
      "④ mandrel 제거", "⑤ spacer를 mask로 아래 막 식각", "⑥ spacer 제거 → 선 개수 2배"]
f, axs = panels(6, 3, 3.8, 2.8, (0, 10), (0, 5.4), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    sadp(ax, k)
    if k == 0:
        bracket(ax, 1.2, 5.2, 4.25, "photo로 만든 pitch", size=9)
save(f, P, "sadp")

# 7. LELE
tt = ["① 1차 photo", "② 1차 식각 (hard mask)", "③ 2차 photo (반 pitch 옮겨서)", "④ 2차 식각 → pitch 절반"]
f, axs = panels(4, 4, 3.2, 2.6, (0, 10), (0, 5.0), titles=tt, size=10.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 1.2, "si", lw=0.6)
    hm1 = [(1.0, 2.0), (5.0, 6.0)]
    hm2 = [(3.0, 4.0), (7.0, 8.0)]
    if k == 0:
        rect(ax, 0.3, 1.5, 9.4, 0.6, "nit", lw=0.6)
        for a, b in hm1:
            rect(ax, a, 2.1, b - a, 1.2, "pr", lw=0.6)
    if k >= 1:
        for a, b in hm1:
            rect(ax, a, 1.5, b - a, 0.6, "nit", lw=0.6)
    if k == 2:
        for a, b in hm2:
            rect(ax, a - 0.15, 1.5, b - a + 0.3, 1.8, "pr", lw=0.6)
    if k == 3:
        for a, b in hm2:
            rect(ax, a, 1.5, b - a, 0.6, "#8bc34a", lw=0.6)
        text(ax, 5.0, 3.6, "두 번째 photo가 어긋나면\n간격이 달라짐 (overlay)", size=8.8)
save(f, P, "lele")
