import numpy as np
from common import *
from cmos import conformal

P = 24


# 1. ALD 한 cycle (Al₂O₃: TMA + H₂O)
def surface(ax, state):
    rect(ax, 0.3, 0.3, 9.4, 1.2, "si", lw=0.6)
    xs = np.arange(1.0, 9.5, 1.0)
    for x in xs:
        if state in ("oh", "end"):
            line(ax, [x, x], [1.5, 2.1], lw=1.0)
            circ(ax, x, 2.25, 0.18, "#e57373", lw=0.4)
            text(ax, x, 2.75, "OH", size=7.5, color="#555555")
        if state in ("tma", "purge1"):
            line(ax, [x, x], [1.5, 2.1], lw=1.0)
            circ(ax, x, 2.25, 0.18, "#e57373", lw=0.4)
            circ(ax, x, 2.75, 0.28, "#90a4ae", lw=0.4)
            text(ax, x, 2.75, "Al", size=7, weight="bold")
            for dx in (-0.35, 0.35):
                circ(ax, x + dx, 3.25, 0.15, "#cfd8dc", lw=0.3)
        if state in ("h2o", "purge2"):
            line(ax, [x, x], [1.5, 2.1], lw=1.0)
            circ(ax, x, 2.25, 0.18, "#e57373", lw=0.4)
            circ(ax, x, 2.75, 0.28, "#90a4ae", lw=0.4)
            text(ax, x, 2.75, "Al", size=7, weight="bold")
            circ(ax, x, 3.3, 0.16, "#e57373", lw=0.3)
            text(ax, x, 3.75, "OH", size=7.5, color="#555555")


tt = ["① TMA pulse: 표면 OH에만 붙고 다 차면 멈춤", "② purge (남은 TMA, 부산물 CH₄ 빼냄)", "③ H₂O pulse: CH₃를 OH로 바꿈",
      "④ purge → Al₂O₃ 한 층 (약 0.1 nm)"]
f, axs = panels(4, 2, 5.4, 3.0, (0, 10), (0, 6.0), titles=tt, size=10.2)
surface(axs[0], "tma")
for x, y in [(2.5, 5.2), (6.0, 5.0), (8.3, 5.4)]:
    circ(axs[0], x, y, 0.28, "#90a4ae", lw=0.4)
    for dx in (-0.35, 0.35):
        circ(axs[0], x + dx, y + 0.35, 0.14, "#cfd8dc", lw=0.3)
surface(axs[1], "purge1")
arrow(axs[1], 0.5, 5.0, 9.5, 5.0, color="#90a4ae", lw=1.6)
text(axs[1], 5.0, 5.5, "N₂ / Ar", size=9, color="#607d8b")
surface(axs[2], "h2o")
for x, y in [(2.0, 5.0), (5.5, 5.3), (8.0, 4.9)]:
    circ(axs[2], x, y, 0.2, "#e57373", lw=0.4)
    for dx in (-0.28, 0.28):
        circ(axs[2], x + dx, y - 0.2, 0.12, "#ffffff", lw=0.3)
surface(axs[3], "purge2")
arrow(axs[3], 0.5, 5.0, 9.5, 5.0, color="#90a4ae", lw=1.6)
save(f, P, "ald_cycle")

# 2. cycle 수 / pulse 시간
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.0))
n = np.arange(0, 201)
ax1.plot(n, 0.11 * n, color=PAL[0], lw=2.2)
ax1.set_xlabel("cycle 수")
ax1.set_ylabel("두께 (nm)")
ax1.set_title("두께 = cycle당 두께 × cycle 수", loc="left", fontsize=11)
ax1.grid(alpha=0.25)
tp = np.linspace(0, 1.0, 200)
ax2.plot(tp, 0.11 * (1 - np.exp(-tp / 0.08)), color=PAL[0], lw=2.2, label="ALD: 포화 (자기 제한)")
ax2.plot(tp, 0.11 * tp / 0.25, "--", color=PAL[1], lw=2.0, label="CVD였다면: 계속 늘어남")
ax2.set_ylim(0, 0.3)
ax2.set_xlabel("전구체 pulse 시간 (s)")
ax2.set_ylabel("cycle당 두께 (nm)")
ax2.set_title("pulse를 길게 해도 한 층 이상 안 붙음 (개념)", loc="left", fontsize=11)
ax2.legend(fontsize=9)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "ald_linear")

# 3. ALD 창
T = np.linspace(50, 450, 300)
win = np.full_like(T, 0.11)
f, ax = plot_ax(7.2, 4.2)
ax.plot(T, np.where(T < 150, 0.11 + 0.10 * (150 - T) / 100, np.nan), color=PAL[1], lw=2, label="응축 (너무 차가움)")
ax.plot(T, np.where(T < 150, 0.11 - 0.06 * (150 - T) / 100, np.nan), color=PAL[3], lw=2, label="반응 부족 (너무 차가움)")
ax.plot(T, np.where((T >= 150) & (T <= 300), 0.11, np.nan), color="#222222", lw=3, label="ALD 창")
ax.plot(T, np.where(T > 300, 0.11 + 0.12 * (T - 300) / 150, np.nan), color=PAL[4], lw=2, label="전구체 분해 → CVD처럼")
ax.plot(T, np.where(T > 300, 0.11 - 0.05 * (T - 300) / 150, np.nan), color=PAL[0], lw=2, label="탈착 (너무 뜨거움)")
ax.axvspan(150, 300, color="#c8e6c9", alpha=0.5)
ax.set_xlabel("기판 온도 (°C)")
ax.set_ylabel("cycle당 두께 (nm)")
ax.set_title("ALD 창: cycle당 두께가 온도와 상관없이 일정한 구간 (개념)", loc="left", fontsize=11)
ax.legend(fontsize=8.6, ncol=2)
save(f, P, "ald_window")

