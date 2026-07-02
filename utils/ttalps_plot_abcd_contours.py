import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator, NullFormatter, LogLocator, LogFormatterMathtext

import mplhep as hep
hep.style.use("CMS")


def truncate_cmap(cmap, minval=0.0, maxval=1.0, n=256):
    return LinearSegmentedColormap.from_list(
        f"trunc({cmap.name})",
        cmap(np.linspace(minval, maxval, n))
    )


def root_th2d_to_numpy(hist):
    nx = hist.GetNbinsX()
    ny = hist.GetNbinsY()
    data = np.zeros((ny, nx))
    xedges = np.array([hist.GetXaxis().GetBinLowEdge(i+1) for i in range(nx+1)])
    yedges = np.array([hist.GetYaxis().GetBinLowEdge(i+1) for i in range(ny+1)])
    for i in range(nx):
        for j in range(ny):
            data[j, i] = hist.GetBinContent(i+1, j+1)
    return data, xedges, yedges


# def draw_scaled_boxes(ax, X_centers, Y_centers, Z, bin_w, bin_h, cmap, norm, zorder=1):
#     """Draw rectangles scaled by bin value, centered on bin positions."""
#     ny, nx = Z.shape
#     for j in range(ny):
#         for i in range(nx):
#             val = Z[j, i]
#             if np.isnan(val) or val <= 0:
#                 continue
#             color = cmap(norm(val))
#             # scale box size by sqrt(val/vmax) so area ∝ value
#             scale = np.sqrt(val / norm.vmax)
#             w = bin_w[i] * scale
#             h = bin_h[j] * scale
#             x = X_centers[i] - w / 2
#             y = Y_centers[j] - h / 2
#             rect = plt.Rectangle((x, y), w, h,
#                                   facecolor=color, edgecolor="none",
#                                   zorder=zorder)
#             ax.add_patch(rect)

def draw_scaled_boxes(
    ax,
    X_centers,
    Y_centers,
    Z,
    bin_w,
    bin_h,
    cmap,
    norm,
    size_max,
    zorder=1,
):
    ny, nx = Z.shape

    for j in range(ny):
        for i in range(nx):
            val = Z[j, i]
            if np.isnan(val) or val <= 0:
                continue

            color = cmap(norm(val))

            scale = np.sqrt(val / size_max)

            w = bin_w[i] * scale
            h = bin_h[j] * scale

            rect = plt.Rectangle(
                (X_centers[i] - w/2, Y_centers[j] - h/2),
                w, h,
                facecolor=color,
                edgecolor="none",
                zorder=zorder,
            )
            ax.add_patch(rect)


