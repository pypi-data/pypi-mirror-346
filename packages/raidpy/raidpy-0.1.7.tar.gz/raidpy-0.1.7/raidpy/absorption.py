#!/usr/bin/env python

"""absorption.py: absorption is dedicated to absorption related function."""

__author__ = "Chakraborty, S."
__copyright__ = "Chakraborty, S."
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "chakras4@erau.edu"
__status__ = "Research"

import math
from dataclasses import dataclass

import numpy as np
from loguru import logger
from scipy.integrate import quad

from raidpy.collision import Collision
from raidpy.constants import *


# ===================================================================================
# These are special function dedicated to the Sen-Wyller absorption calculation.
#
# Sen, H. K., and Wyller, A. A. ( 1960), On the Generalization of Appleton-Hartree magnetoionic Formulas
# J. Geophys. Res., 65( 12), 3931- 3950, doi:10.1029/JZ065i012p03931.
#
# ===================================================================================
def C(p, y):

    def gamma_factorial(N):
        n = int(str(N).split(".")[0])
        f = N - n
        if f > 0.0:
            fact = math.factorial(n) * math.gamma(f)
        else:
            fact = math.factorial(n)
        return fact

    func = lambda t: t**p * np.exp(-t) / (t**2 + y**2)
    cy, _ = quad(func, 0, np.inf)
    return cy / gamma_factorial(p)


def calculate_sw_RL(Bo, Ne, nu, fo=30e6, nu_sw_r=1.0):
    if (
        Ne > 0.0
        and Bo > 0.0
        and nu > 0.0
        and (not np.isnan(Ne))
        and (not np.isnan(Bo))
        and (not np.isnan(nu))
    ):
        k = (2 * np.pi * fo) / pconst["c"]
        w = 2 * np.pi * fo
        nu_sw = nu * nu_sw_r
        wh = pconst["q_e"] * Bo / pconst["m_e"]
        yo, yx = (w + wh) / nu_sw, (w - wh) / nu_sw
        nL = 1 - (
            (Ne * pconst["q_e"] ** 2 / (2 * pconst["m_e"] * w * pconst["eps0"] * nu_sw))
            * np.complex_(yo * C(1.5, yo) + (1j * 2.5 * C(2.5, yo)))
        )
        nR = 1 - (
            (Ne * pconst["q_e"] ** 2 / (2 * pconst["m_e"] * w * pconst["eps0"] * nu_sw))
            * np.complex_(yx * C(1.5, yx) + (1j * 2.5 * C(2.5, yx)))
        )
        R, L = np.abs(nR.imag * 8.68 * k * 1e3), np.abs(nL.imag * 8.68 * k * 1e3)
    else:
        R, L = np.nan, np.nan
    return R, L


def calculate_sw_OX(Bo, Ne, nu, fo=30e6, nu_sw_r=1.0):
    if (
        Ne > 0.0
        and Bo > 0.0
        and nu > 0.0
        and (not np.isnan(Ne))
        and (not np.isnan(Bo))
        and (not np.isnan(nu))
    ):
        k = (2 * np.pi * fo) / pconst["c"]
        w = 2 * np.pi * fo
        nu_sw = nu * nu_sw_r
        wh = pconst["q_e"] * Bo / pconst["m_e"]
        wo2 = Ne * pconst["q_e"] ** 2 / (pconst["m_e"] * pconst["eps0"])
        yo, yx = (w) / nu_sw, (w) / nu_sw
        y = (w) / nu_sw

        ajb = (wo2 / (w * nu_sw)) * ((y * C(1.5, y)) + 1.0j * (2.5 * C(2.5, y)))
        c = (wo2 / (w * nu_sw)) * yx * C(1.5, yx)
        d = 2.5 * (wo2 / (w * nu_sw)) * C(1.5, yx)
        e = (wo2 / (w * nu_sw)) * yo * C(1.5, yo)
        f = 2.5 * (wo2 / (w * nu_sw)) * C(1.5, yo)

        eI = 1 - ajb
        eII = 0.5 * ((f - d) + (c - e) * 1.0j)
        eIII = ajb - (0.5 * ((c + e) + 1.0j * (d + f)))

        Aa = 2 * eI * (eI + eIII)
        Bb = (eIII * (eI + eII)) + eII**2
        Cc = 2 * eI * eII
        Dd = 2 * eI
        Ee = 2 * eIII

        nO = np.sqrt(Aa / (Dd + Ee))
        nX = np.sqrt((Aa + Bb) / (Dd + Ee))
        O, X = np.abs(nO.imag * 8.68 * k * 1e3), np.abs(nX.imag * 8.68 * k * 1e3)
    else:
        O, X = np.nan, np.nan
    return O, X


