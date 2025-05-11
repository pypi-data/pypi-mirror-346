#!/usr/bin/env python

"""utils.py: Calculate all the functions of utility"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

from types import SimpleNamespace

import numpy as np
import pandas as pd
from geopy.distance import great_circle as GC
from loguru import logger
from scipy.io import loadmat


def load_bearing_mat_file(file_loc: str):
    logger.info(f" Loading bearing file: {file_loc}")
    bearing = SimpleNamespace(**loadmat(file_loc))
    return bearing


def load_rays_mat_file(file_loc: str):
    logger.info(f" Loading rays file: {file_loc}")
    sim_data = loadmat(file_loc)
    path_data_keys = [
        "ground_range",
        "height",
        "group_range",
        "phase_path",
        "geometric_distance",
        "electron_density",
        "refractive_index",
    ]
    ray_data_keys = [
        "ground_range",
        "group_range",
        "phase_path",
        "geometric_path_length",
        "initial_elev",
        "final_elev",
        "apogee",
        "gnd_rng_to_apogee",
        "plasma_freq_at_apogee",
        "virtual_height",
        "effective_range",
        "deviative_absorption",
        "TEC_path",
        "Doppler_shift",
        "Doppler_spread",
        "frequency",
        "nhops_attempted",
        "ray_label",
    ]
    ray_data, ray_path_data = [], dict()
    for i in range(sim_data["ray_data"].shape[1]):
        r_data, p_data = dict(), dict()
        for key in ray_data_keys:
            r_data[key] = sim_data["ray_data"][0, i][key].ravel()[0]
            if key == "initial_elev":
                e = r_data[key]
        for key in path_data_keys:
            p_data[key] = sim_data["ray_path_data"][0, i][key].ravel()
        ray_path_data[e] = pd.DataFrame.from_records(p_data)
        ray_data.append(r_data)
    ray_data = pd.DataFrame.from_records(ray_data)
    return ray_data, ray_path_data


def create_lat_lon_from_routes(
    grange: np.array,
    r_bearing: float,
    olat: float,
    olon: float,
):
    lats, lons = [], []
    p = (olat, olon)
    gc = GC(p, p)
    for d in grange:
        x = gc.destination(p, r_bearing, distance=d)
        lats.append(x[0])
        lons.append(x[1])
    lats, lons = np.array(lats), np.array(lons)
    return lats, lons
