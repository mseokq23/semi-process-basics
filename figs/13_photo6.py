import numpy as np
from common import *

P = 13

# 1. EUV 장비 빛 경로
f, ax = canvas(12, 5.6, (0, 24), (0, 11))
rect(ax, 0.3, 0.3, 23.4, 10.4, "#f7f9fb", ec="#90a4ae", lw=1.2)
text(ax, 12, 10.2, "전부 진공 안 (EUV는 공기에도 흡수됨)", size=10, color="#607d8b")
box(ax, 0.8, 1.0, 3.2, 1.6, "CO₂ 레이저", fc="#ffe0b2", size=9.5)
arrow(ax, 4.0, 1.8, 5.6, 3.6, color="orange", lw=1.8)
for y in np.linspace(5.6, 3.0, 6):
    circ(ax, 5.9, y, 0.12, "#78909c", lw=0.3)
ax.add_patch(Circle((5.9, 4.0), 0.45, fc="#fff59d", ec=C["orange"], lw=1.2, zorder=6))
text(ax, 5.9, 6.3, "주석(Sn) 방울", size=9)
text(ax, 7.4, 3.3, "플라즈마 → 13.5 nm 빛", size=9, color=C["orange"], ha="left")
ax.add_patch(Arc((5.2, 4.0), 2.6, 4.0, theta1=100, theta2=260, color="#455a64", lw=3, zorder=5))
text(ax, 3.2, 6.6, "집광 거울", size=9)
pts = [(6.3, 4.2), (9.0, 7.8), (11.5, 6.4), (13.8, 8.6), (16.4, 5.0), (18.6, 7.0), (20.6, 3.6), (22.0, 2.2)]
for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
    arrow(ax, x0, y0, x1, y1, color="purple", lw=1.4, ms=9)
for (x, y) in pts[1:3]:
    rect(ax, x - 0.6, y - 0.12, 1.2, 0.24, "#455a64", lw=0)
text(ax, 10.2, 8.6, "조명 거울", size=9)
rect(ax, 13.0, 8.7, 1.6, 0.35, "#5e35b1", lw=0.5)
text(ax, 13.8, 9.4, "반사형 마스크", size=9.5, weight="bold")
for (x, y) in pts[4:7]:
    rect(ax, x - 0.6, y - 0.12, 1.2, 0.24, "#455a64", lw=0)
text(ax, 18.6, 8.0, "투영 거울 (여러 장)", size=9)
rect(ax, 20.8, 1.0, 2.6, 0.4, "si", lw=0.6)
text(ax, 22.1, 0.55, "웨이퍼", size=9)
text(ax, 12.5, 2.0, "렌즈 대신 거울로만 빛을 보냄\n거울 한 장 반사율 약 70 % → 여러 번 반사하면 많이 줄어듦",
     size=9.5, box="white")
save(f, P, "euv_system")

# 2. Mo/Si 다층막 반사율 (특성 행렬)
n_si = 0.99888 - 0.00183j
n_mo = 0.92108 - 0.00644j


def reflect(lam, N=40, d=6.9, gamma=0.4, theta_deg=6.0):
    th0 = np.deg2rad(theta_deg)
    s0 = np.sin(th0)
    layers = []
    for _ in range(N):
        layers += [(n_si, d * (1 - gamma)), (n_mo, d * gamma)]
    M = np.eye(2, dtype=complex)
    for n, t in layers:
        ct = np.sqrt(1 - (s0 / n) ** 2)
        eta = n * ct
        dl = 2 * np.pi * n * t * ct / lam
        M = M @ np.array([[np.cos(dl), 1j * np.sin(dl) / eta], [1j * eta * np.sin(dl), np.cos(dl)]])
    ns = n_si
    eta_s = ns * np.sqrt(1 - (s0 / ns) ** 2)
    eta0 = np.cos(th0)
    B, Cc = M @ np.array([1, eta_s])
    r = (eta0 * B - Cc) / (eta0 * B + Cc)
    return abs(r) ** 2


