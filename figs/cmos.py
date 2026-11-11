"""CMOS inverter 단면 (NMOS 왼쪽, PMOS 오른쪽). 1, 2, 34, 35, 38편에서 같이 씀"""
import numpy as np
from common import C, rect, poly, text, arrow, ions, line

X0, X1 = 0.0, 24.0
STI = [(0.0, 1.0), (11.0, 13.0), (23.0, 24.0)]
ACT = [(1.0, 11.0), (13.0, 23.0)]
GATE = [(5.4, 6.6), (17.4, 18.6)]
TRD = -1.6          # trench 깊이
PADOX, NIT = 0.12, 0.6
GOX, PTOP = 0.1, 1.5
SPW, SPH = 0.45, 1.42
LDD_D, SD_D, SIL_D = 0.28, 0.65, 0.12
WELL_D = -4.2
PMD_TOP = 3.0
CT_X, CT_W = [3.0, 9.0, 15.0, 21.0], 0.7
M1 = [(2.2, 3.8, "GND"), (8.2, 15.8, "OUT"), (20.2, 21.8, "VDD")]
M1_T = 0.8
IMD_TOP = 6.0
VIA = (11.6, 12.4)
M2 = (10.0, 14.0)
PASS_T = 0.6


def conformal(ax, bumps, t, c, base=0.0, z=6.5, x0=X0, x1=X1, lw=0.7):
    """평평한 면 + 튀어나온 구조(bumps) 위에 두께 t로 고르게 덮인 막"""
    top, bot = [(x0, base + t)], [(x0, base)]
    for bx0, bx1, h in bumps:
        bot += [(bx0, base), (bx0, h), (bx1, h), (bx1, base)]
        top += [(bx0 - t, base + t), (bx0 - t, h + t), (bx1 + t, h + t), (bx1 + t, base + t)]
    top.append((x1, base + t))
    bot.append((x1, base))
    poly(ax, top + bot[::-1], c, z=z, lw=lw)


def spacer(ax, gx0, gx1, c="nit", z=6.2):
    th = np.linspace(0, np.pi / 2, 30)
    left = [(gx0, 0.0), (gx0, SPH)] + [(gx0 - SPW * np.sin(a), SPH * np.cos(a)) for a in th]
    right = [(gx1, 0.0), (gx1, SPH)] + [(gx1 + SPW * np.sin(a), SPH * np.cos(a)) for a in th]
    poly(ax, left, c, z=z, lw=0.7)
    poly(ax, right, c, z=z, lw=0.7)


def pr(ax, x0, x1, y0, h=0.9):
    rect(ax, x0, y0, x1 - x0, h, "pr", z=11)


