"""그림 공통 설정과 그리기 함수"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Polygon, FancyArrowPatch, FancyBboxPatch,
                                Circle, Ellipse, Wedge, Arc)
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "img")

plt.rcParams.update({
    "font.family": ["Noto Sans CJK KR", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "mathtext.fontset": "dejavusans",
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.12,
    "figure.facecolor": "white",
})

# 재료 색 (모든 편에서 같은 색을 씀)
C = dict(
    si="#d5dbe1", ox="#a8d8f0", nit="#b5d99c", pr="#f2a7bb", poly="#f6c667",
    al="#b9c0c7", cu="#d58f5a", w="#7f8c99", tin="#8d6e63", sil="#9b88cf",
    np="#5b9bd5", pp="#e06c6c", nl="#9cc3e8", pl="#f0a8a8",
    nw="#dceaf7", pw="#f9e0e0", lowk="#dccbe8", hk="#ffd966", mg="#6d7f8f",
    epi="#c9d9c0", box="#9fc9e0", sic="#c8c0a8", emc="#4a4a4a", sub="#cfd6dc",
    ink="#222222", red="#d9534f", blue="#2f6fb0", green="#3c8d40",
    gray="#888888", orange="#e69138", purple="#7b5ea7", light="#f4f4f4",
)
NAME = dict(si="Si", ox="SiO₂", nit="Si₃N₄", pr="PR", poly="poly-Si", al="Al", cu="Cu",
            w="W", tin="Ti/TiN", sil="silicide", np="n⁺", pp="p⁺", nl="n⁻ (LDD)",
            pl="p⁻ (LDD)", nw="N-well", pw="P-well", lowk="Low-k", hk="High-k",
            epi="epi층", box="BOX (SiO₂)")
PAL = ["#2f6fb0", "#d9534f", "#3c8d40", "#e69138", "#7b5ea7", "#555555", "#17a2b8"]
EC = "#333333"


def canvas(w, h, xlim, ylim, ax=None):
    """축 없는 그림판. 좌표는 데이터 단위, 가로세로 비율 1:1"""
    if ax is None:
        f, ax = plt.subplots(figsize=(w, h))
    else:
        f = ax.figure
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return f, ax


def panels(n, ncols, w, h, xlim, ylim, titles=None, size=10.5):
    """단계별 단면을 여러 칸으로 그릴 때"""
    nrows = int(np.ceil(n / ncols))
    f, axs = plt.subplots(nrows, ncols, figsize=(w * ncols, h * nrows))
    axs = np.atleast_1d(axs).ravel()
    for i, ax in enumerate(axs):
        canvas(0, 0, xlim, ylim, ax=ax)
        if i >= n:
            ax.set_visible(False)
        elif titles:
            ax.set_title(titles[i], fontsize=size, loc="left")
    return f, axs[:n]


def rect(ax, x, y, w, h, c, ec=EC, lw=0.8, z=2, hatch=None, alpha=1.0, **kw):
    col = C.get(c, c)
    p = Rectangle((x, y), w, h, fc=col, ec=ec, lw=lw, zorder=z, hatch=hatch, alpha=alpha, **kw)
    ax.add_patch(p)
    return p


def poly(ax, pts, c, ec=EC, lw=0.8, z=2, hatch=None, alpha=1.0, closed=True, **kw):
    col = C.get(c, c)
    p = Polygon(pts, closed=closed, fc=col, ec=ec, lw=lw, zorder=z, hatch=hatch, alpha=alpha, **kw)
    ax.add_patch(p)
    return p


def circ(ax, x, y, r, c, ec=EC, lw=0.8, z=3, **kw):
    p = Circle((x, y), r, fc=C.get(c, c), ec=ec, lw=lw, zorder=z, **kw)
    ax.add_patch(p)
    return p


def text(ax, x, y, s, size=10, ha="center", va="center", color=None, weight=None, z=20,
         box=None, **kw):
    bbox = None
    if box:
        bbox = dict(boxstyle="round,pad=0.25", fc=box, ec="none", alpha=0.9)
    return ax.text(x, y, s, fontsize=size, ha=ha, va=va, color=color or C["ink"],
                   fontweight=weight, zorder=z, bbox=bbox, **kw)


def arrow(ax, x0, y0, x1, y1, color=None, lw=1.4, ms=12, style="-|>", z=15, ls="-", **kw):
    a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=ms,
                        color=C.get(color, color) if color else C["ink"], lw=lw, zorder=z,
                        linestyle=ls, shrinkA=0, shrinkB=0, **kw)
    ax.add_patch(a)
    return a


def line(ax, xs, ys, color=None, lw=1.0, z=12, ls="-", **kw):
    return ax.plot(xs, ys, color=C.get(color, color) if color else C["ink"], lw=lw,
                   zorder=z, ls=ls, **kw)


def box(ax, x, y, w, h, s, fc="#ffffff", ec=EC, size=10, lw=1.0, z=5, color=None,
        weight=None, rounding=0.08):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rounding}",
                       fc=C.get(fc, fc), ec=C.get(ec, ec), lw=lw, zorder=z)
    ax.add_patch(p)
    text(ax, x + w / 2, y + h / 2, s, size=size, color=color, weight=weight, z=z + 1)
    return p


def legend(ax, keys, loc="upper right", ncol=1, size=9, bbox=None, names=None):
    names = names or {}
    hs = [Rectangle((0, 0), 1, 1, fc=C.get(k, k), ec=EC, lw=0.6) for k in keys]
    ls = [names.get(k, NAME.get(k, k)) for k in keys]
    kw = dict(loc=loc, ncol=ncol, fontsize=size, handlelength=1.2, handleheight=0.9,
              columnspacing=0.9, borderaxespad=0.2)
    if bbox:
        kw["bbox_to_anchor"] = bbox
    return ax.legend(hs, ls, **kw)


def ions(ax, xs, y0, y1, color="ink", lw=1.1, ms=8):
    """위에서 내려오는 ion 화살표 여러 개"""
    for x in xs:
        arrow(ax, x, y0, x, y1, color=color, lw=lw, ms=ms)


def light(ax, xs, y0, y1, color="#8e44ad", lw=1.2):
    """노광 빛 (물결 없이 점선 화살표)"""
    for x in xs:
        arrow(ax, x, y0, x, y1, color=color, lw=lw, ms=9, ls="--")


def save(f, post, name):
    d = os.path.join(IMG, f"{post:02d}")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name + ".png")
    f.savefig(p, metadata={"Software": None})
    plt.close(f)
    print("saved", os.path.relpath(p, ROOT))
    return p


def wafer_top(ax, cx, cy, r, c="si", notch=True, flats=None, lw=1.0, z=2):
    """wafer 윗면. flats = [(각도deg, 깊이비), ...]"""
    t = np.linspace(0, 2 * np.pi, 721)
    x = cx + r * np.cos(t)
    y = cy + r * np.sin(t)
    pts = np.c_[x, y]
    if flats:
        for ang, depth in flats:
            a = np.deg2rad(ang)
            n = np.array([np.cos(a), np.sin(a)])
            d = r * (1 - depth)
            rel = pts - [cx, cy]
            proj = rel @ n
            over = proj > d
            rel[over] = rel[over] - np.outer(proj[over] - d, n)
            pts = rel + [cx, cy]
    if notch:
        a = -np.pi / 2
        half = np.deg2rad(2.2)
        dist = np.abs(np.angle(np.exp(1j * (t - a))))
        for k in np.where(dist < half)[0]:
            frac = 1 - dist[k] / half
            rr = r * (1 - 0.06 * frac)
            pts[k] = [cx + rr * np.cos(t[k]), cy + rr * np.sin(t[k])]
    ax.add_patch(Polygon(pts, closed=True, fc=C.get(c, c), ec=EC, lw=lw, zorder=z))


def bracket(ax, x0, x1, y, s, size=9.5, h=0.15, color=None, below=False):
    """가로 치수선 + 글자"""
    col = color or C["ink"]
    sgn = -1 if below else 1
    ax.plot([x0, x0, x1, x1], [y - sgn * h, y, y, y - sgn * h], color=col, lw=0.9, zorder=14)
    text(ax, (x0 + x1) / 2, y + sgn * 0.25, s, size=size, va="bottom" if not below else "top",
         color=col)


def vdim(ax, x, y0, y1, s, size=9.5, side="right", color=None, off=0.25):
    """세로 치수선 + 글자"""
    col = color or C["ink"]
    arrow(ax, x, y0, x, y1, color=col, lw=0.9, ms=8, style="<|-|>")
    if side == "right":
        text(ax, x + off, (y0 + y1) / 2, s, size=size, ha="left", color=col)
    else:
        text(ax, x - off, (y0 + y1) / 2, s, size=size, ha="right", color=col)


def plot_ax(w=6.4, h=4.0):
    f, ax = plt.subplots(figsize=(w, h))
    ax.grid(alpha=0.25, lw=0.6)
    return f, ax
