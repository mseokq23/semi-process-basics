import numpy as np
from common import *

P = 3

# 1. fab 단면 (공기 흐름)
f, ax = canvas(11, 6.4, (0, 22), (0, 13))
rect(ax, 1, 10.6, 20, 1.2, "#d9e2ea")                       # FFU 천장
for x in np.arange(2.0, 20.5, 2.0):
    rect(ax, x - 0.7, 10.75, 1.4, 0.9, "#ffffff", lw=0.6, z=3)
    ax.add_patch(Circle((x, 11.2), 0.3, fc="#cfd8dc", ec="#555555", lw=0.6, zorder=4))
text(ax, 11, 12.2, "FFU (fan + HEPA/ULPA filter)", size=10)
rect(ax, 1, 4.6, 20, 0.35, "#ffffff", hatch="||||", lw=0.8)  # grating 바닥
text(ax, 21.3, 4.75, "구멍 뚫린 바닥", size=9, ha="left")
for x in np.arange(2.5, 20, 1.6):
    arrow(ax, x, 10.4, x, 5.3, color="#7fb3d5", lw=1.0, ms=8, z=1)
text(ax, 11, 10.15, "위 → 아래로 곧게 흐르는 공기 (층류)", size=9.5, color=C["blue"], box="white")
# 장비
for x0, w, s in [(3.0, 3.2, "노광기"), (8.0, 2.6, "식각"), (12.2, 2.6, "증착"), (16.2, 3.0, "세정")]:
    box(ax, x0, 5.0, w, 2.6, s, fc="#eef1f4", size=9.5)
line(ax, [1, 21], [9.4, 9.4], color="#555555", lw=2.0, z=6)
rect(ax, 8.3, 8.6, 1.4, 0.6, "#f6c667", lw=0.6, z=6)
text(ax, 9.0, 8.9, "OHT", size=8)
rect(ax, 8.55, 7.85, 0.9, 0.7, "#888888", lw=0.6, z=6)
text(ax, 10.0, 8.2, "FOUP", size=8.5, ha="left", box="white")
# subfab
rect(ax, 1, 0.4, 20, 4.2, "#f1f1f1", lw=0.8)
for x0, s in [(2.0, "진공 pump"), (6.0, "chiller"), (10.0, "gas·약액 공급"), (14.5, "scrubber\n(배기 처리)")]:
    box(ax, x0, 1.0, 3.4, 2.0, s, fc="#ffffff", size=9)
text(ax, 11, 3.8, "subfab (장비를 받쳐주는 설비 층)", size=10)
# 공기 되돌아가는 길
for x in [0.5, 21.5]:
    arrow(ax, x, 5.0, x, 11.0, color="#aaaaaa", lw=1.4, ms=10, ls="--")
text(ax, 0.3, 8.0, "순환", size=8.5, ha="right", color="#777777")
save(f, P, "fab_section")

# 2. clean room 등급
iso = [3, 4, 5, 6, 7, 8, 9]
n05 = [35, 352, 3520, 35200, 352000, 3520000, 35200000]
fed = ["Class 1", "Class 10", "Class 100", "Class 1,000", "Class 10,000", "Class 100,000", "-"]
f, ax = plot_ax(8.0, 4.2)
cols = [PAL[0]] * 6 + ["#aaaaaa"]
ax.bar([f"ISO {i}" for i in iso], n05, color=cols)
ax.set_yscale("log")
ax.set_ylabel("0.5 µm 이상 입자 수 (개/m³)")
for i, (v, s) in enumerate(zip(n05, fed)):
    ax.text(i, v * 1.6, s, ha="center", fontsize=8.5)
ax.text(6, 35200000 / 12, "일반 실내·외\n공기 수준", ha="center", fontsize=8.5, color="white")
ax.set_ylim(10, 3e8)
ax.set_title("clean room 등급 (ISO 14644-1) - 한 단계마다 10배", loc="left")
save(f, P, "cleanroom_class")

# 3. 크기 비교
items = [("머리카락 굵기", 70e-6), ("꽃가루", 25e-6), ("적혈구", 7e-6), ("미세먼지 PM2.5", 2.5e-6),
         ("박테리아", 1e-6), ("바이러스", 0.1e-6), ("최신 chip 배선 간격", 20e-9),
         ("gate 산화막 두께", 1.5e-9)]
