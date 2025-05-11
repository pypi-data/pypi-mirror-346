#!/usr/bin/env python

"""iri.py: Calculate IRI object along the path"""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"


import datetime as dt

import iricore
import numpy as np
from loguru import logger


class IRI2d(object):
    """
    This function calculate thermospheric plsama densitites along the path.

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
        iri_version: int = 20,
    ):
        self.date = date
        self.lats = lats
        self.lons = lons
        self.alts = alts
        self.iri_version = iri_version
        self.compute()
        return

    def compute(
        self,
    ):
        """
        Run IGRF codes
        """
        logger.info(f"Running IRI-{self.iri_version} on {self.date}")
        n = len(self.alts)
        self.iri = dict(
            edens=np.zeros((n)),  # Electron density in [m-3]
            ntemp=np.zeros((n)),  # Neutral temperature in [K]
            itemp=np.zeros((n)),  # Ion temperature in [K]
            etemp=np.zeros((n)),  # Electron temperature in [K]
            o=np.zeros((n)),  # O+ ion density in [%](default) or [m-3]
            h=np.zeros((n)),  # H+ ion density in [%](default) or [m-3].
            he=np.zeros((n)),  # He+ ion density in [%](default) or [m-3].
            o2=np.zeros((n)),  # O2+ ion density in [%](default) or [m-3].
            no=np.zeros((n)),  # NO+ ion density in [%](default) or [m-3].
            cluster=np.zeros((n)),  # Cluster ion density in [%](default) or [m-3].
            n=np.zeros((n)),  # N+ ion density in [%](default) or [m-3].
        )
        for lat, lon, alt, j in zip(self.lats, self.lons, self.alts, range(n)):
            alt_range = [alt, alt, 1]
            iriout = iricore.iri(
                self.date,
                alt_range,
                lat,
                lon,
                self.iri_version,
            )
            for i, key in enumerate(self.iri.keys()):
                self.iri[key][j] = getattr(iriout, key)
        return


if __name__ == "__main__":
    iri = IRI2d(
        dt.datetime(2024, 4, 8),
        np.array([0, 1, 3]),
        np.array([0, 1, 3]),
        np.array([100, 200, 300]),
    )