# 4. 고종횡비에서 CVD vs ALD
f, axs = panels(2, 2, 3.6, 5.0, (0, 10), (0, 13), titles=["CVD", "ALD"], size=11.5)
for k, ax in enumerate(axs):
    rect(ax, 0.3, 0.3, 9.4, 0.8, "si", lw=0.6)
    rect(ax, 0.3, 1.1, 3.9, 10.4, "si", lw=0.6)
    rect(ax, 5.8, 1.1, 3.9, 10.4, "si", lw=0.6)
    if k == 0:
        poly(ax, [(0.3, 11.5), (4.2, 11.5), (4.2, 1.1), (5.8, 1.1), (5.8, 11.5), (9.7, 11.5), (9.7, 12.2),
                  (5.6, 12.2), (5.35, 11.4), (5.72, 1.2), (4.28, 1.2), (4.65, 11.4), (4.4, 12.2), (0.3, 12.2)],
             "hk", lw=0.5, z=5)
        text(ax, 5.0, 0.0, "아래로 갈수록 얇음", size=9, va="bottom")
    else:
        conformal(ax, [(0.3, 4.2, 11.5), (5.8, 9.7, 11.5)], 0.3, "hk", base=1.1, x0=0.3, x1=9.7)
        text(ax, 5.0, 0.0, "바닥까지 같은 두께", size=9, va="bottom")
save(f, P, "conformal_compare")

# 5. 유전율 vs band gap
mats = [("SiO₂", 3.9, 9.0), ("Si₃N₄", 7, 5.3), ("Al₂O₃", 9, 8.8), ("Y₂O₃", 15, 6.0), ("HfO₂", 25, 5.8),
        ("ZrO₂", 25, 5.8), ("Ta₂O₅", 22, 4.4), ("La₂O₃", 30, 6.0), ("TiO₂", 80, 3.5)]
f, ax = plot_ax(7.2, 4.4)
for (n_, k_, eg), c in zip(mats, PAL * 2):
    col = C["red"] if n_ in ("HfO₂", "ZrO₂") else "#455a64"
    ax.plot(k_, eg, "o", ms=9, color=col)
    off = {"ZrO₂": (-3, -0.75), "HfO₂": (-3, 0.35), "Y₂O₃": (-4, 0.3), "La₂O₃": (3, 0.1)}.get(n_, (2, 0.1))
    ax.text(k_ + off[0], eg + off[1], n_, fontsize=10, color=col)
ax.set_xscale("log")
ax.set_xlabel("유전율 k")
ax.set_ylabel("band gap (eV)")
ax.set_title("유전율이 높을수록 band gap이 작은 경향 (값은 문헌 대략값)", loc="left", fontsize=11)
ax.set_xlim(3, 120)
ax.set_ylim(2.5, 10)
save(f, P, "k_vs_gap")

# 6. 같은 EOT, 다른 물리 두께
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw=dict(width_ratios=[1, 1.1]))
canvas(0, 0, (0, 10), (0, 9), ax=ax1)
ax1.set_title("EOT 1 nm를 만드는 두 방법", loc="left", fontsize=11)
for x0, t, c, s in [(0.6, 0.5, "ox", "SiO₂ 1.0 nm"), (5.6, 3.2, "hk", "HfO₂ 약 6.4 nm")]:
    rect(ax1, x0, 0.6, 3.8, 2.0, "si", lw=0.6)
    rect(ax1, x0, 2.6, 3.8, t, c, lw=0.6)
    rect(ax1, x0, 2.6 + t, 3.8, 2.0, "#78909c", lw=0.6)
    text(ax1, x0 + 1.9, 2.6 + t / 2, s, size=9.5)
    text(ax1, x0 + 1.9, 3.6 + t, "gate", size=9, color="white")
text(ax1, 2.5, 8.2, "얇아서 전자가 tunneling", size=9.5, color=C["red"])
text(ax1, 7.5, 8.2, "두꺼워서 tunneling ↓", size=9.5, color=C["green"])
tt_ = np.linspace(0.5, 7, 200)
for kap, c, lab in [(5.0, PAL[0], "SiO₂ (장벽 높음)"), (2.5, PAL[3], "HfO₂ (장벽 낮음)")]:
    ax2.semilogy(tt_, np.exp(-2 * kap * tt_), color=c, lw=2.2, label=lab)
ax2.plot(1.0, np.exp(-10.0), "o", color=PAL[0], ms=8)
ax2.text(1.2, np.exp(-10.0) * 3, "SiO₂ 1 nm", fontsize=9.5)
ax2.plot(6.4, np.exp(-2 * 2.5 * 6.4), "o", color=PAL[3], ms=8)
ax2.text(5.0, np.exp(-2 * 2.5 * 6.4) * 30, "HfO₂ 6.4 nm", fontsize=9.5)
ax2.set_yticks([])
ax2.minorticks_off()
ax2.set_xlabel("절연막 물리 두께 (nm)")
ax2.set_ylabel("tunneling 누설 (log, 상대값)")
ax2.set_title("tunneling은 두께에 지수적으로 줄어듦 (개념)", loc="left", fontsize=11)
ax2.legend(fontsize=9)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "eot")
