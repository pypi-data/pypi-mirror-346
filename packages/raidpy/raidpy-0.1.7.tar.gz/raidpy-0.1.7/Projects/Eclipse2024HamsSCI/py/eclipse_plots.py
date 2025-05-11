from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np

from raidpy.functions import Oblique

plt.style.use(["science", "ieee"])
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Tahoma", "DejaVu Sans", "Lucida Grande", "Verdana"]
plt.rcParams["text.usetex"] = False


def line_plots_all(ols: Sequence[Oblique]) -> None:
    fig = plt.figure(figsize=(6, 3), dpi=300)
    ax = fig.add_subplot(111)
    ax.plot(
        np.arange(len(ols)) * 5,
        [
            o.get_total_absorption_along_path(
                None,
                "ah",
                "sn",
                "O",
            )
            for o in ols
        ],
        color="r",
        ms=2,
        marker=".",
        ls="-",
        label=r"$\beta_{ah}(\nu_{sn})$",
    )
    ax.plot(
        np.arange(len(ols)) * 5,
        [
            o.get_total_absorption_along_path(
                None,
                "ah",
                "ft",
                "O",
            )
            for o in ols
        ],
        color="b",
        ms=2,
        marker=".",
        ls="-",
        label=r"$\beta_{ah}(\nu_{ft})$",
    )
    ax.plot(
        np.arange(len(ols)) * 5,
        [
            o.get_total_absorption_along_path(
                None,
                "ah",
                "av_cc",
                "O",
            )
            for o in ols
        ],
        color="k",
        ms=2,
        marker=".",
        ls="-",
        label=r"$\beta_{ah}(\nu_{av-cc})$",
    )
    ax.plot(
        np.arange(len(ols)) * 5,
        [
            o.get_total_absorption_along_path(
                None,
                "ah",
                "av_mb",
                "O",
            )
            for o in ols
        ],
        color="g",
        ms=2,
        marker=".",
        ls="-",
        label=r"$\beta_{ah}(\nu_{av-mb})$",
    )
    ax.plot(
        np.arange(len(ols)) * 5,
        [
            o.get_total_absorption_along_path(
                None,
                "sw",
                "ft",
                "O",
            )
            for o in ols
        ],
        color="m",
        ms=2,
        marker=".",
        ls="-",
        label=r"$\beta_{sw}(\nu_{ft})$",
    )
    ax.legend(loc=1, fontsize=8)
    ax.set_ylabel("O-mode Absorption, dB")
    ax.set_xlabel("Minutes since 17 UT on 8 April 2024")
    text = r"Spot: wwv-w2naf / 10 Mhz, $\alpha=30^\circ$ / $\int\beta$"
    ax.text(
        0.05,
        1.05,
        text,
        horizontalalignment="left",
        verticalalignment="center",
        transform=ax.transAxes,
    )
    fig.savefig(
        "figures/ts_absorption.png", bbox_inches="tight", facecolor=(1, 1, 1, 1)
    )
    return
