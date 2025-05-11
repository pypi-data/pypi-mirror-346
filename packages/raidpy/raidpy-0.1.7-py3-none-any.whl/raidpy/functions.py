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
import os

import numpy as np
import pandas as pd
from loguru import logger

from raidpy import utils
from raidpy.iono import Ionosphere2d
from raidpy.plots import PlotOlRays


class Oblique(object):
    """
    This class takes PHaRLAP rays as input and computes absorption along the path
    """

    def __init__(
        self,
        date: dt.datetime,
        grange: np.array,
        height: np.array,
        ray_bearing: float,
        origin_lat: float,
        origin_lon: float,
        fo: float,
        ion2d: dict = None,
        igrf2d: dict = None,
        msise: dict = None,
        edens: np.array = None,
        ray_details: pd.DataFrame = pd.DataFrame(),
    ):
        self.date = date
        self.ground_range = grange
        self.height = height
        self.ray_bearing = ray_bearing
        self.origin_lat = origin_lat
        self.origin_lon = origin_lon
        self.edens = edens
        self.fo = fo
        self.ion2d = ion2d
        self.msise = msise
        self.igrf2d = igrf2d
        self.ray_details = ray_details
        self.initialize()
        return

    def initialize(self):
        logger.info(f"Initialize for {self.date}")
        self.glats, self.glons = utils.create_lat_lon_from_routes(
            self.ground_range, self.ray_bearing, self.origin_lat, self.origin_lon
        )
        self.galts = np.array(self.height)
        self.iono = Ionosphere2d(self.date, self.glats, self.glons, self.galts, self.fo)
        if self.edens is not None:
            logger.info(f"change e-dens")
            self.iono.iri_block.iri["edens"] = self.edens
        self.iono.compute()
        self.ray = pd.DataFrame()
        self.ray["ground_range"], self.ray["height"] = self.ground_range, self.height
        return

    def get_absorption_datasets(
        self,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
    ):
        _a = getattr(
            getattr(getattr(self.iono.ca, wave_disp_reltn), col_freq), f"mode_{mode}"
        )
        ray = (
            self.ray_details.copy()
            if self.ray_details is not None and len(self.ray_details) == len(self.ray)
            else self.ray.copy()
        )
        ray["los"] = _a
        if not hasattr(self, "total_free_path_los"):
            self.total_free_path_los = 10 * np.log10(
                1.0 / ray.geometric_distance.iloc[-1]
            )
            logger.info(f"Total free path LoS {self.total_free_path_los}")
        return ray

    def get_total_absorption_along_path(
        self,
        phase_path: np.array,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
    ):
        ray = self.get_absorption_datasets(wave_disp_reltn, col_freq, mode)
        phase_path = phase_path if phase_path is not None else ray.phase_path
        ray.fillna(0, inplace=True)
        total_absorption = np.trapz(ray.los, phase_path)
        logger.info(f"Total absorption {total_absorption} dB")
        return total_absorption

    def plot_absorption(
        self,
        phase_path: np.array,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
        fig_path: str = "figures/test_figures.png",
        text: str = None,
    ):
        logger.info(f"Plotting for {self.date} for {wave_disp_reltn}:{col_freq}")
        pol = PlotOlRays(self.date)
        ray = self.get_absorption_datasets(wave_disp_reltn, col_freq, mode)
        total_absorption = self.get_total_absorption_along_path(
            phase_path, wave_disp_reltn, col_freq, mode
        )
        logger.info(f"Total absorption {total_absorption} dB")
        pol.lay_rays(ray, text=text + r" / $\int\beta$=%.1f dB" % total_absorption)
        dirc = fig_path.split("/")
        if len(dirc) > 1:
            os.makedirs("/".join(dirc[:-1]), exist_ok=True)
        pol.save(fig_path)
        pol.close()
        logger.info(f"Saving files in {fig_path}")
        return total_absorption

    def get_phase_datasets(
        self,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
    ):
        p = getattr(
            getattr(getattr(self.iono.cp, wave_disp_reltn), col_freq), f"mode_{mode}"
        )
        ray = (
            self.ray_details.copy()
            if self.ray_details is not None and len(self.ray_details) == len(self.ray)
            else self.ray.copy()
        )
        ray["phase"] = p
        return ray

    def get_total_phase_along_path(
        self,
        phase_path: np.array,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
    ):
        ray = self.get_phase_datasets(wave_disp_reltn, col_freq, mode)
        phase_path = phase_path if phase_path is not None else ray.phase_path
        ray.fillna(0, inplace=True)
        total_phase = np.trapz(ray["phase"], phase_path)
        logger.info(f"Total phase {total_phase} radian")
        return total_phase
