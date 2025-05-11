#!/usr/bin/env python

"""doppler.py: Doppler is dedicated to doppler related function."""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

from dataclasses import dataclass

import numpy as np
from loguru import logger

from raidpy.constants import *
from raidpy.functions import Oblique


@dataclass
class Doppler:
    mode: str = None
    wave_disp_reltn: str = None
    col_freq: str = None
    pt0: Oblique = None
    pt1: Oblique = None
    dp: float = np.nan
    dv: float = np.nan
    df: float = np.nan


class ComputeDoppler(object):
    """
    This class is used to Doppler height profile.

    pt0 = Phase at time t0
    pt1 = Phase at time t1
    del_t = Total time in secs
    fo = operating frequency
    """

    def __init__(
        self,
        pt0: Oblique,
        pt1: Oblique,
        fo: float,
        del_t: float,
        _run_=False,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
    ):
        self.pt0 = pt0
        self.pt1 = pt1
        self.fo = fo
        self.del_t = del_t
        self.wave_disp_reltn = wave_disp_reltn
        self.col_freq = col_freq
        self.mode = mode
        self.w = 2 * np.pi * fo
        self.k = (2 * np.pi * fo) / pconst["c"]
        if _run_:
            logger.info(f"Running Doppler calculations....")
            self.estimate_dop()
        return

    def estimate_dop(self):
        self.dop = Doppler(
            pt0=self.pt0,
            pt1=self.pt1,
            mode=self.mode,
            col_freq=self.col_freq,
            wave_disp_reltn=self.wave_disp_reltn,
        )
        logger.info(
            f"Solving Doppler for {self.wave_disp_reltn.upper()}:{self.col_freq.upper()} Mode>{self.mode}"
        )
        p0, p1 = (
            self.pt0.get_total_phase_along_path(
                None, self.wave_disp_reltn, self.col_freq, self.mode
            ),
            self.pt1.get_total_phase_along_path(
                None, self.wave_disp_reltn, self.col_freq, self.mode
            ),
        )
        self.dop.dp, self.dop.df = (
            (p0 - p1) / self.del_t,
            (p0 - p1) / (self.del_t * 4 * np.pi),
        )
        self.dop.dv = self.dop.df * pconst["c"] / (2 * self.fo)
        return self.dop


class ComputeKikuchiDoppler(object):
    """
    This class is used to Kikuchi's Doppler height profile.

    df0 = Details at time t0
    df1 = Details at time t1
    del_t = Total time in secs
    fo = operating frequency
    """

    def __init__(
        self,
        pt0: Oblique,
        pt1: Oblique,
        fo: float,
        del_t: float,
        _run_=False,
        wave_disp_reltn: str = "ah",
        col_freq: str = "sn",
        mode: str = "O",
    ):
        return