f, ax = plt.subplots(figsize=(9, 3.8))
ax.set_xscale("log")
ax.set_xlim(5e-10, 3e-4)
for k, (s, v) in enumerate(items):
    y = len(items) - k
    col = PAL[1] if "chip" in s or "산화막" in s else PAL[0]
    ax.plot([v], [y], "o", color=col, ms=8)
    ax.text(v * 1.4, y, s, va="center", fontsize=9.5)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xticks([1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4])
ax.set_xticklabels(["1 nm", "10 nm", "100 nm", "1 µm", "10 µm", "100 µm"])
ax.grid(axis="x", alpha=0.3)
ax.set_title("크기 비교 (대략값) - 먼지 하나가 pattern 수천 개를 덮음", loc="left", fontsize=11.5)
save(f, P, "size_compare")

# 4. particle 불량
f, axs = plt.subplots(1, 2, figsize=(10, 3.6))
for k, ax in enumerate(axs):
    canvas(0, 0, (0, 10), (0, 6), ax=ax)
    rect(ax, 0, 0, 10, 6, "#f0f3f6", lw=0)
    for y in [1.2, 3.4]:
        if k == 1 and y == 3.4:
            rect(ax, 0.5, y, 3.6, 1.2, "al")
            rect(ax, 6.0, y, 3.5, 1.2, "al")
        else:
            rect(ax, 0.5, y, 9.0, 1.2, "al")
    if k == 0:
        circ(ax, 5.0, 2.95, 1.0, "#6d4c41", ec="#3e2723", z=6)
        ax.set_title("선 사이에 남은 입자 → 단락 (short)", fontsize=11, loc="left")
    else:
        circ(ax, 5.0, 4.0, 0.95, "#6d4c41", ec="#3e2723", z=6)
        ax.set_title("pattern을 가린 입자 → 단선 (open)", fontsize=11, loc="left")
    text(ax, 9.7, 5.4, "위에서 본 금속선", size=8.5, ha="right", color="#555555")
plt.tight_layout()
save(f, P, "particle_defect")

# 5. FOUP, 반송
f, ax = canvas(10, 4.8, (0, 20), (0, 9.6))
line(ax, [0.5, 19.5], [8.6, 8.6], color="#555555", lw=3)
text(ax, 1.0, 9.1, "천장 rail (OHT)", size=9.5, ha="left")
rect(ax, 4.0, 7.8, 2.0, 0.6, "#f6c667", lw=0.6)
line(ax, [4.6, 4.6], [7.8, 6.9], color="#555555", lw=0.9)
line(ax, [5.4, 5.4], [7.8, 6.9], color="#555555", lw=0.9)
rect(ax, 4.0, 5.4, 2.0, 1.5, "#999999", lw=0.8)
for y in np.linspace(5.6, 6.7, 6):
    line(ax, [4.2, 5.8], [y, y], color="#dddddd", lw=0.8)
text(ax, 5.0, 4.95, "FOUP (wafer 25장)", size=9)
arrow(ax, 6.3, 6.1, 8.3, 4.3, color="#555555", lw=1.0, ls="--")
rect(ax, 8.0, 1.0, 2.6, 3.0, "#e0e0e0")
text(ax, 9.3, 2.5, "load\nport", size=9)
rect(ax, 10.6, 1.0, 3.4, 4.2, "#eef1f4")
text(ax, 12.3, 4.5, "EFEM", size=9.5, weight="bold")
text(ax, 12.3, 3.8, "(작은 clean 공간)", size=8.5)
line(ax, [11.5, 12.3, 13.3], [2.0, 2.8, 2.3], color="#444444", lw=2.0)
circ(ax, 12.3, 2.8, 0.18, "#666666")
text(ax, 12.3, 1.5, "robot", size=8.5)
rect(ax, 14.0, 1.0, 5.2, 4.2, "#dfe7ef")
text(ax, 16.6, 3.1, "공정 chamber", size=10, weight="bold")
arrow(ax, 13.4, 2.4, 14.6, 2.4, color="#555555", lw=1.0)
save(f, P, "foup_amhs")
