# rst Imports
from pyhyp import pyHyp

# rst general

# Front wing vol mesh
options_front = {
    # ---------------------------
    #   General options
    # ---------------------------
    "inputFile": "wing.cgns",
    "fileType": "CGNS",
    "unattachedEdgesAreSymmetry": True,
    "outerFaceBC": "overset",
    "autoConnect": True,
    "BC": {},
    "families": "wing_front",
    # rst grid
    # ---------------------------
    #   Grid Parameters
    # ---------------------------
    "N": 33,
    "s0": 3e-5,
    "marchDist": 0.4,
    "coarsen": 2,
    # rst rest
    # ---------------------------
    #   Pseudo Grid Parameters
    # ---------------------------
    "ps0": -1.0,
    "pGridRatio": -1.0,
    "cMax": 1.0,
    # ---------------------------
    #   Smoothing parameters
    # ---------------------------
    "epsE": 1.0,
    "epsI": 2.0,
    "theta": 3.0,
    "volCoef": 0.2,
    "volBlend": 0.0005,
    "volSmoothIter": 20,
    # ---------------------------
    #   Solution Parameters
    # ---------------------------
    "kspRelTol": 1e-10,
    "kspMaxIts": 1500,
    "kspSubspaceSize": 50,
}

hyp = pyHyp(options=options_front)
hyp.run()
hyp.writeCGNS("wing_vol_front.cgns")

# rst front_end

# Back wing vol mesh
options_back = {
    # ---------------------------
    #   General options
    # ---------------------------
    "inputFile": "wing.cgns",
    "fileType": "cgns",
    "unattachedEdgesAreSymmetry": True,
    "outerFaceBC": "overset",
    "autoConnect": True,
    "BC": {},
    "families": "wing_back",
    # ---------------------------
    #   Grid Parameters
    # ---------------------------
    "N": 33,
    "s0": 3e-5,
    "marchDist": 0.4,
    "coarsen": 2,
    # ---------------------------
    #   Pseudo Grid Parameters
    # ---------------------------
    "ps0": -1.0,
    "pGridRatio": -1.0,
    "cMax": 1.0,
    # ---------------------------
    #   Smoothing parameters
    # ---------------------------
    "epsE": 1.0,
    "epsI": 2.0,
    "theta": 3.0,
    "volCoef": 0.2,
    "volBlend": 0.0005,
    "volSmoothIter": 20,
    # ---------------------------
    #   Solution Parameters
    # ---------------------------
    "kspRelTol": 1e-10,
    "kspMaxIts": 1500,
    "kspSubspaceSize": 50,
}

hyp = pyHyp(options=options_back)
hyp.run()
hyp.writeCGNS("wing_vol_back.cgns")

# rst end