@dataclass
class Absorption:
    mode_O: np.array = None
    mode_X: np.array = None
    mode_R: np.array = None
    mode_L: np.array = None
    mode_n: np.array = None


@dataclass
class AppletonHartree:
    ft: Absorption = None
    sn: Absorption = None
    av_cc: Absorption = None
    av_mb: Absorption = None

    @staticmethod
    def init():
        ah = AppletonHartree()
        (ah.ft, ah.sn, ah.av_cc, ah.av_mb) = (
            Absorption(),
            Absorption(),
            Absorption(),
            Absorption(),
        )
        return ah


@dataclass
class SenWyller:
    ft: Absorption = None

    @staticmethod
    def init():
        sw = SenWyller()
        sw.ft = Absorption()
        return sw


# ===================================================================================
# This class is used to estimate O,X,R & L mode absorption height profile.
# ===================================================================================
class CalculateAbsorption(object):
    """
    This class is used to estimate O,X,R & L mode absorption height profile.

    Bo = geomagnetic field
    coll = collision frequency
    Ne = electron density
    fo = operating frequency
    """

    def __init__(
        self, iri: dict, igrf: dict, coll: Collision, fo: float = 30e6, _run_=False
    ):
        self.igrf = igrf
        self.iri = iri
        self.coll = coll
        self.fo = fo
        self.w = 2 * np.pi * fo
        self.k = (2 * np.pi * fo) / pconst["c"]
        if _run_:
            logger.info(f"Running absorption calculations....")
            self.ah = AppletonHartree.init()
            self.sw = SenWyller.init()
            self.estimate_ah()
            self.estimate_sw()
        return

    def estimate_ah(self):
        # =========================================================
        # Using FT collision frequency
        # =========================================================
        X, Z = (
            (self.iri["edens"] * pconst["q_e"] ** 2)
            / (pconst["eps0"] * pconst["m_e"] * self.w**2),
            self.coll.nu_ft / self.w,
        )
        x, jz = X, Z * 1.0j
        n = np.sqrt(1 - (x / (1 - jz)))
        self.ah.ft.no = np.abs(8.68 * self.k * 1e3 * n.imag)

        YL, YT = 0, (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w)
        nO, nX = (
            np.sqrt(1 - (x / (1 - jz))),
            np.sqrt(
                1
                - (
                    (2 * x * (1 - x - jz))
                    / ((2 * (1 - x - jz) * (1 - jz)) - (2 * YT**2))
                )
            ),
        )
        self.ah.ft.mode_O, self.ah.ft.mode_X = (
            np.abs(8.68 * self.k * 1e3 * nO.imag),
            np.abs(8.68 * self.k * 1e3 * nX.imag),
        )

        YL, YT = (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w), 0
        nL, nR = np.sqrt(1 - (x / ((1 - jz) + YL))), np.sqrt(1 - (x / ((1 - jz) - YL)))
        self.ah.ft.mode_R, self.ah.ft.mode_L = (
            np.abs(8.68 * self.k * 1e3 * nR.imag),
            np.abs(8.68 * self.k * 1e3 * nL.imag),
        )

        # ========================================================
        # Using SN collision frequency  quite_model
        # ========================================================
        Z = self.coll.nu_sn.total / self.w
        jz = Z * 1.0j
        n = np.sqrt(1 - (x / (1 - jz)))
        self.ah.sn.no = np.abs(8.68 * self.k * 1e3 * n.imag)

        YL, YT = 0, (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w)
        nO, nX = (
            np.sqrt(1 - (x / (1 - jz))),
            np.sqrt(
                1
                - (
                    (2 * x * (1 - x - jz))
                    / ((2 * (1 - x - jz) * (1 - jz)) - (2 * YT**2))
                )
            ),
        )
        self.ah.sn.mode_O, self.ah.sn.mode_X = (
            np.abs(8.68 * self.k * 1e3 * nO.imag),
            np.abs(8.68 * self.k * 1e3 * nX.imag),
        )

        YL, YT = (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w), 0
        nL, nR = np.sqrt(1 - (x / ((1 - jz) + YL))), np.sqrt(1 - (x / ((1 - jz) - YL)))
        self.ah.sn.mode_R, self.ah.sn.mode_L = (
            np.abs(8.68 * self.k * 1e3 * nR.imag),
            np.abs(8.68 * self.k * 1e3 * nL.imag),
        )

        # =========================================================
        # Using AV_CC collision frequency quite_model
        # =========================================================
        Z = self.coll.nu_av_cc / self.w
        jz = Z * 1.0j
        n = np.sqrt(1 - (x / (1 - jz)))
        self.ah.av_cc.no = np.abs(8.68 * self.k * 1e3 * n.imag)

        YL, YT = (0, (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w))
        nO, nX = (
            np.sqrt(1 - (x / (1 - jz))),
            np.sqrt(
                1
                - (
                    (2 * x * (1 - x - jz))
                    / ((2 * (1 - x - jz) * (1 - jz)) - (2 * YT**2))
                )
            ),
        )
        self.ah.av_cc.mode_O, self.ah.av_cc.mode_X = (
            np.abs(8.68 * self.k * 1e3 * nO.imag),
            np.abs(8.68 * self.k * 1e3 * nX.imag),
        )

        YL, YT = (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w), 0
        nL, nR = np.sqrt(1 - (x / ((1 - jz) + YL))), np.sqrt(1 - (x / ((1 - jz) - YL)))
        self.ah.av_cc.mode_R, self.ah.av_cc.mode_L = (
            np.abs(8.68 * self.k * 1e3 * nR.imag),
            np.abs(8.68 * self.k * 1e3 * nL.imag),
        )

        # =========================================================
        # Using AV_MB collision frequency quite_model
        # =========================================================
        Z = self.coll.nu_av_mb / self.w
        jz = Z * 1.0j
        n = np.sqrt(1 - (x / (1 - jz)))
        self.ah.av_mb.no = np.abs(8.68 * self.k * 1e3 * n.imag)

        YL, YT = 0, (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w)
        nO, nX = (
            np.sqrt(1 - (x / (1 - jz))),
            np.sqrt(
                1
                - (
                    (2 * x * (1 - x - jz))
                    / ((2 * (1 - x - jz) * (1 - jz)) - (2 * YT**2))
                )
            ),
        )
        self.ah.av_mb.mode_O, self.ah.av_mb.mode_X = (
            np.abs(8.68 * self.k * 1e3 * nO.imag),
            np.abs(8.68 * self.k * 1e3 * nX.imag),
        )

        YL, YT = (pconst["q_e"] * self.igrf["total"]) / (pconst["m_e"] * self.w), 0
        nL, nR = (
            np.sqrt(1 - (x / ((1 - jz) + YL))),
            np.sqrt(1 - (x / ((1 - jz) - YL))),
        )
        self.ah.av_mb.mode_R, self.ah.av_mb.mode_L = (
            np.abs(8.68 * self.k * 1e3 * nR.imag),
            np.abs(8.68 * self.k * 1e3 * nL.imag),
        )
        return

    def estimate_sw(self):
        Bo = self.igrf["total"]
        n = len(Bo)
        # ===================================================
        # Using FT collistion frequency
        # ===================================================
        nu = self.coll.nu_ft
        (
            self.sw.ft.mode_O,
            self.sw.ft.mode_X,
            self.sw.ft.mode_R,
            self.sw.ft.mode_L,
            self.sw.ft.mode_no,
        ) = (
            np.zeros_like(Bo),
            np.zeros_like(Bo),
            np.zeros_like(Bo),
            np.zeros_like(Bo),
            np.zeros_like(Bo),
        )
        for i in range(n):
            self.sw.ft.mode_O[i], self.sw.ft.mode_X[i] = calculate_sw_OX(
                Bo[i], self.iri["edens"][i], nu[i], self.fo
            )
            self.sw.ft.mode_R[i], self.sw.ft.mode_L[i] = calculate_sw_RL(
                Bo[i], self.iri["edens"][i], nu[i], self.fo
            )
        return