def draw(ax, st, lab=True, size=8.5):
    """st: 단계별로 있는 것만 True"""
    g = st.get
    # 기판, well
    rect(ax, X0, -7, X1 - X0, 7, "sub", z=1, lw=0.6)
    if g("wells"):
        rect(ax, 0, WELL_D, 12, -WELL_D, "pw", z=1.2, lw=0.6)
        rect(ax, 12, WELL_D, 12, -WELL_D, "nw", z=1.2, lw=0.6)
        if lab:
            text(ax, 1.4, WELL_D + 0.45, "P-well", size=size, ha="left")
            text(ax, 22.6, WELL_D + 0.45, "N-well", size=size, ha="right")
    elif lab and not g("no_sub_label"):
        text(ax, 12, -2.6, "p형 Si 기판 (100)", size=size)

    # source/drain, LDD
    sd = g("sd") or ""
    ldd = g("ldd") or ""
    for i, ((a0, a1), (gx0, gx1)) in enumerate(zip(ACT, GATE)):
        typ = "n" if i == 0 else "p"
        if typ in sd:
            c = "np" if typ == "n" else "pp"
            rect(ax, a0, -SD_D, (gx0 - SPW + 0.1) - a0, SD_D, c, z=2.5, lw=0.6)
            rect(ax, gx1 + SPW - 0.1, -SD_D, a1 - (gx1 + SPW - 0.1), SD_D, c, z=2.5, lw=0.6)
        if typ in ldd:
            c = "nl" if typ == "n" else "pl"
            rect(ax, gx0 - SPW, -LDD_D, SPW + 0.12, LDD_D, c, z=2.6, lw=0.6)
            rect(ax, gx1 - 0.12, -LDD_D, SPW + 0.12, LDD_D, c, z=2.6, lw=0.6)
        if g("sil"):
            rect(ax, a0, -SIL_D, gx0 - SPW - a0, SIL_D, "sil", z=3, lw=0.6)
            rect(ax, gx1 + SPW, -SIL_D, a1 - gx1 - SPW, SIL_D, "sil", z=3, lw=0.6)

    # STI
    sti = g("sti")
    if sti == "trench":
        for a, b in STI:
            rect(ax, a, TRD, b - a, -TRD, "#ffffff", z=4, lw=0.8)
    elif sti == "liner":
        for a, b in STI:
            rect(ax, a, TRD, b - a, -TRD, "#ffffff", z=4, lw=0.8)
            # 측벽과 바닥에 얇은 liner
            if a > 0:
                rect(ax, a, TRD, 0.12, -TRD, "ox", z=4.1, lw=0.5)
            if b < 24:
                rect(ax, b - 0.12, TRD, 0.12, -TRD, "ox", z=4.1, lw=0.5)
            rect(ax, a, TRD, b - a, 0.12, "ox", z=4.1, lw=0.5)
    elif sti in ("fill", "cmp"):
        top = PADOX + NIT if sti == "cmp" else 1.7
        for a, b in STI:
            rect(ax, a, TRD, b - a, (PADOX + NIT) - TRD, "ox", z=4, lw=0.8)
        if sti == "fill":
            poly(ax, [(X0, PADOX + NIT), (X1, PADOX + NIT), (X1, 1.55), (23.0, 1.55), (22.6, 1.85),
                      (13.4, 1.85), (13.0, 1.55), (11.0, 1.55), (10.6, 1.85), (1.4, 1.85),
                      (1.0, 1.55), (X0, 1.55)], "ox", z=4.2, lw=0.8)
    elif sti == "final":
        for a, b in STI:
            rect(ax, a, TRD, b - a, -TRD, "ox", z=4, lw=0.8)

    # pad 산화막 + 질화막
    pad = g("pad")
    if pad == "blanket":
        rect(ax, X0, 0, X1 - X0, PADOX, "ox", z=5, lw=0.6)
        rect(ax, X0, PADOX, X1 - X0, NIT, "nit", z=5, lw=0.6)
    elif pad == "active":
        for a, b in ACT:
            rect(ax, a, 0, b - a, PADOX, "ox", z=5, lw=0.6)
            rect(ax, a, PADOX, b - a, NIT, "nit", z=5, lw=0.6)
    elif pad == "padox":
        for a, b in ACT:
            rect(ax, a, 0, b - a, PADOX, "ox", z=5, lw=0.6)

    # gate 산화막, poly
    if g("gox") == "active":
        for a, b in ACT:
            rect(ax, a, 0, b - a, GOX, "ox", z=5, lw=0.6)
    if g("poly") == "blanket":
        rect(ax, X0, GOX, X1 - X0, PTOP - GOX, "poly", z=6, lw=0.7)
    if g("gates"):
        for gx0, gx1 in GATE:
            rect(ax, gx0, 0, gx1 - gx0, GOX, "ox", z=6, lw=0.6)
            rect(ax, gx0, GOX, gx1 - gx0, PTOP - GOX, "poly", z=6, lw=0.7)
            if g("sil"):
                rect(ax, gx0, PTOP, gx1 - gx0, 0.16, "sil", z=6.3, lw=0.6)

    # spacer
    if g("spacer_blanket"):
        conformal(ax, [(a, b, PTOP) for a, b in GATE], 0.42, "nit", z=6.5)
    if g("spacer"):
        for gx0, gx1 in GATE:
            spacer(ax, gx0, gx1)

    # salicide용 금속
    if g("metal_blanket"):
        conformal(ax, [(a - SPW, b + SPW, PTOP) for a, b in GATE], 0.16, "#7f7f7f", z=6.8)
    if g("metal_left"):
        # 반응 안 한 금속: STI, spacer 위에만 남음
        for a, b in STI:
            rect(ax, a, 0, b - a, 0.16, "#7f7f7f", z=6.8, lw=0.6)
        for gx0, gx1 in GATE:
            for xs in [(gx0 - SPW, gx0), (gx1, gx1 + SPW)]:
                rect(ax, xs[0], 0.0, xs[1] - xs[0], 0.12, "#7f7f7f", z=6.9, lw=0.5)

    # PMD (층간 절연막)
    pmd = g("pmd")
    if pmd == "bumpy":
        top = [(X0, 3.4)]
        for gx0, gx1 in GATE:
            top += [(gx0 - 1.3, 3.4), (gx0 - 0.5, 4.0), (gx1 + 0.5, 4.0), (gx1 + 1.3, 3.4)]
        top += [(X1, 3.4)]
        poly(ax, [(X0, 0)] + top + [(X1, 0)], "ox", z=3.5, lw=0.7)
    elif pmd:
        rect(ax, X0, 0, X1 - X0, PMD_TOP, "ox", z=3.5, lw=0.7)

    ct = g("ct")
    if ct == "hole":
        for x in CT_X:
            rect(ax, x - CT_W / 2, 0, CT_W, PMD_TOP, "#ffffff", z=7, lw=0.7)
    elif ct in ("fill", "plug"):
        for x in CT_X:
            rect(ax, x - CT_W / 2, 0, CT_W, PMD_TOP, "tin", z=7, lw=0.6)
            rect(ax, x - CT_W / 2 + 0.09, 0.09, CT_W - 0.18, PMD_TOP - 0.09, "w", z=7.1, lw=0.5)
        if ct == "fill":
            rect(ax, X0, PMD_TOP, X1 - X0, 0.08, "tin", z=7, lw=0.5)
            rect(ax, X0, PMD_TOP + 0.08, X1 - X0, 0.45, "w", z=7, lw=0.6)

    if g("m1"):
        imd_top = IMD_TOP if g("m2") else PMD_TOP + M1_T
        rect(ax, X0, PMD_TOP, X1 - X0, imd_top - PMD_TOP, "lowk", z=3.4, lw=0.7)
        for a, b, name in M1:
            rect(ax, a, PMD_TOP, b - a, M1_T, "cu", z=8, lw=0.7)
            if lab:
                text(ax, (a + b) / 2, PMD_TOP + M1_T / 2, name, size=size - 0.5, color="white",
                     weight="bold", z=21)
    if g("m2"):
        rect(ax, VIA[0], PMD_TOP + M1_T, VIA[1] - VIA[0], 1.0, "cu", z=8, lw=0.7)
        rect(ax, M2[0], PMD_TOP + M1_T + 1.0, M2[1] - M2[0], 0.8, "cu", z=8, lw=0.7)
        if lab:
            text(ax, (M2[0] + M2[1]) / 2, PMD_TOP + M1_T + 1.4, "M2", size=size - 0.5,
                 color="white", weight="bold", z=21)
        if g("pass"):
            rect(ax, X0, IMD_TOP, X1 - X0, PASS_T, "nit", z=8.5, lw=0.7)

    # PR, ion
    for (x0, x1, y0) in g("pr", []):
        pr(ax, x0, x1, y0, g("pr_h", 0.9))
    if g("ions"):
        xs_rng, y0, label = g("ions")
        xs = []
        for a, b in xs_rng:
            xs += list(np.arange(a + 0.5, b, 1.0))
        ions(ax, xs, y0 + 1.4, y0 + 0.05, color="red", lw=1.0, ms=7)
        if lab and label:
            text(ax, 12, y0 + 1.8, label, size=size, color=C["red"], weight="bold", box="white")

    if g("etch_arrows"):
        xs_rng, y0 = g("etch_arrows")
        for a, b in xs_rng:
            for x in np.arange(a + 0.25, b, 0.5):
                arrow(ax, x, y0 + 1.0, x, y0 + 0.2, color="#555555", lw=0.9, ms=6)

    if lab and g("dev_labels"):
        text(ax, 6.0, g("dev_y", 2.6), "NMOS", size=size + 1, weight="bold")
        text(ax, 18.0, g("dev_y", 2.6), "PMOS", size=size + 1, weight="bold")


