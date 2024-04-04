# ==============================================================================
#       Import modules
# ==============================================================================
import argparse
from adflow import ADFLOW
from baseclasses import AeroProblem
from mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default=".")
parser.add_argument("--gridFile", type=str, default="INPUT/wing_vol.cgns")
args = parser.parse_args()

# ==============================================================================
#       Set up ADflow
# ==============================================================================
aeroOptions = {
    # I/O Parameters
    "gridFile": args.gridFile,
    "outputDirectory": args.output,
    "monitorvariables": ["resrho", "cl", "cd"],
    "writeTecplotSurfaceSolution": True,
    # Physics Parameters
    "equationType": "RANS",
    # Solver Parameters
    "smoother": "DADI",
    "MGCycle": "sg",
    # ANK Solver Parameters
    "useANKSolver": True,
    "ankswitchtol": 1e-1,
    # NK Solver Parameters
    "useNKSolver": True,
    "nkswitchtol": 1e-4,
    # Termination Criteria
    "L2Convergence": 1e-6,
    "nCycles": 1000,
}

# Create solver
CFDSolver = ADFLOW(options=aeroOptions)

# ==============================================================================
#       Set up AeroProblem
# ==============================================================================
ap = AeroProblem(name="wing", mach=0.85, altitude=5000, alpha=1.5, areaRef=45.5, chordRef=3.25, evalFuncs=["cl", "cd"])

# ==============================================================================
#       Solve for a specific CL
# ==============================================================================
W = 50000 * 9.81  # total aircraft weight in Newtons
n = 2.5  # load factor for 2.5g maneuver
Sref = ap.areaRef * 2  # total reference wing area
CLstar = W * n / Sref / ap.q  # desired CL for load condition
if MPI.COMM_WORLD.rank == 0:
    print("\nSolving for CL={:.5f}\n".format(CLstar))
CFDSolver.solveCL(ap, CLstar)

# ==============================================================================
#       Print functions and write force file
# ==============================================================================
funcs = {}
CFDSolver.evalFunctions(ap, funcs)
# Print the evaluated functions
if MPI.COMM_WORLD.rank == 0:
    print(funcs)

CFDSolver.writeForceFile("forces.txt")