def plot_abcd_box(
    h_background,
    h_signal,
    cut_x,
    cut_y,
    mass,
    ctau,
    category,
    axis_labels,
    output_path=None
):
    hep.style.use("CMS")

    bg_data, xedges, yedges = root_th2d_to_numpy(h_background)
    sig_data, _, _ = root_th2d_to_numpy(h_signal)

    # ── normalize to fractions ────────────────────────────────────────────────
    bg  = bg_data.astype(float)
    sig = sig_data.astype(float)
    # bg  /= bg.sum()  if bg.sum()  > 0 else 1.0
    # sig /= sig.sum() if sig.sum() > 0 else 1.0

    # ── shared log scale ──────────────────────────────────────────────────────
    eps = 1e-9  # mask true zeros
    bg_masked  = np.where(bg  > 0, bg,  np.nan)
    sig_masked = np.where(sig > 0, sig, np.nan)

    # all_nonzero = np.concatenate([bg[bg > 0], sig[sig > 0]])
    # vmin = 10 ** np.floor(np.log10(all_nonzero.min()))
    # vmax = 10 ** np.ceil( np.log10(all_nonzero.max()))
    # norm = LogNorm(vmin=vmin, vmax=vmax)

    sig_z_min = 1e-4
    sig_z_max = 1e2
    bg_z_min = 1e0
    bg_z_max = 1e2

    bg_norm = LogNorm(bg_z_min, bg_z_max)
    sig_norm = LogNorm(sig_z_min, sig_z_max)

    # bg_nonzero = bg[bg > 0]
    # sig_nonzero = sig[sig > 0]
    # bg_norm = LogNorm(
    #     vmin=10 ** np.floor(np.log10(bg_nonzero.min())),
    #     vmax=10 ** np.ceil(np.log10(bg_nonzero.max())),
    # )
    # sig_norm = LogNorm(
    #     vmin=10 ** np.floor(np.log10(sig_nonzero.min())),
    #     vmax=10 ** np.ceil(np.log10(sig_nonzero.max())),
    # )

    # ── grid (bin edges for pcolormesh) ───────────────────────────────────────
    X, Y = np.meshgrid(xedges, yedges)   # shape (ny+1, nx+1) — correct for pcolormesh

    xlo, xhi = xedges[0], xedges[-1]
    ylo, yhi = yedges[0], yedges[-1]

    # ── figure ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8.0, 7.0))
    fig.subplots_adjust(right=0.74)

    # ── bin centres and sizes ─────────────────────────────────────────────────
    xcenters = 0.5 * (xedges[:-1] + xedges[1:])
    ycenters = 0.5 * (yedges[:-1] + yedges[1:])
    bin_w = xedges[1:] - xedges[:-1]   # per-bin widths
    bin_h = yedges[1:] - yedges[:-1]   # per-bin heights

    # ── background (grey scaled boxes) ───────────────────────────────────────
    bg_cmap = truncate_cmap(plt.cm.Greys, 0.4, 1.0)
    # draw_scaled_boxes(ax, xcenters, ycenters, bg_masked,
    #                   bin_w, bin_h, bg_cmap, bg_norm, zorder=1)

    # # ── signal (red scaled boxes) ─────────────────────────────────────────────
    sig_cmap = truncate_cmap(plt.cm.Reds, 0.2, 1.0)
    # draw_scaled_boxes(ax, xcenters, ycenters, sig_masked,
    #                   bin_w, bin_h, sig_cmap, sig_norm, zorder=2)

    bg_size_max = np.nanmax(bg_masked)
    sig_size_max = np.nanmax(sig_masked)

    draw_scaled_boxes(
        ax, xcenters, ycenters,
        bg_masked,
        bin_w, bin_h,
        bg_cmap, bg_norm,
        bg_size_max,
        zorder=1,
    )

    draw_scaled_boxes(
        ax, xcenters, ycenters,
        sig_masked,
        bin_w, bin_h,
        sig_cmap, sig_norm,
        sig_size_max,
        zorder=2,
    )

    # # ── background (grey boxes) ───────────────────────────────────────────────
    # bg_cmap = truncate_cmap(plt.cm.Greys, 0.1, 1.0)
    # bg_cmap.set_bad(alpha=0)   # NaN (zero bins) → transparent
    # ax.pcolormesh(
    #     X, Y, bg_masked,
    #     cmap=bg_cmap,
    #     norm=norm,
    #     shading="flat",
    #     zorder=1,
    # )

    # # ── signal (red boxes on top) ─────────────────────────────────────────────
    # sig_cmap = truncate_cmap(plt.cm.Reds, 0.1, 1.0)
    # sig_cmap.set_bad(alpha=0)  # NaN (zero bins) → transparent
    # ax.pcolormesh(
    #     X, Y, sig_masked,
    #     cmap=sig_cmap,
    #     norm=norm,
    #     shading="flat",
    #     zorder=2,
    # )

    # ── ABCD cut lines (solid cyan) ───────────────────────────────────────────
    line_kw = dict(color="cyan", linewidth=1.5, zorder=4)
    ax.axvline(cut_x, **line_kw)
    ax.axhline(cut_y, **line_kw)

    # ── ABCD labels ───────────────────────────────────────────────────────────
    dx = 0.015 * (xhi - xlo)
    dy = 0.015 * (yhi - ylo)
    label_kw = dict(fontsize=16, fontweight="bold", color="cyan", zorder=5)

    ax.text(xlo + 5*dx, cut_y + dy, "A", ha="right", va="bottom", **label_kw)
    ax.text(xhi - 5*dx, cut_y + dy, "C", ha="left",  va="bottom", **label_kw)
    ax.text(xlo + 5*dx, cut_y - dy, "B", ha="right", va="top",    **label_kw)
    ax.text(xhi - 5*dx, cut_y - dy, "D", ha="left",  va="top",    **label_kw)

    # ── axes ──────────────────────────────────────────────────────────────────
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.set_xlabel(axis_labels[0], fontsize=22)
    ax.set_ylabel(axis_labels[1], fontsize=22)
    ax.tick_params(axis="both", labelsize=20)
    # ax.xaxis.set_major_locator(MultipleLocator(1))
    # ax.yaxis.set_major_locator(MultipleLocator(1))

    if category == "_Pat":
        draw_custom_Pat_axes(ax)
    elif category == "_PatDSA":
        draw_custom_PatDSA_axes(ax)
    elif category == "_DSA":
        draw_custom_DSA_axes(ax)


    # ── in-plot label ─────────────────────────────────────────────────────────
    ax.text(
        0.05, 0.95,
        f"{mass} GeV, {ctau}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=20,
        fontweight="bold",
        color=plt.cm.Reds(1.0),
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
    )

    # ── CMS label ─────────────────────────────────────────────────────────────
    hep.cms.label(
        llabel="Preliminary",
        rlabel=r"138 fb$^{-1}$ (13 TeV), 62 fb$^{-1}$ (13.6 TeV)",
        ax=ax,
        fontsize=15,
    )

    # ── dual colorbars ────────────────────────────────────────────────────────
    ax_bg_cb  = fig.add_axes([0.76, 0.11, 0.03, 0.77])
    ax_sig_cb = fig.add_axes([0.86, 0.11, 0.03, 0.77])

    # fig.colorbar(ScalarMappable(norm=norm, cmap=bg_cmap),  cax=ax_bg_cb)
    # fig.colorbar(ScalarMappable(norm=norm, cmap=sig_cmap), cax=ax_sig_cb)
    fig.colorbar(
        ScalarMappable(norm=bg_norm, cmap=bg_cmap),
        cax=ax_bg_cb
    )
    fig.colorbar(
        ScalarMappable(norm=sig_norm, cmap=sig_cmap),
        cax=ax_sig_cb
    )

    ax_bg_cb.set_title("Data",   fontsize=16, pad=12)
    ax_sig_cb.set_title("Signal", fontsize=16, pad=12)

    ax_bg_cb.set_ylim(bg_z_min, bg_z_max)
    ax_sig_cb.set_ylim(sig_z_min, sig_z_max)

    ax_bg_cb.yaxis.set_ticks_position("right")
    ax_sig_cb.yaxis.set_ticks_position("right")
    # ax_sig_cb.set_ylabel("Fraction of events", fontsize=12)
    ax_sig_cb.set_ylabel("Event yields", fontsize=22)
    ax_sig_cb.yaxis.set_label_position("right")
    ax_bg_cb.tick_params(labelsize=20)
    ax_sig_cb.tick_params(labelsize=20)
    ax_bg_cb.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,)))
    ax_bg_cb.yaxis.set_major_formatter(LogFormatterMathtext(base=10))

    # Minor ticks: keep marks but remove labels
    ax_bg_cb.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
    ax_bg_cb.yaxis.set_minor_formatter(NullFormatter())

    # ── save / show ───────────────────────────────────────────────────────────
    if output_path:
        print(f"Saving plot to {output_path}")
        fig.savefig(output_path, bbox_inches="tight", dpi=150)
    else:
        plt.show()

    plt.close(fig)


