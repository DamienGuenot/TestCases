# rst start
from baseclasses import AeroProblem
from adflow import ADFLOW

# from mpi4py import MPI
# import shutil
# import collections

# ======================================================================
#         Input Information
# ======================================================================

# File name of the mesh
gridFile = "overset_combined.cgns"

# Common aerodynamic problem description and design variables
ap = AeroProblem(name="ihc_check", mach=0.3, altitude=1000, areaRef=0.24 * 0.64 * 2, chordRef=0.24)

# dictionary with name of the zone as a key and a factor to multiply it with.
oversetpriority = {}

aeroOptions = {
    # Common Parameters
    "gridFile": gridFile,
    "outputDirectory": "./",
    "mgcycle": "sg",
    "volumevariables": ["blank"],
    "surfacevariables": ["blank"],
    # Physics Parameters
    "equationType": "RANS",
    # Debugging parameters
    "debugzipper": False,
    "usezippermesh": False,
    "nrefine": 10,  # number of times to run IHC cycle
    "nearwalldist": 0.1,
    "oversetpriority": oversetpriority,
}

# Create solver
CFDSolver = ADFLOW(options=aeroOptions, debug=False)

# Uncoment this if just want to check flooding
CFDSolver.setAeroProblem(ap)

name = ".".join(gridFile.split(".")[0:-1])
CFDSolver.writeVolumeSolutionFile(name + "_IHC.cgns", writeGrid=True)
# rst end
