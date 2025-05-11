#!/usr/bin/env python

"""msise.py: Calculate msise object along the path"""

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
import pymsis
from loguru import logger


class MSISE2d(object):
    """
    This function calculate thermospheric gas densities along the path.

    Parameters:
    -----------
    date: Datetime of the event
    lats: Latitudes as an array (same size as alts)
    lons: Longitudes as an array (same size as alts)
    alts: Altitudes as an array

    All lat, lon and alts has same size.
    """

    def __init__(
        self, date: dt.datetime, lats: np.array, lons: np.array, alts: np.array
    ):
        self.date = date
        self.lats = lats
        self.lons = lons
        self.alts = alts
        self.compute()
        return

    def compute(self):
        """
        run pymsise
        """
        keys = ["nn", "N2", "O2", "O", "He", "H", "Ar", "N", "O_Anomalous", "NO", "Tn"]
        n = len(self.alts)
        self.msise = dict(
            nn=np.zeros((n)),  # in km/m3
            N2=np.zeros((n)),  # in /m3
            O2=np.zeros((n)),  # in /m3
            O=np.zeros((n)),  # in /m3
            He=np.zeros((n)),  # in /m3
            H=np.zeros((n)),  # in /m3
            Ar=np.zeros((n)),  # in /m3
            N=np.zeros((n)),  # in /m3
            O_Anomalous=np.zeros((n)),  # in /m3
            NO=np.zeros((n)),  # in /m3
            t_nn=np.zeros((n)),  # in /m3
            Tn=np.zeros((n)),  # in K
        )
        logger.info(f"Running pymsise00 on {self.date}")
        for lat, lon, alt, j in zip(self.lats, self.lons, self.alts, range(n)):
            x = pymsis.calculate([self.date], [lat], [lon], [alt])
            for i, key in enumerate(keys):
                self.msise[key][j] = x[0, i]
            self.msise["t_nn"][j] = np.nansum(x[0, 1:-2])
        return


if __name__ == "__main__":
    msise = MSISE2d(
        dt.datetime(2024, 4, 8),
        np.array([0, 1, 3]),
        np.array([0, 1, 3]),
        np.array([100, 200, 300]),
    )
