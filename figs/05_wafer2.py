import numpy as np
from common import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

P = 5

# 1. ingot → wafer 가공 순서
tt = ["① 양 끝 자르고 외경 연삭", "② notch(또는 flat) 내기", "③ wire saw로 얇게 절단", "④ lapping, edge 다듬기",
      "⑤ 식각 (손상층 제거)", "⑥ polishing (거울면)", "⑦ 세정, 검사"]
f, axs = panels(7, 4, 3.2, 2.7, (0, 10), (0, 7), titles=tt, size=10)
a = axs
rect(a[0], 1.5, 2.2, 7.0, 2.6, "#c9d1d9")
rect(a[0], 1.5, 4.8, 7.0, 0.25, "#9e9e9e", lw=0.4)
rect(a[0], 1.5, 1.95, 7.0, 0.25, "#9e9e9e", lw=0.4)
for x in (1.5, 8.5):
    line(a[0], [x, x], [1.3, 5.7], color="red", lw=1.4, ls="--")
text(a[0], 5.0, 0.8, "지름을 정확히 맞춤", size=8.5)
wafer_top(a[1], 5.0, 3.4, 2.6, c="#c9d1d9")
arrow(a[1], 7.6, 0.8, 5.25, 0.88, lw=0.9, ms=8)
text(a[1], 7.7, 0.8, "notch", size=9, ha="left")
rect(a[2], 1.0, 2.0, 8.0, 3.0, "#c9d1d9")
for x in np.linspace(1.6, 8.4, 10):
    line(a[2], [x, x], [1.2, 5.8], color="#555555", lw=1.0)
text(a[2], 5.0, 0.6, "수백 가닥 wire + 연마재", size=8.5)
for k, ax_ in enumerate([a[3], a[4], a[5]]):
    ax_.add_patch(FancyBboxPatch((1.0, 2.6), 8.0, 1.6, boxstyle="round,pad=0,rounding_size=0.7",
                                 fc="#c9d1d9", ec=EC, lw=0.8, zorder=2))
xs = np.linspace(1.2, 8.8, 40)
a[3].plot(xs, 4.2 + 0.08 * np.sin(xs * 9), color="#555555", lw=0.8, zorder=5)
text(a[3], 5.0, 1.5, "두께 맞추고 가장자리를 둥글게", size=8.5)
rect(a[4], 1.0, 3.95, 8.0, 0.25, "#e57373", lw=0, alpha=0.6, z=3)
text(a[4], 5.0, 5.0, "절단·lapping 손상층", size=8.5, color=C["red"])
text(a[4], 5.0, 1.5, "산 / alkali 용액으로 녹여냄", size=8.5)
rect(a[5], 0.5, 4.5, 9.0, 0.6, "#8d6e63", lw=0.6)
text(a[5], 5.0, 5.6, "pad + slurry", size=8.5)
text(a[5], 5.0, 1.5, "표면 거칠기 nm 이하", size=8.5)
wafer_top(a[6], 5.0, 3.6, 2.4, c="#dfe6ec")
for (x, y) in [(4.0, 4.1), (5.9, 3.0), (5.2, 4.8)]:
    circ(a[6], x, y, 0.08, "#333333")
text(a[6], 5.0, 0.6, "particle, 평탄도, 두께 검사", size=8.5)
save(f, P, "ingot_to_wafer")

# 2. flat, notch
f, axs = plt.subplots(1, 5, figsize=(14, 3.4))
specs = [("p형 (111)", [(-90, 0.07)], False), ("n형 (111)", [(-90, 0.07), (-45, 0.035)], False),
         ("p형 (100)", [(-90, 0.07), (0, 0.035)], False), ("n형 (100)", [(-90, 0.07), (90, 0.035)], False),
         ("300 mm: notch", None, True)]
for ax, (t, fl, nt) in zip(axs, specs):
    canvas(0, 0, (-1.3, 1.3), (-1.4, 1.3), ax=ax)
    wafer_top(ax, 0, 0, 1.0, c="#c9d1d9", flats=fl, notch=nt)
    ax.set_title(t, fontsize=11)
axs[0].text(0, -1.25, "1차 flat만", ha="center", fontsize=8.8)
axs[1].text(0, -1.25, "2차 flat 45°", ha="center", fontsize=8.8)
axs[2].text(0, -1.25, "2차 flat 90°", ha="center", fontsize=8.8)
axs[3].text(0, -1.25, "2차 flat 180°", ha="center", fontsize=8.8)
axs[4].text(0, -1.25, "작은 V 홈 하나", ha="center", fontsize=8.8)
plt.suptitle("예전 wafer: flat 위치로 결정면과 doping 구분 / 지금 200, 300 mm: 주로 notch", fontsize=11.5, y=1.02)
save(f, P, "notch_flat")

# 3. 결정면
f = plt.figure(figsize=(12, 4.2))
planes = {"(100)": [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)],
          "(110)": [(1, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 1)],
          "(111)": [(1, 0, 0), (0, 1, 0), (0, 0, 1)]}
edges = [((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 1, 0)),
         ((1, 0, 0), (1, 0, 1)), ((0, 1, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1)), ((0, 0, 1), (1, 0, 1)),
         ((0, 0, 1), (0, 1, 1)), ((1, 1, 0), (1, 1, 1)), ((1, 0, 1), (1, 1, 1)), ((0, 1, 1), (1, 1, 1))]