def draw_custom_Pat_axes(ax):
    # ── custom tick labels (linear values on log-transformed axes) ────────────
    # x-axis major ticks at each decade
    x_tick_positions = list(range(-4, 2))
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels([f"$10^{{{p}}}$" for p in x_tick_positions], fontsize=20)

    x_minor_positions = [p + np.log10(i) for p in range(-4, 1) for i in range(2, 10)]
    ax.xaxis.set_minor_locator(FixedLocator(x_minor_positions))
    ax.xaxis.set_minor_formatter(NullFormatter())

    y_tick_positions = list(range(-6, 4)) 
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels([f"$10^{{{p}}}$" for p in y_tick_positions], fontsize=20)

    y_minor_positions = [p + np.log10(i) for p in range(-6, 4) for i in range(2, 10)]
    ax.yaxis.set_minor_locator(FixedLocator(y_minor_positions))
    ax.yaxis.set_minor_formatter(NullFormatter())

def draw_custom_PatDSA_axes(ax):
    # ── custom tick labels (linear values on log-transformed axes) ────────────
    # x-axis major ticks at each decade
    x_tick_positions = list(range(-7, 2))
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels([f"$10^{{{p}}}$" for p in x_tick_positions], fontsize=20)

    x_minor_positions = [p + np.log10(i) for p in range(-7, 1) for i in range(2, 10)]
    ax.xaxis.set_minor_locator(FixedLocator(x_minor_positions))
    ax.xaxis.set_minor_formatter(NullFormatter())

    y_tick_positions = list(range(-6, 4)) 
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels([f"$10^{{{p}}}$" for p in y_tick_positions], fontsize=20)

    y_minor_positions = [p + np.log10(i) for p in range(-6, 4) for i in range(2, 10)]
    ax.yaxis.set_minor_locator(FixedLocator(y_minor_positions))
    ax.yaxis.set_minor_formatter(NullFormatter())

