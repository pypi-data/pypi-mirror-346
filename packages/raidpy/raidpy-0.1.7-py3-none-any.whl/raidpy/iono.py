#!/usr/bin/env python

"""iono.py: Calculate Ionosphereic object along the path"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

import datetime as dt

import numpy as np
from loguru import logger

from raidpy.absorption import CalculateAbsorption
from raidpy.collision import ComputeCollision
from raidpy.ionosphere.igrf13 import IGRF2d
from raidpy.ionosphere.iri import IRI2d
from raidpy.ionosphere.msise import MSISE2d
from raidpy.phase import CalculatePhase


class Ionosphere2d(object):
    """
    This function calculate thermospheric parameters along the path.

    Parameters:
    -----------
    date: Datetime of the event
    lats: Latitudes as an array (same size as alts)
    lons: Longitudes as an array (same size as alts)
    alts: Altitudes as an array

    All lat, lon and alts has same size.
    """

    def __init__(
        self,
        date: dt.datetime,
        lats: np.array,
        lons: np.array,
        alts: np.array,
        fo: float = 5e6,  # in Hz
        iri_version: int = 20,
    ):
        self.date = date
        self.lats = lats
        self.lons = lons
        self.alts = alts
        self.iri_version = iri_version
        self.fo = fo
        self.initl()
        return

    def initl(self):
        logger.info(f"Initialize ionosphere on {self.date}")
        self.iri_block = IRI2d(
            self.date,
            self.lats,
            self.lons,
            self.alts,
            self.iri_version,
        )
        self.msise_block = MSISE2d(
            self.date,
            self.lats,
            self.lons,
            self.alts,
        )
        self.igrf_block = IGRF2d(
            self.date,
            self.lats,
            self.lons,
            self.alts,
        )
        return

    def compute(
        self,
    ):
        """
        Run Ionosphere codes
        """
        logger.info(f"Running ionosphere on {self.date}")
        self.cc = ComputeCollision(
            self.msise_block.msise, self.iri_block.iri, date=self.date, _run_=True
        )
        self.ca = CalculateAbsorption(
            self.iri_block.iri,
            self.igrf_block.igrf,
            self.cc.collision,
            fo=self.fo,
            _run_=True,
        )
        self.cp = CalculatePhase(
            self.iri_block.iri,
            self.igrf_block.igrf,
            self.cc.collision,
            fo=self.fo,
            _run_=True,
        )
        return


if __name__ == "__main__":
    ion = Ionosphere2d(
        dt.datetime(2024, 4, 8),
        np.array([0, 1, 3]),
        np.array([0, 1, 3]),
        np.array([100, 200, 300]),
    )