lams = np.linspace(12.6, 14.4, 400)
R = np.array([reflect(l) for l in lams])
k = np.argmax(R)
print("peak R = %.3f at %.2f nm, FWHM = %.2f nm" % (R[k], lams[k], np.ptp(lams[R > R[k] / 2])))
Rn = [reflect(13.5, N=n) for n in range(1, 61)]
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
ax1.plot(lams, R * 100, color=PAL[4], lw=2.2)
ax1.set_xlabel("파장 (nm)")
ax1.set_ylabel("반사율 (%)")
ax1.set_title(f"Mo/Si 40쌍: 최대 약 {R[k] * 100:.0f} % ({lams[k]:.2f} nm)", loc="left", fontsize=11)
ax1.grid(alpha=0.25)
ax2.plot(range(1, 61), np.array(Rn) * 100, "o-", ms=3, color=PAL[0])
ax2.set_xlabel("Mo/Si 쌍 수")
ax2.set_ylabel("13.5 nm 반사율 (%)")
ax2.set_title("층이 쌓일수록 반사가 보강되다가 포화", loc="left", fontsize=11)
ax2.grid(alpha=0.25)
plt.tight_layout()
save(f, P, "multilayer")

# 3. 반사형 마스크
f, ax = canvas(10, 4.4, (0, 20), (0, 9))
rect(ax, 1.0, 0.4, 18.0, 2.0, "#eceff1", lw=0.8)
text(ax, 10.0, 1.4, "저열팽창 유리 기판", size=9.5)
for i in range(16):
    rect(ax, 1.0, 2.4 + i * 0.18, 18.0, 0.18, "#7986cb" if i % 2 == 0 else "#e8eaf6", lw=0)
rect(ax, 1.0, 2.4, 18.0, 2.88, "none", lw=0.8)
text(ax, 19.3, 3.8, "Mo/Si\n40쌍", size=9, ha="left")
rect(ax, 1.0, 5.28, 18.0, 0.15, "#ffb74d", lw=0.4)
text(ax, 19.3, 5.35, "캡핑층", size=8.5, ha="left")
for x0, x1 in [(1.0, 4.5), (7.5, 9.5), (12.5, 15.5)]:
    rect(ax, x0, 5.43, x1 - x0, 1.2, "#37474f", lw=0.6)
text(ax, 3.0, 6.0, "흡수체", size=9, color="white")
for x0 in (5.0, 10.0, 16.0):
    line(ax, [x0 - 0.45 * 3.2, x0], [8.7, 5.43], color="#8e44ad", lw=1.4)
    arrow(ax, x0, 5.43, x0 + 0.45 * 3.2, 8.7, color="purple", lw=1.4, ms=9)
text(ax, 10.0, 8.7, "약 6° 비스듬히 들어가서 반사 (그림은 각도를 과장함)", size=9.5, color=C["purple"], box="white")
text(ax, 10.0, -0.2, "흡수체 두께 때문에 한쪽에 그림자가 생김 → 마스크 3D 효과", size=9.5, va="bottom")
save(f, P, "euv_mask")

# 4. 광자 수 차이 (확률적 결함)
rng = np.random.default_rng(7)
Np = 120
x = np.arange(Np)
X, Y = np.meshgrid(x, x)
holes = np.zeros((Np, Np))
for cx in (30, 90):
    for cy in (30, 90):
        holes += np.exp(-(((X - cx) ** 2 + (Y - cy) ** 2) / (2 * 11.0 ** 2)) ** 2)
holes = np.clip(holes, 0, 1)
dose_area = 30e-3 / 1e14  # 30 mJ/cm² → J/nm²
ev = 1.602e-19
dens = {"ArF (6.4 eV)": dose_area / (6.42 * ev), "EUV (92 eV)": dose_area / (91.8 * ev)}
for k_, v in dens.items():
    print(f"{k_}: {v:.1f} photons/nm^2, {v * 100:.0f} per 10x10 nm")
