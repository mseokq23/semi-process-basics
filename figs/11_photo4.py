import numpy as np
from common import *

P = 11


def aerial(pitch, cutoff=1.0, duty=0.5, n=4096, periods=4, phase=False):
    """1D 결맞음(coherent) 결상. 길이 단위 = λ/NA, 투과부 = 1"""
    L = pitch * periods
    x = np.linspace(0, L, n, endpoint=False)
    m = ((x % pitch) < pitch * duty).astype(complex)
    if phase:  # 이웃 창마다 위상 180도
        m *= np.where((x // pitch) % 2 == 0, 1, -1)
    F = np.fft.fft(m)
    fx = np.fft.fftfreq(n, d=L / n)
    F[np.abs(fx) > cutoff] = 0
    E = np.fft.ifft(F)
    return x, m, E


if __name__ == "__main__":
    # 1. 회절과 NA
    f, axs = panels(2, 2, 5.6, 5.0, (0, 10), (0, 10),
                    titles=["pitch가 클 때: ±1차가 lens 안으로 → pattern이 맺힘",
                            "pitch가 작을 때: ±1차가 lens 밖 → 0차만 → pattern 없음"], size=10.5)
    for k, ax in enumerate(axs):
        pitch = 1.0 if k == 0 else 0.5
        rect(ax, 1.0, 8.4, 8.0, 0.25, "#e3f2fd", lw=0.6)
        for x0 in np.arange(1.0, 9.0, pitch):
            rect(ax, x0, 8.4, pitch / 2, 0.12, "#424242", lw=0.2)
        ax.add_patch(Ellipse((5.0, 5.0), 5.6, 0.8, fc="#e1f5fe", ec="#4fc3f7", lw=1.2, zorder=4))
        rect(ax, 1.5, 0.6, 7.0, 0.5, "si", lw=0.6)
        ang = np.deg2rad(22 if k == 0 else 50)
        for m in (-1, 0, 1):
            x_lens = 5.0 + np.tan(m * ang) * 3.4
            col = "#8e44ad" if m == 0 else C["blue"]
            if abs(x_lens - 5.0) < 2.7:
                line(ax, [5.0, x_lens], [8.4, 5.0], color=col, lw=1.6)
                line(ax, [x_lens, 5.0], [5.0, 1.1], color=col, lw=1.6)
            else:
                xe = 5.0 + np.tan(m * ang) * 2.3
                line(ax, [5.0, xe], [8.4, 6.1], color=col, lw=1.6, ls="--")
                text(ax, xe + 0.25 * m, 5.85, "×", size=15, color=C["red"], weight="bold")
            if m != 0:
                text(ax, 5.0 + np.tan(m * ang) * 1.3 + 0.35 * m, 7.3, f"{m:+d}차", size=9.5, color=col)
        text(ax, 5.0, 7.3, "0차", size=9.5, color="#8e44ad")
        text(ax, 5.0, 9.4, "mask (pitch p)", size=9.5)
        text(ax, 8.6, 5.0, "lens", size=9.5, ha="left")
    text(axs[0], 5.0, 0.05, "sinθ = λ / p : pitch가 작을수록 크게 꺾임", size=9.5, va="bottom")
    text(axs[1], 5.0, 0.05, "lens가 받을 수 있는 최대 각도 = NA", size=9.5, va="bottom")
    save(f, P, "diffraction_na")

    # 2. pitch에 따른 공중 image
    f, axs = plt.subplots(1, 3, figsize=(13.5, 3.6), sharey=True)
    for ax, p in zip(axs, (3.5, 1.4, 0.9)):
        x, m, E = aerial(p)
        I = np.abs(E) ** 2
        for k in range(4):
            ax.axvspan(k * p, k * p + p / 2, color="#e3f2fd", zorder=0)
        ax.plot(x, I, color=PAL[1], lw=2)
        ax.set_title(f"pitch = {p} × λ/NA", loc="left", fontsize=11)
        ax.set_xlabel("위치 (λ/NA 단위)")
        ax.set_ylim(0, 1.25)
        ax.grid(alpha=0.25)
    axs[0].set_ylabel("빛 세기")
    axs[2].text(1.8, 0.6, "0차만 통과\n→ 세기가 평평\n(pattern 없음)", ha="center", fontsize=10, color=PAL[1])
    plt.suptitle("파란 띠 = mask에서 빛이 통과하는 곳, 빨간 선 = wafer에 맺히는 빛 (결맞음 조명 계산)",
                 fontsize=10.5, y=1.02)
    plt.tight_layout()
    save(f, P, "aerial_pitch")

    # 3. 해상도 vs NA
    k1 = 0.3
    f, ax = plot_ax(7.4, 4.4)
    NA = np.linspace(0.2, 1.4, 200)
    for (name, lam, c) in [("i-line 365 nm", 365, PAL[4]), ("KrF 248 nm", 248, PAL[3]),
                           ("ArF 193 nm", 193, PAL[2]), ("EUV 13.5 nm", 13.5, PAL[0])]:
        na = NA if lam > 20 else np.linspace(0.2, 0.6, 50)
        ax.plot(na, k1 * lam / na, color=c, lw=2, label=name)
    pts = [("i-line", 365, 0.62), ("KrF", 248, 0.86), ("ArF 건식", 193, 0.93), ("ArF 액침", 193, 1.35),
           ("EUV", 13.5, 0.33), ("High-NA EUV", 13.5, 0.55)]
    for n, lam, na in pts:
        r = k1 * lam / na
        ax.plot(na, r, "ko", ms=5)
        ax.text(na + 0.02, r * 1.12, f"{n}\n{r:.0f} nm", fontsize=8.6)
    ax.set_yscale("log")
    ax.set_xlabel("NA")
    ax.set_ylabel("해상도 R (nm)")
    ax.set_title("R = k₁·λ / NA  (k₁ = 0.3으로 계산)", loc="left")
    ax.legend(fontsize=9, loc="upper right")
    save(f, P, "resolution_na")

    # 4. 초점심도
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.4), gridspec_kw=dict(width_ratios=[1, 1.1]))
    canvas(0, 0, (0, 10), (0, 9), ax=ax1)
    ax1.set_title("DoF: 초점이 맞았다고 볼 수 있는 높이 범위", fontsize=11, loc="left")
    for sgn in (-1, 1):
        line(ax1, [5.0 + sgn * 3.0, 5.0 + sgn * 0.25], [8.5, 4.6], color="#8e44ad", lw=1.2)
        line(ax1, [5.0 + sgn * 0.25, 5.0 + sgn * 3.0], [3.4, -0.5 + 0.5], color="#8e44ad", lw=1.2)
    line(ax1, [4.75, 4.75], [3.4, 4.6], color="#8e44ad", lw=1.2)
    line(ax1, [5.25, 5.25], [3.4, 4.6], color="#8e44ad", lw=1.2)
    ax1.axhspan(3.4, 4.6, xmin=0.05, xmax=0.95, color="#c8e6c9", alpha=0.6)
    vdim(ax1, 8.6, 3.4, 4.6, "DoF", size=10)
    rect(ax1, 0.8, 3.55, 3.0, 0.5, "pr", lw=0.5)
    text(ax1, 2.3, 3.0, "PR 두께 + wafer 단차가\n이 범위 안에 들어와야 함", size=9)
    canvas(0, 0, (0, 10), (0, 9), ax=ax1)
    NA = np.linspace(0.5, 1.0, 100)
    lam = 193
    R = 0.3 * lam / NA
    DoF = 1.0 * lam / NA ** 2
    ax2.plot(NA, R, color=PAL[0], lw=2.2, label="해상도 R = 0.3·λ/NA")
    ax2.plot(NA, DoF, color=PAL[1], lw=2.2, label="DoF = λ/NA²")
    ax2.set_xlabel("NA (ArF 193 nm, 건식)")
    ax2.set_ylabel("nm")
    ax2.grid(alpha=0.25)
    ax2.legend()
    ax2.set_title("NA를 키우면 R은 좋아지지만 DoF가 더 빨리 줄어듦", fontsize=11, loc="left")
    plt.tight_layout()
    save(f, P, "dof")

    # 5. Bossung 곡선, 공정 창 (개념 model)
    fz = np.linspace(-0.16, 0.16, 161)
    Es = np.linspace(21, 29, 161)

    def cd(E, fo):
        return 45 - 1.6 * (E - 25) - 2200 * (E - 24.0) / 25 * fo ** 2 - 9000 * fo ** 4

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.4))
    for E, c in zip([22, 24, 25, 26, 28], PAL):
        ax1.plot(fz * 1e3, cd(E, fz), color=c, lw=2, label=f"{E} mJ/cm²")
    ax1.axhspan(45 * 0.9, 45 * 1.1, color="#c8e6c9", alpha=0.5)
    ax1.set_xlabel("초점 위치 (nm)")
    ax1.set_ylabel("선폭 CD (nm)")
    ax1.set_title("Bossung 곡선 (노광량별 CD - 초점)", fontsize=11, loc="left")
    ax1.legend(fontsize=8.6, ncol=2)
    ax1.grid(alpha=0.25)
    FF, EE = np.meshgrid(fz, Es)
    CD = cd(EE, FF)
    ok = (CD > 40.5) & (CD < 49.5)
    ax2.contourf(FF * 1e3, EE, ok, levels=[0.5, 1.5], colors=["#c8e6c9"])
    ax2.contour(FF * 1e3, EE, CD, levels=[40.5, 49.5], colors=[PAL[1], PAL[0]], linewidths=1.5)
    best = None
    for h in np.linspace(0.02, 0.16, 71):
        for e0 in np.linspace(22, 28, 121):
            for de in np.linspace(0.2, 4, 77):
                sel = (np.abs(FF) <= h) & (EE >= e0 - de) & (EE <= e0 + de)
                if sel.any() and ok[sel].all():
                    area = h * de / 25
                    if best is None or area > best[0]:
                        best = (area, h, e0, de)
    _, h, e0, de = best
    rect(ax2, -h * 1e3, e0 - de, 2 * h * 1e3, 2 * de, "none", ec="#333333", lw=1.4, z=6)
    ax2.text(0, e0 + de + 0.25, f"DoF ≈ {2 * h * 1e3:.0f} nm,  EL ≈ {200 * de / e0:.0f} %", ha="center", fontsize=9.5)
    ax2.set_xlabel("초점 위치 (nm)")
    ax2.set_ylabel("노광량 (mJ/cm²)")
    ax2.set_title("공정 창: CD ±10 % 안에 드는 영역", fontsize=11, loc="left")
    plt.tight_layout()
    save(f, P, "process_window")
    print("window: DoF %.0f nm, EL %.1f %%, center dose %.2f" % (2 * h * 1e3, 200 * de / e0, e0))
