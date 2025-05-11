#!/usr/bin/env python

"""functions.py: Calculate absorption along the path"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

import datetime as dt

import matplotlib.pyplot as plt

plt.style.use(["science", "ieee"])
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Tahoma", "DejaVu Sans", "Lucida Grande", "Verdana"]
plt.rcParams["text.usetex"] = False
import numpy as np
from matplotlib.collections import LineCollection


class PlotOlRays(object):
    def __init__(self, date: dt.datetime, ylim=[], xlim=[]):
        self.date = date
        self.xlim = xlim
        self.ylim = ylim
        self.create_figure_pane()
        return

    def save(self, filepath):
        self.fig.savefig(filepath, bbox_inches="tight", facecolor=(1, 1, 1, 1))
        return

    def close(self):
        self.fig.clf()
        plt.close()
        return

    def get_parameter(self, kind):
        import matplotlib.colors as colors

        if kind == "pf":
            cmap, label, norm = (
                "plasma",
                r"$f_0$ [MHz]",
                colors.Normalize(4, 6),
            )
        if kind == "edens":
            cmap, label, norm = (
                "plasma",
                r"$N_e$ [$/cm^{-3}$]",
                colors.LogNorm(1e4, 1e6),
            )
        if kind == "ref_indx":
            cmap, label, norm = (
                "plasma",
                r"$\eta$",
                colors.Normalize(0.9, 1.0),
            )
        if kind == "los":
            cmap, label, norm = (
                "Reds",
                r"$\beta$, dB",
                colors.Normalize(0, 1e-2),
            )
        if kind == "phase":
            cmap, label, norm = (
                "RdBu",
                r"$\theta$ [Deg]",
                colors.Normalize(-np.pi, np.pi),
            )
        return cmap, label, norm

    def lay_rays(
        self,
        df,
        kind="los",
        zoomed_in=[],
        elv_range=[],
        tag_distance: float = -1,
        text=None,
    ):
        points = np.array([df.ground_range, df.height]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        cmap, label, norm = self.get_parameter(kind)
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(df[kind])
        lc.set_linewidth(2)
        line = self.ax.add_collection(lc)
        self.ax.plot(
            df.ground_range, df.height, c="k", zorder=3, alpha=0.7, ls="-", lw=0.1
        )
        pos = self.ax.get_position()
        cpos = [
            pos.x1 + 0.025,
            pos.y0 + 0.05,
            0.015,
            pos.height * 0.6,
        ]
        cax = self.fig.add_axes(cpos)
        cbax = self.fig.colorbar(
            line, cax, spacing="uniform", orientation="vertical", cmap="plasma"
        )
        _ = cbax.set_label(label)
        if tag_distance > 100:
            self.ax.plot(
                [tag_distance, tag_distance],
                [0, 100],
                c="m",
                zorder=4,
                alpha=0.7,
                ls="--",
                lw=0.8,
            )
        stitle = "%s UT" % self.date.strftime("%Y-%m-%d %H:%M")
        self.ax.text(
            0.95, 1.05, stitle, ha="right", va="center", transform=self.ax.transAxes
        )
        if text:
            self.ax.text(
                0.05, 0.9, text, ha="left", va="center", transform=self.ax.transAxes
            )
        # Create Zoomed in panel
        if len(zoomed_in):
            self.__zoomed_in_panel__(df, kind, zoomed_in)
        return

    def create_figure_pane(self):
        self.fig = plt.figure(figsize=(6, 3), dpi=300)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel(r"Height [km]")
        self.ax.set_xlabel(r"Ground range [km]")
        self.ax.set_xlim(self.xlim if len(self.xlim) == 2 else [0, 3000])
        self.ax.set_ylim(self.ylim if len(self.ylim) == 2 else [0, 400])
        return

    def __zoomed_in_panel__(self, df, kind, zoomed_in):
        self.zoom_ax = self.ax.inset_axes([0.4, 1.3, 0.3, 0.5])
        cmap, _, norm = self.get_parameter(kind)
        points = np.array([df.grange, df.height]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        cmap, label, norm = self.get_parameter(kind)
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(df[kind])
        lc.set_linewidth(0.8)
        self.zoom_ax.add_collection(lc)
        self.zoom_ax.plot(
            df.grange, df.height, c="k", zorder=3, alpha=0.7, ls="-", lw=0.1
        )

        self.zoom_ax.set_xlim(zoomed_in[0])
        self.zoom_ax.set_ylim(zoomed_in[1])
        th_ticklabels, r_ticklabels = (
            self.zoom_ax.get_xticklabels(),
            self.zoom_ax.get_yticklabels(),
        )
        self.zoom_ax.set_xlabel("Ground Range, [km]", fontdict={"size": 8})
        self.zoom_ax.set_ylabel("Height, [km]", fontdict={"size": 8})
        self.ax.indicate_inset_zoom(self.zoom_ax)
        return