def draw_custom_DSA_axes(ax):
    # ── custom tick labels (linear values on log-transformed axes) ────────────
    # x-axis major ticks at each decade
    x_tick_positions = list(range(-4, 2))  # -4, -3, -2, -1, 0, 1
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels([f"$10^{{{p}}}$" for p in x_tick_positions], fontsize=20)

    x_minor_positions = [p + np.log10(i) for p in range(-4, 1) for i in range(2, 10)]
    ax.xaxis.set_minor_locator(FixedLocator(x_minor_positions))
    ax.xaxis.set_minor_formatter(NullFormatter())

    y_tick_positions = list(range(-1, 8))  # -1, 0, 1, ..., 7
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels([f"$10^{{{p}}}$" for p in y_tick_positions], fontsize=20)

    y_minor_positions = [p + np.log10(i) for p in range(-1, 7) for i in range(2, 10)]
    ax.yaxis.set_minor_locator(FixedLocator(y_minor_positions))
    ax.yaxis.set_minor_formatter(NullFormatter())


# ── Main ──────────────────────────────────────────────────────────────────────
# category = "_Pat"
# category = "_PatDSA"
category = "_DSA"

lifetimes = {
    "_Pat": ("1e1", "1 cm"),
    "_PatDSA": ("1e2", "10 cm"),
    "_DSA": ("1e2", "10 cm"),
}
lifetime = lifetimes[category]

optimal_points = {
    "_Pat": (17, 13),
    "_PatDSA": (33, 11),
    "_DSA": (18, 11),
}
bin_x, bin_y = optimal_points[category]

axis_labels = {
    "_Pat": (r"$-p_T$ [GeV]", r"$d_{xy}^{\mu^2}$ [cm]"),
    "_PatDSA": (r"$|\Delta\Phi_{coll}|$", r"$d_{xy}^{\mu^1}$ [cm]"),
    "_DSA": (r"$-p_T$ [GeV]", r"$-|\Delta\Phi_{coll}|$"),
}

root_file_path = (
    "/afs/desy.de/user/l/lrygaard/TTALP/tea_ttalps/abcd/results_2016preVFP2016postVFP201720182022preEE2022postEE"
    f"2023preBPix2023postBPix/results_SR_ANv10_regionABCD_BestPFIsoDimuonVertex_SRDimuons_data{category}_signalscaled/"
    f"signal_hists/histograms{category}.root"
)

f = ROOT.TFile.Open(root_file_path, "READ")
if not f or f.IsZombie():
    raise RuntimeError(f"Could not open ROOT file: {root_file_path}")

h_background = f.Get("background")
h_signal     = f.Get(f"signal_12_{lifetime[0]}")

if not h_background:
    raise RuntimeError("Could not find histogram 'background' in file")
if not h_signal:
    raise RuntimeError("Could not find histogram 'signal_12_1e2' in file")

h_background.SetDirectory(0)
h_signal.SetDirectory(0)
f.Close()

cut_x = float(h_background.GetXaxis().GetBinLowEdge(bin_x))
cut_y = float(h_background.GetYaxis().GetBinLowEdge(bin_y))

plot_abcd_box(
    h_background, h_signal,
    cut_x=cut_x, cut_y=cut_y,
    mass=12, ctau=lifetime[1],
    category=category,
    axis_labels=axis_labels[category],
    output_path=f"../abcd_12_{lifetime[0]}{category}.pdf"
)
