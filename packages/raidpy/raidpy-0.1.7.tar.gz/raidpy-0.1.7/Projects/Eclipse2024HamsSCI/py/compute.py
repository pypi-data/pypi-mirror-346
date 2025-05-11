import datetime as dt

import matplotlib.pyplot as plt
import numpy as np

from raidpy import utils
from raidpy.functions import Oblique

plt.style.use(["science", "ieee"])
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Tahoma", "DejaVu Sans", "Lucida Grande", "Verdana"]
plt.rcParams["text.usetex"] = False


if __name__ == "__main__":
    import sys

    sys.path.append("Projects/Eclipse2024HamsSCI/py")

    bearing_file_loc = "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_10MHz_SCurve/2024-04-08/wwv/sami3/w2naf/bearing.mat"
    bearing = utils.load_bearing_mat_file(bearing_file_loc)
    tfreq = bearing.freq.ravel()[0]
    rays_file_locs = [
        "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_%02dMHz_SCurve/2024-04-08/wwv/sami3/w2naf/1700_rt.mat"
        % tfreq,
        "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_%02dMHz_SCurve/2024-04-08/wwv/sami3/w2naf/1705_rt.mat"
        % tfreq,
    ]
    # rays_file_locs = glob.glob(
    #     "/home/chakras4/OneDrive/trace/outputs/April2024_SAMI3_eclipse_hamsci_%02dMHz_SCurve/2024-04-08/wwv/sami3/w2naf/*_rt.mat"%tfreq
    # )
    rays_file_locs.sort()
    elv = 12
    wave_disp_reltn = "ah"
    col_freq = "sn"
    paths, absorptions, dop = [], [], []
    for i, floc in enumerate(rays_file_locs):
        _, rays = utils.load_rays_mat_file(floc)
        ray = rays[elv]
        ol = Oblique(
            dt.datetime(2024, 4, 8, 17) + dt.timedelta(minutes=i * 5),
            np.array(ray.ground_range),
            np.array(ray.height),
            bearing.rb,
            bearing.olat,
            bearing.olon,
            bearing.freq.ravel().tolist()[0] * 1e6,
            edens=np.array(ray.electron_density) * 1e6,  # To /m3
            ray_details=ray,
        )
        t_abs = ol.plot_absorption(
            None,
            wave_disp_reltn=wave_disp_reltn,
            col_freq=col_freq,
            text=f"Spot: wwv-w2naf / {tfreq} MHz, $\\alpha={elv}^\circ$ "
            + r"/ $\beta=\beta_{ah}(\nu_{sn})$",
            fig_path="figures/%04d.png" % i,
        )
        absorptions.append(t_abs)
        paths.append(ol)

    # fig = plt.figure(figsize=(6, 3), dpi=300)
    # ax = fig.add_subplot(111)
    # ax.plot(np.arange(len(absorptions)) * 5, absorptions, color="r", ms=2, marker=".")
    # ax.set_ylabel("O-mode Absorption, dB")
    # ax.set_xlabel("Minutes since 17 UT on 8 April 2024")
    # fig.savefig(
    #     "figures/ts_absorption.png", bbox_inches="tight", facecolor=(1, 1, 1, 1)
    # )
    # ep.line_plots_all(paths)

    # from raidpy.doppler import ComputeDoppler

    # for i, floc in enumerate(rays_file_locs[:-1]):
    #     cd = ComputeDoppler(
    #         paths[i],
    #         paths[1 + i],
    #         fo=bearing.freq.ravel().tolist()[0] * 1e6,
    #         del_t=300,
    #         _run_=True,
    #         mode="O",
    #         wave_disp_reltn=wave_disp_reltn,
    #         col_freq=col_freq,
    #     )
    #     dop.append(cd.dop.df)
    # print(dop)
    # fig = plt.figure(figsize=(6, 3), dpi=300)
    # ax = fig.add_subplot(111)
    # ax.plot(np.arange(len(dop)) * 5, dop, color="r", ms=2, marker=".")
    # ax.set_ylabel("Doppler, Hz")
    # ax.set_xlabel("Minutes since 17 UT on 8 April 2024")
    # fig.savefig("figures/ts_dop.png", bbox_inches="tight", facecolor=(1, 1, 1, 1))