f, axs = plt.subplots(1, 2, figsize=(11, 5.6))
for ax, (name, d) in zip(axs, dens.items()):
    counts = rng.poisson(d * holes)
    ker = np.exp(-((np.fft.fftfreq(Np)[None, :]) ** 2 + (np.fft.fftfreq(Np)[:, None]) ** 2) * 2 * (np.pi * 2.0) ** 2)
    sm = np.real(np.fft.ifft2(np.fft.fft2(counts / d) * ker))
    ax.imshow(counts / d, cmap="magma", origin="lower", vmin=0, vmax=1.6)
    ax.contour(X, Y, sm, levels=[0.5], colors=["#4fc3f7"], linewidths=1.6)
    ax.set_title(f"{name}: 1 nm²당 광자 약 {d:.0f}개", fontsize=11, loc="left")
    ax.set_xticks([])
    ax.set_yticks([])
plt.suptitle("같은 30 mJ/cm²라도 EUV는 광자 수가 약 14배 적음 → 컨택 홀 가장자리가 울퉁불퉁 (하늘색: PR 경계 예시)",
             fontsize=10.5, y=0.98)
plt.tight_layout()
save(f, P, "stochastic")

# 5. 포토 불량 모음
tt = ["① 브리지 (선끼리 붙음)", "② 패턴 무너짐", "③ 스컴 (바닥 잔막)", "④ PR 들뜸 (접착 불량)",
      "⑤ LER (가장자리 거칠기)", "⑥ 파티클로 패턴 없어짐"]
f, axs = panels(6, 3, 3.6, 2.8, (0, 10), (0, 6), titles=tt, size=10.5)
a = axs
for ax in (a[1], a[2], a[3]):
    rect(ax, 0.3, 0.3, 9.4, 1.2, "si", lw=0.6)
for x0 in (1.0, 4.0, 7.0):
    rect(a[0], x0, 0.6, 1.8, 4.8, "pr", lw=0.6)
rect(a[0], 2.8, 2.6, 1.2, 0.8, "pr", lw=0, z=3)
text(a[0], 5.0, 5.7, "위에서 본 모습", size=8.5, color="#666666")
for k, x0 in enumerate((1.4, 3.8, 6.2)):
    if k == 1:
        poly(a[1], [(x0, 1.5), (x0 + 0.8, 1.5), (x0 + 2.6, 4.2), (x0 + 1.9, 4.6)], "pr", lw=0.6)
    else:
        rect(a[1], x0, 1.5, 0.8, 3.6, "pr", lw=0.6)
text(a[1], 5.0, 5.6, "높고 가는 패턴 + 건조할 때 모세관력", size=8.6)
for x0 in (0.8, 4.4, 8.0):
    rect(a[2], x0, 1.5, 1.2, 2.6, "pr", lw=0.6)
rect(a[2], 2.0, 1.5, 2.4, 0.3, "pr", lw=0.3, alpha=0.7)
rect(a[2], 5.6, 1.5, 2.4, 0.18, "pr", lw=0.3, alpha=0.7)
poly(a[3], [(1.0, 1.5), (4.0, 1.5), (4.0, 2.9), (1.0, 2.9)], "pr", lw=0.6)
poly(a[3], [(5.6, 1.9), (8.8, 1.5), (9.0, 2.9), (5.8, 3.3)], "pr", lw=0.6)
text(a[3], 7.3, 4.3, "현상액이 계면으로 스며듦", size=8.6)
rng = np.random.default_rng(1)
ys = np.linspace(0.6, 5.4, 80)
for x0 in (1.5, 5.5):
    xl = x0 + 0.15 * rng.standard_normal(80).cumsum() * 0.3
    xr = x0 + 2.2 + 0.15 * rng.standard_normal(80).cumsum() * 0.3
    poly(a[4], list(zip(xl, ys)) + list(zip(xr[::-1], ys[::-1])), "pr", lw=0.6)
for x0 in (1.0, 4.0, 7.0):
    rect(a[5], x0, 0.6, 1.8, 4.8, "pr", lw=0.6)
circ(a[5], 5.0, 3.0, 1.15, "#ffffff", ec="#ffffff", z=3)
circ(a[5], 5.0, 3.0, 0.35, "#6d4c41", lw=0.5, z=4)
text(a[5], 5.0, 5.7, "위에서 본 모습", size=8.5, color="#666666")
save(f, P, "defects")
