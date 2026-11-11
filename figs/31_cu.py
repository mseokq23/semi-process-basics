import numpy as np
from common import *

P = 31
EPS0 = 8.854e-14


def tau_ps(rho_uohm, k, W_nm, L_cm=0.1):
    """폭 = 두께 = 간격 = 위아래 절연막 두께인 배선의 RC 곱 (ps)"""
    W = W_nm * 1e-7
    return 4 * rho_uohm * 1e-6 * EPS0 * k * L_cm ** 2 / W ** 2 * 1e12


def rho_cu(w, rho0=1.68, lam=39.0, p=0.0, R=0.3):
    """표면, 결정립 경계 산란을 넣은 대략적인 비저항 (결정립 크기 = 선폭)"""
    return rho0 * (1 + 0.375 * (1 - p) * lam / w + 1.5 * R / (1 - R) * lam / w)


def rho_eff(w, tb=2.0, ar=2.0, **kw):
    h = ar * w
    return rho_cu(w, **kw) * (w * h) / ((w - 2 * tb) * (h - tb))


if __name__ == "__main__":
    for name, r, k in [("Al/SiO2", 2.65, 3.9), ("Cu/SiO2", 1.68, 3.9), ("Cu/low-k", 1.68, 2.5)]:
        print(f"{name}: 1 mm, 100 nm -> RC = {tau_ps(r, k, 100):.0f} ps")
    for w in (10, 20, 50, 100):
        print(f"Cu w={w} nm: rho = {rho_cu(w):.2f}, with barrier = {rho_eff(w):.2f} uOhm cm, "
              f"Ru = {rho_cu(w, rho0=7.1, lam=6.6):.2f}")

    # 1. RC 지연
    W = np.linspace(50, 500, 300)
    f, ax = plot_ax(7.4, 4.4)
    ax.loglog(W, tau_ps(2.65, 3.9, W), color=C["gray"], lw=2.2, label="Al + SiO₂ (k 3.9)")
    ax.loglog(W, tau_ps(1.68, 3.9, W), color=C["cu"], lw=2.2, label="Cu + SiO₂")
    ax.loglog(W, tau_ps(1.68, 2.5, W), color=PAL[0], lw=2.2, label="Cu + Low-k (k 2.5)")
    ax.loglog(W, tau_ps(rho_eff(W), 2.5, W), "--", color=PAL[0], lw=1.8, label="Cu + Low-k, 가는 선 저항 증가 포함")
    ax.set_xticks([50, 100, 200, 500])
    ax.set_xticklabels(["50", "100", "200", "500"])
    ax.minorticks_off()
    ax.set_xlabel("배선 폭 = 두께 = 간격 (nm)")
    ax.set_ylabel("1 mm 배선의 RC (ps)")
    ax.set_title("배선이 가늘어질수록 RC 지연이 제곱으로 커짐 (단순 계산)", loc="left", fontsize=11)
    ax.legend(fontsize=9)
    save(f, P, "rc_delay")

    # 2. 식각 방식 vs damascene
    tt = ["Al ① 금속 증착", "② photo", "③ 금속 식각", "④ 절연막 채우고 CMP",
          "Cu ① 절연막 증착", "② photo", "③ 절연막 식각 (홈)", "④ Cu 채우고 CMP"]
    f, axs = panels(8, 4, 3.3, 2.3, (0, 10), (-0.5, 4.4), titles=tt, size=10)
    L = [(1.5, 3.5), (6.5, 8.5)]
    for k, ax in enumerate(axs):
        rect(ax, 0, -0.5, 10, 0.5, "ox", lw=0.5)
        if k < 4:
            if k < 2:
                rect(ax, 0, 0, 10, 1.4, "al", lw=0.6)
            else:
                for a, b in L:
                    rect(ax, a, 0, b - a, 1.4, "al", lw=0.6, z=3)
            if k in (1, 2):
                for a, b in L:
                    rect(ax, a, 1.4, b - a, 0.7, "pr", lw=0.6, z=3)
            if k == 3:
                rect(ax, 0, 0, 10, 1.4, "ox", lw=0.6, z=2)
            if k == 2:
                for x in (0.7, 5.0, 9.3):
                    arrow(ax, x, 3.2, x, 1.6, color="#555555", lw=0.9, ms=7)
        else:
            if k < 7:
                if k < 6:
                    rect(ax, 0, 0, 10, 1.4, "lowk", lw=0.6)
                else:
                    rect(ax, 0, 0, 10, 1.4, "lowk", lw=0.6)
                    for a, b in L:
                        rect(ax, a, 0, b - a, 1.4, "white", lw=0.6, z=3)
                if k in (5, 6):
                    for a, b in [(0, 1.5), (3.5, 6.5), (8.5, 10)]:
                        rect(ax, a, 1.4, b - a, 0.7, "pr", lw=0.6, z=3)
                if k == 6:
                    for x in (2.5, 7.5):
                        arrow(ax, x, 3.2, x, 0.4, color="#555555", lw=0.9, ms=7, z=6)
            else:
                rect(ax, 0, 0, 10, 1.4, "lowk", lw=0.6)
                for a, b in L:
                    rect(ax, a, 0, b - a, 1.4, "tin", lw=0.5, z=3)
                    rect(ax, a + 0.12, 0.12, b - a - 0.24, 1.28, "cu", lw=0.5, z=3.1)
    text(axs[3], 5.0, 3.3, "금속을 깎아서 배선", size=9.5, weight="bold", color="#555555")
    text(axs[7], 5.0, 3.3, "홈을 파고 금속을 채워서 배선", size=9.5, weight="bold", color=C["cu"])
    save(f, P, "subtractive_vs_damascene")

    # 3. dual damascene (via 먼저)
    tt = ["① cap / Low-k / hard mask 적층", "② via photo + 식각 (cap에서 멈춤)", "③ trench photo + 식각, 바닥 cap 열기",
          "④ barrier (TaN/Ta) + Cu seed (PVD)", "⑤ Cu 전해도금으로 채움", "⑥ CMP + cap 증착"]
    f, axs = panels(6, 3, 3.9, 3.0, (0, 10), (-1.7, 5.6), titles=tt, size=10)
    YC, YL, YH = 0.25, 4.0, 4.3          # cap 위, low-k 위, hard mask 위
    VX, TX, YT = (4.4, 5.6), (2.4, 7.6), 2.2
    t = 0.14
    for k, ax in enumerate(axs):
        rect(ax, 0, -1.7, 10, 1.7, "lowk", lw=0.5)
        rect(ax, 3.3, -1.4, 3.4, 1.2, "tin", lw=0.5)
        rect(ax, 3.42, -1.28, 3.16, 1.08, "cu", lw=0.5)
        text(ax, 5.0, -0.75, "아래 배선 (M1)", size=8.2, color="white")
        rect(ax, 0, 0, 10, YC, "nit", lw=0.5, z=2.4)
        rect(ax, 0, YC, 10, YL - YC, "lowk", lw=0.6)
        if k < 5:
            rect(ax, 0, YL, 10, YH - YL, "ox", lw=0.5)
        if k == 1:
            rect(ax, VX[0], YC, VX[1] - VX[0], YH - YC, "white", lw=0.6, z=3)
        if k >= 2:
            rect(ax, TX[0], YT, TX[1] - TX[0], (YH if k < 5 else YL) - YT, "white", lw=0.6, z=3)
            rect(ax, VX[0], 0.0, VX[1] - VX[0], YT - 0.0, "white", lw=0.6, z=3)
        if k in (3, 4, 5):
            top = YH if k < 5 else YL
            segs = [(0, top, TX[0], t), (TX[0], YT, t, top - YT + t), (TX[0], YT, VX[0] - TX[0], t),
                    (VX[0], 0.0, t, YT), (VX[0], 0.0, VX[1] - VX[0], t), (VX[1] - t, 0.0, t, YT),
                    (VX[1], YT, TX[1] - VX[1], t), (TX[1] - t, YT, t, top - YT + t), (TX[1], top, 10 - TX[1], t)]
            if k == 5:
                segs = segs[1:-1]
            for (x, y, w, h) in segs:
                rect(ax, x, y, w, h, "tin", lw=0.0, z=4)
        if k in (4, 5):
            rect(ax, TX[0] + t, YT + t, TX[1] - TX[0] - 2 * t, (YH if k == 4 else YL) - YT - t + (0.0 if k == 5 else 0.14),
                 "cu", lw=0.5, z=4.1)
            rect(ax, VX[0] + t, t, VX[1] - VX[0] - 2 * t, YT, "cu", lw=0.0, z=4.1)
            if k == 4:
                rect(ax, 0, YH + t, 10, 0.75, "cu", lw=0.5, z=4.1)
        if k == 5:
            rect(ax, 0, YL, 10, 0.25, "nit", lw=0.5, z=4.5)
        if k in (1, 2):
            pr_x = [(0, VX[0]), (VX[1], 10)] if k == 1 else [(0, TX[0]), (TX[1], 10)]
            for a, b in pr_x:
                rect(ax, a, YH, b - a, 0.6, "pr", lw=0.5, z=3.5)
    text(axs[0], 8.6, 2.1, "Low-k", size=9)
    text(axs[0], 8.6, 0.55, "cap (SiCN)", size=8.4)
    text(axs[5], 5.0, 3.1, "배선", size=9, color="white", weight="bold")
    text(axs[5], 5.0, 1.1, "via", size=8.6, color="white", weight="bold")
    save(f, P, "dual_damascene")

    # 4. 전해도금 장치
    f, ax = canvas(8.6, 4.6, (0, 17), (-0.6, 8.8))
    rect(ax, 1.0, 0.0, 15.0, 5.6, "#e3f2fd", lw=1.0)
    text(ax, 13.6, 3.9, "CuSO₄ + H₂SO₄\n+ 첨가제", size=9.5)
    rect(ax, 4.5, 0.5, 8.0, 0.6, "cu", lw=0.7)
    text(ax, 8.5, 0.8, "Cu 양극 (+): Cu → Cu²⁺ + 2e⁻", size=9, color="white", weight="bold")
    rect(ax, 3.5, 5.0, 10.0, 0.35, "si", lw=0.8, z=4)
    rect(ax, 3.5, 5.35, 10.0, 0.9, "#9e9e9e", lw=0.8, z=4)
    text(ax, 8.5, 5.8, "wafer holder (회전)", size=9, color="white")
    text(ax, 8.5, 6.9, "wafer (−): 아래를 보고 담김, seed층에 전류 연결", size=9.5)
    text(ax, 8.5, 4.65, "Cu²⁺ + 2e⁻ → Cu (seed 위에 쌓임)", size=9, color=C["cu"], weight="bold")
    for x in (5.5, 8.0, 10.5):
        arrow(ax, x, 1.5, x, 4.2, color=C["cu"], lw=1.3, ms=10)
        text(ax, x + 0.55, 2.6, "Cu²⁺", size=9, color=C["cu"])
    line(ax, [13.5, 15.2, 15.2], [5.6, 5.6, 7.9], color="#555555", lw=1.0)
    line(ax, [12.5, 15.8, 15.8], [0.8, 0.8, 7.9], color="#555555", lw=1.0)
    box(ax, 14.5, 7.6, 2.2, 0.9, "전원", fc="#fff8e1", size=9.5)
    save(f, P, "ecp_cell")

    # 5. superfill
    f, axs = panels(3, 3, 3.5, 3.6, (0, 10), (-0.4, 8.8), titles=["첨가제 없이: 입구가 먼저 막힘 → void",
                                                               "superfill: 바닥부터 빨리 차오름", "다 차면: 가운데가 살짝 볼록"],
                    size=10)
    x0, x1, yb, yt = 3.5, 6.5, 0.6, 6.6
    for k, ax in enumerate(axs):
        rect(ax, 0, -0.4, 10, 1.0, "lowk", lw=0.5)
        rect(ax, 0, yb, x0, yt - yb, "lowk", lw=0.6)
        rect(ax, x1, yb, 10 - x1, yt - yb, "lowk", lw=0.6)
        if k == 0:
            poly(ax, [(0, yt), (x0, yt), (x0, yb), (x1, yb), (x1, yt), (10, yt), (10, yt + 1.0), (0, yt + 1.0)],
                 "cu", lw=0.6, z=3)
            poly(ax, [(4.7, 2.0), (5.3, 2.0), (5.6, 5.0), (5.15, 6.4), (4.85, 6.4), (4.4, 5.0)], "white", lw=0.6, z=4)
            text(ax, 5.0, 4.0, "void", size=8.8, color=C["red"], weight="bold", rotation=90)
        elif k == 1:
            for i, (hb, c) in enumerate([(1.4, "#f3c9a6"), (2.8, "#eab183"), (4.3, "#e19a62")]):
                pts = [(x0, yb), (x1, yb), (x1, hb + 1.0 - 0.2 * i), (x1 - 0.4, hb + 1.0), (x0 + 0.4, hb + 1.0),
                       (x0, hb + 1.0 - 0.2 * i)]
                poly(ax, pts, c, lw=0.6, z=3 - 0.1 * i)
            for xx in (4.1, 4.8, 5.5):
                text(ax, xx + 0.15, 5.5, "A", size=8.5, color=C["green"], weight="bold")
            for xx in np.arange(0.5, 3.4, 0.8):
                text(ax, xx, yt + 0.3, "S", size=8.5, color=C["red"], weight="bold")
            for xx in np.arange(6.9, 9.8, 0.8):
                text(ax, xx, yt + 0.3, "S", size=8.5, color=C["red"], weight="bold")
            text(ax, 5.0, 7.9, "A: 가속제 (바닥에 모임)\nS: 억제제 (윗면, 벽)", size=8.6)
            line(ax, [x0, x0], [yb, yt], lw=0.8)
            line(ax, [x1, x1], [yb, yt], lw=0.8)
        else:
            poly(ax, [(0, yt), (x0, yt), (x0, yb), (x1, yb), (x1, yt), (10, yt), (10, yt + 0.6), (6.8, yt + 0.6),
                      (6.0, yt + 1.3), (4.0, yt + 1.3), (3.2, yt + 0.6), (0, yt + 0.6)], "cu", lw=0.6, z=3)
            text(ax, 5.0, 8.4, "CMP로 갈아냄 (32편)", size=8.8)
    save(f, P, "superfill")

    # 6. barrier와 cap
    f, ax = canvas(9.6, 4.4, (0, 20), (-1.0, 8.4))
    rect(ax, 0, -1.0, 20, 6.6, "lowk", lw=0.6)
    for a in (3.0, 11.0):
        rect(ax, a, 1.0, 6.0, 4.6, "tin", lw=0.6, z=3)
        rect(ax, a + 0.3, 1.3, 5.4, 4.3, "cu", lw=0.6, z=3.1)
        text(ax, a + 3.0, 3.2, "Cu", size=12, color="white", weight="bold")
    rect(ax, 0, 5.6, 20, 0.5, "nit", lw=0.6, z=4)
    text(ax, 0.3, 7.7, "cap (SiN / SiCN): 윗면으로 Cu가 못 나가게 + 다음 층 식각 정지", size=9.5, ha="left")
    text(ax, 1.5, 2.6, "barrier\n(TaN / Ta)", size=9, color=C["tin"], weight="bold")
    arrow(ax, 2.4, 3.3, 2.95, 3.3, color=C["tin"], lw=1.0, ms=8)
    arrow(ax, 9.3, 2.0, 10.7, 2.0, color=C["red"], lw=1.4, ms=10)
    text(ax, 10.0, 2.6, "×", size=16, color=C["red"], weight="bold")
    text(ax, 10.0, 0.0, "Cu가 절연막, Si로 퍼지면 누설 전류,\ntransistor 특성 변화", size=8.8, color=C["red"])
    arrow(ax, 11.6, 5.45, 16.4, 5.45, color=C["red"], lw=1.6, ms=10, z=8)
    arrow(ax, 17.4, 6.7, 16.2, 5.75, color=C["red"], lw=1.0, ms=8, z=8)
    text(ax, 17.4, 6.95, "EM이 주로 일어나는 곳:\nCu와 cap 사이 계면", size=8.8, color=C["red"], weight="bold", va="bottom")
    save(f, P, "barrier_cap")

    # 7. 크기 효과
    w = np.linspace(8, 200, 300)
    f, ax = plot_ax(7.4, 4.4)
    ax.plot(w, np.full_like(w, 1.68), ":", color="#555555", lw=1.4, label="Cu bulk (1.68)")
    ax.plot(w, rho_cu(w), color=C["cu"], lw=2.0, label="Cu: 표면 + 결정립 경계 산란")
    ax.plot(w, rho_eff(w), color=C["red"], lw=2.4, label="Cu: + barrier 2 nm가 자리 차지")
    ax.plot(w, rho_cu(w, rho0=7.1, lam=6.6), "--", color=PAL[2], lw=2.0, label="Ru: barrier 없이 (개념)")
    ax.set_xscale("log")
    ax.set_xticks([10, 20, 50, 100, 200])
    ax.set_xticklabels(["10", "20", "50", "100", "200"])
    ax.minorticks_off()
    ax.set_ylim(0, 20)
    ax.set_xlabel("배선 폭 (nm)")
    ax.set_ylabel("실효 비저항 (µΩ·cm)")
    ax.set_title("가늘어질수록 Cu 비저항이 커짐 (대략적인 model)", loc="left", fontsize=11)
    ax.legend(fontsize=9)
    save(f, P, "size_effect")

    # 8. Low-k 종류
    rows = [("SiO₂", 3.9, 4.2), ("FSG (SiOF)", 3.4, 3.7), ("SiCOH", 2.7, 3.0), ("다공성 SiCOH", 2.2, 2.5),
            ("air gap (공기)", 1.0, 1.0)]
    f, ax = plot_ax(7.6, 3.4)
    ax.grid(False)
    for i, (s, a, b) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.barh(y, max(b - a, 0.06), left=a - (0.03 if a == b else 0), height=0.55,
                color=[C["ox"], "#b9d7ef", C["lowk"], "#c7b2dd", "#eeeeee"][i], edgecolor="#333333", lw=0.7)
        ax.text(b + 0.08, y, f"k ≈ {a:g}" + (f" ~ {b:g}" if b != a else ""), va="center", fontsize=9.5)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=10)
    ax.set_xlim(0.8, 4.8)
    ax.set_xlabel("유전율 k")
    ax.set_title("층간 절연막 유전율 (낮을수록 배선 사이 capacitance 감소)", loc="left", fontsize=11)
    save(f, P, "lowk")

    # 9. 다공성 Low-k 손상
    f, ax = canvas(8.6, 4.0, (0, 18), (-0.6, 7.6))
    rect(ax, 0, -0.6, 18, 0.6, "nit", lw=0.5)
    rect(ax, 0, 0, 18, 6.0, "lowk", lw=0.6)
    rect(ax, 6.0, 1.0, 6.0, 5.0, "white", lw=0.7, z=3)
    rect(ax, 5.3, 1.0, 0.7, 5.0, "#9575cd", lw=0.0, z=2.5, alpha=0.75)
    rect(ax, 12.0, 1.0, 0.7, 5.0, "#9575cd", lw=0.0, z=2.5, alpha=0.75)
    rect(ax, 5.3, 0.3, 7.4, 0.7, "#9575cd", lw=0.0, z=2.5, alpha=0.75)
    rng = np.random.default_rng(5)
    for x, y in rng.uniform([0.3, 0.3], [17.7, 5.7], size=(150, 2)):
        if 5.3 < x < 12.7 and y > 0.3:
            continue
        circ(ax, x, y, 0.12, "white", ec="#7e57c2", lw=0.5, z=2.6)
    text(ax, 9.0, 3.6, "식각한 홈", size=10)
    text(ax, 2.6, 6.6, "작은 구멍이 많은 Low-k", size=9.5)
    text(ax, 14.9, 6.6, "벽 쪽 손상층", size=9.5, color="#5e35b1", weight="bold")
    arrow(ax, 14.0, 6.3, 12.5, 4.8, color="#5e35b1", lw=1.0, ms=8)
    text(ax, 15.2, 2.7, "plasma에 C가 빠지고\n수분을 머금음 → k 증가", size=8.8, color="#5e35b1", box="white")
    save(f, P, "lowk_damage")
