#!/usr/bin/env python

"""igrf.py: Calculate IGRF object along the path"""

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

import igrf

igrf.build()


class IGRF2d(object):
    """
    This function calculate thermospheric B-field along the path.

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
        to_Tesla: bool = True,
    ):
        self.date = date
        self.lats = lats
        self.lons = lons
        self.alts = alts
        self.to_Tesla = to_Tesla
        self.compute()
        return

    def compute(
        self,
    ):
        """
        Run IGRF codes
        """
        logger.info(f"Running IGRF on {self.date}")
        n = len(self.alts)
        self.igrf = dict(
            north=np.zeros((n)),  # Bo north compnent in nT
            east=np.zeros((n)),  # Bo east compnent in nT
            down=np.zeros((n)),  # Bo down compnent in nT
            total=np.zeros((n)),  # Total Bo in nT
            incl=np.zeros((n)),  # Inclinition in deg
            decl=np.zeros((n)),  # Declination in deg
        )
        for lat, lon, alt, j in zip(self.lats, self.lons, self.alts, range(n)):
            mag = igrf.igrf(
                self.date.strftime("%Y-%m-%d"), glat=lat, glon=lon, alt_km=alt
            )
            for i, key in enumerate(self.igrf.keys()):
                self.igrf[key][j] = mag.variables[key][0]
        if self.to_Tesla:
            self.igrf["north"] *= 1e-9
            self.igrf["east"] *= 1e-9
            self.igrf["down"] *= 1e-9
            self.igrf["total"] *= 1e-9
        return


if __name__ == "__main__":
    msise = IGRF2d(
        dt.datetime(2024, 4, 8),
        np.array([0, 1, 3]),
        np.array([0, 1, 3]),
        np.array([100, 200, 300]),
    )