# 34편: 기판 ~ gate
A = [
    ("① p형 Si 기판 준비, 세정", dict()),
    ("② pad 산화막 + 질화막", dict(pad="blanket")),
    ("③ Active photo (소자 자리에 PR)", dict(pad="blanket", pr=[(1.0, 11.0, 0.72), (13.0, 23.0, 0.72)])),
    ("④ 질화막·산화막·Si 식각 → trench", dict(pad="active", sti="trench",
                                         pr=[(1.0, 11.0, 0.72), (13.0, 23.0, 0.72)])),
    ("⑤ PR 제거, liner 산화", dict(pad="active", sti="liner")),
    ("⑥ HDP 산화막으로 trench 채움", dict(pad="active", sti="fill")),
    ("⑦ CMP (질화막에서 멈춤)", dict(pad="active", sti="cmp")),
    ("⑧ 질화막, pad 산화막 제거 → STI 완성", dict(sti="final")),
    ("⑨ N-well photo + 인(P) 주입", dict(sti="final", pr=[(0.0, 12.0, 0.0)],
                                      ions=([(12.0, 24.0)], 0.0, "P⁺ ion (높은 energy)"))),
    ("⑩ P-well photo + 붕소(B) 주입", dict(sti="final", pr=[(12.0, 24.0, 0.0)],
                                       ions=([(0.0, 12.0)], 0.0, "B⁺ ion"))),
    ("⑪ 열처리로 well 완성", dict(sti="final", wells=True)),
    ("⑫ 문턱전압(Vt) 조절 주입 (NMOS 예)", dict(sti="final", wells=True, pr=[(12.0, 24.0, 0.0)],
                                             ions=([(0.0, 12.0)], 0.0, "낮은 energy, 적은 dose"))),
    ("⑬ gate 산화 (건식, 얇게)", dict(sti="final", wells=True, gox="active")),
    ("⑭ poly-Si 증착 (LPCVD)", dict(sti="final", wells=True, gox="active", poly="blanket")),
    ("⑮ gate photo", dict(sti="final", wells=True, gox="active", poly="blanket",
                       pr=[(5.4, 6.6, 1.5), (17.4, 18.6, 1.5)])),
    ("⑯ poly 식각, PR 제거 → gate", dict(sti="final", wells=True, gates=True)),
]

