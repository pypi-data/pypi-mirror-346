"""
Constants used in the pyslammer package.

Attributes
----------
G_EARTH : float
    Acceleration due to gravity (m/s^2).
"""
G_EARTH = 9.80665 # Acceleration due to gravity (m/s^2).

FT_TO_IN = 12.0
FT_TO_M = 0.3048
FT3_TO_IN3 = FT_TO_IN**3
CM_TO_FT = 0.032808399
CM_TO_IN = CM_TO_FT * FT_TO_IN
M_TO_CM = 100.0
M_TO_FT = 3.28084
M3_TO_CM3 = M_TO_CM**3
LBFT3_TO_KNM3 = 6.3659
KNM3_TO_LBFT3 = 1 / LBFT3_TO_KNM3

BETA = 0.25
GAMMA = 0.5