for k, (name, pts) in enumerate(planes.items()):
    ax = f.add_subplot(1, 3, k + 1, projection="3d")
    for p0, p1 in edges:
        ax.plot(*zip(p0, p1), color="#555555", lw=1.0)
    ax.add_collection3d(Poly3DCollection([pts], fc=PAL[k], alpha=0.45, ec=PAL[k]))
    ax.set_title(name + " 면", fontsize=12, fontweight="bold")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=30)
    ax.set_axis_off()
    for v, s in [((1.25, 0, 0), "x"), ((0, 1.25, 0), "y"), ((0, 0, 1.25), "z")]:
        ax.quiver(0, 0, 0, *v, color="#999999", arrow_length_ratio=0.08, lw=0.8)
        ax.text(*(np.array(v) * 1.08), s, fontsize=10)
save(f, P, "miller")

# 4. wafer 크기와 chip 수
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.2), gridspec_kw=dict(width_ratios=[1.35, 1]))
canvas(0, 0, (-10, 1170), (-250, 260), ax=ax1)
x = 0
for d in [100, 150, 200, 300, 450]:
    r = d / 2
    wafer_top(ax1, x + r, 0, r, c="#c9d1d9" if d != 450 else "#eeeeee", notch=d >= 200)
    text(ax1, x + r, -r - 30, f"{d} mm" + (" (보류)" if d == 450 else ""), size=10)
    x += d + 25
ax1.set_title("wafer 지름 비교 (같은 축척)", fontsize=11.5, loc="left")
ds = np.array([150, 200, 300, 450])
for S, c in zip([50, 100, 200], PAL):
    dpw = np.pi * (ds / 2) ** 2 / S - np.pi * ds / np.sqrt(2 * S)
    ax2.plot(ds, dpw, "o-", color=c, lw=2, label=f"chip 면적 {S} mm²")
ax2.set_xlabel("wafer 지름 (mm)")
ax2.set_ylabel("wafer당 chip 수 (근사)")
ax2.set_xticks(ds)
ax2.grid(alpha=0.25)
ax2.legend(fontsize=9.5)
ax2.set_title("지름 1.5배 → chip 수 2.4배 정도", fontsize=11.5, loc="left")
plt.tight_layout()
save(f, P, "wafer_size")

# 5. wafer 각 부분
f, ax = canvas(10, 6.4, (-1.35, 2.75), (-1.25, 1.25))
wafer_top(ax, 0, 0, 1.0, c="#d5dbe1", lw=1.2)
clip = Circle((0, 0), 1.0, transform=ax.transData)
ax.add_patch(Circle((0, 0), 0.94, fc="none", ec=C["red"], ls="--", lw=1.0, zorder=6))
p, s_ = 0.16, 0.015
for i in np.arange(-7, 7):
    for j in np.arange(-7, 7):
        x0, y0 = i * p + s_ / 2, j * p + s_ / 2
        cs = [(x0, y0), (x0 + p - s_, y0), (x0, y0 + p - s_), (x0 + p - s_, y0 + p - s_)]
        inside = all(np.hypot(*c_) < 0.94 for c_ in cs)
        partial = any(np.hypot(*c_) < 1.0 for c_ in cs) and not inside
        if inside:
            rect(ax, x0, y0, p - s_, p - s_, "#f7f9fb", lw=0.4, z=3)
        elif partial:
            r_ = rect(ax, x0, y0, p - s_, p - s_, "#9aa3ab", lw=0.3, z=2.5, alpha=0.55)
            r_.set_clip_path(clip)
notes = [((0.08, 0.08), (1.25, 0.9), "die (chip 하나)"), ((0.16 - 0.0075, 0.3), (1.25, 0.55), "scribe line\n(자를 자리, TEG 배치)"),
         ((0.88, 0.42), (1.25, 0.15), "가장자리 불완전 die"), ((0.93, -0.25), (1.25, -0.35), "가장자리 미사용 영역"),
         ((0, -1.0), (1.25, -0.85), "notch")]
for (px, py), (tx, ty), s in notes:
    text(ax, tx, ty, s, size=10, ha="left", box="white")
    arrow(ax, tx - 0.02, ty, px, py, lw=0.8, ms=7, color="#555555")
save(f, P, "wafer_parts")

# 6. wafer 종류
f, axs = panels(3, 3, 4.2, 3.4, (0, 10), (0, 8), titles=["일반 (polished) wafer", "epi wafer", "SOI wafer"],
                size=11)
for ax in axs:
    rect(ax, 0.5, 0.5, 9, 5.0, "#c9d1d9", lw=0.8)
    for x0 in (0.2, 9.2):
        pass
    ax.plot([0.3, 9.7], [2.6, 2.6], color="white", lw=6, zorder=5)
    ax.plot([0.3, 9.7], [2.6, 2.6], color="#999999", lw=0.8, ls=(0, (4, 3)), zorder=6)
text(axs[0], 5.0, 1.4, "Si 단결정 (300 mm면 775 µm 두께)", size=10)
rect(axs[1], 0.5, 5.5, 9, 1.0, "epi", lw=0.8)
text(axs[1], 5.0, 6.0, "epi층 (수 µm, 저농도)", size=10)
text(axs[1], 5.0, 1.4, "기판 (고농도로 doping하기도 함)", size=10)
rect(axs[2], 0.5, 5.5, 9, 0.7, "box", lw=0.8)
rect(axs[2], 0.5, 6.2, 9, 0.6, "#dfe6ec", lw=0.8)
text(axs[2], 5.0, 6.5, "Top Si (소자가 들어가는 층)", size=8.6)
text(axs[2], 5.0, 5.85, "BOX (매몰 산화막)", size=8.6)
text(axs[2], 5.0, 1.4, "handle wafer (받침)", size=10)
save(f, P, "wafer_types")