_base = dict(sti="final", wells=True, gates=True)


def _s(**kw):
    d = dict(_base)
    d.update(kw)
    return d


# 35편: LDD ~ 배선
B = [
    ("① NLDD: PMOS 가리고 비소(As) 주입", _s(ldd="n", pr=[(12.0, 24.0, 0.0)], pr_h=1.9,
                                         ions=([(0.0, 12.0)], 1.9, "As⁺ (얕게, 적게)"))),
    ("② PLDD: NMOS 가리고 BF₂ 주입", _s(ldd="np", pr=[(0.0, 12.0, 0.0)], pr_h=1.9,
                                      ions=([(12.0, 24.0)], 1.9, "BF₂⁺"))),
    ("③ spacer용 질화막 증착", _s(ldd="np", spacer_blanket=True)),
    ("④ etch back (이방성 식각) → spacer", _s(ldd="np", spacer=True)),
    ("⑤ N⁺ S/D: PMOS 가리고 As 주입", _s(ldd="np", spacer=True, sd="n", pr=[(12.0, 24.0, 0.0)],
                                      pr_h=1.9, ions=([(0.0, 12.0)], 1.9, "As⁺ (많이)"))),
    ("⑥ P⁺ S/D: NMOS 가리고 B 주입 → RTA", _s(ldd="np", spacer=True, sd="np",
                                          pr=[(0.0, 12.0, 0.0)], pr_h=1.9,
                                          ions=([(12.0, 24.0)], 1.9, "B⁺ / BF₂⁺ (많이)"))),
    ("⑦ 금속(Co, Ni) 얇게 증착", _s(ldd="np", spacer=True, sd="np", metal_blanket=True)),
    ("⑧ 1차 열처리 → Si 닿은 곳만 silicide", _s(ldd="np", spacer=True, sd="np", sil=True,
                                           metal_left=True)),
    ("⑨ 반응 안 한 금속 제거 + 2차 열처리", _s(ldd="np", spacer=True, sd="np", sil=True)),
    ("⑩ 층간 절연막(PMD) 증착", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="bumpy")),
    ("⑪ CMP로 평탄화", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="flat")),
    ("⑫ contact photo + 식각", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="flat", ct="hole")),
    ("⑬ Ti/TiN + W 증착", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="flat", ct="fill")),
    ("⑭ W CMP → contact plug", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="flat",
                                ct="plug")),
    ("⑮ Metal1 (Cu damascene)", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="flat", ct="plug",
                              m1=True)),
    ("⑯ Via1 + Metal2 + 보호막", _s(ldd="np", spacer=True, sd="np", sil=True, pmd="flat",
                                 ct="plug", m1=True, m2=True, **{"pass": True})),
]

FINAL = B[-1][1]
FEOL_DONE = _s(ldd="np", spacer=True, sd="np", sil=True)
