# rst start initialize-TACS
# ==============================================================================
#       Import modules
# ==============================================================================
import argparse
import numpy
import os
from baseclasses import StructProblem
from mpi4py import MPI
from SETUP import setup_tacs

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="ouput")
parser.add_argument("--bdfFile", type=str, default="INPUT/wingbox.bdf")
args = parser.parse_args()
comm = MPI.COMM_WORLD
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)

# ==============================================================================
#       Initialize TACS
# ==============================================================================
FEASolver = setup_tacs.setup(args.bdfFile, args.output)
# rst end initialize-TACS
# ==============================================================================
#       Set up structural problem
# ==============================================================================
sp = StructProblem("2.5gload", loadfile="forces.txt", loadFactor=2.5, evalFuncs=FEASolver.functionList.keys())
# rst end structProblem
# ==============================================================================
#       Add loads
# ==============================================================================
# Add distributed load to tip rib
F = numpy.array([0.0, 3e5, 0.0])  # N
FEASolver.addLoadToComponents(sp, FEASolver.selectCompIDs(["RIB.18"]), F=F)

# Add pressure load (10 kPa) acting upward on the lower skin of the wing
FEASolver.addPressureLoad(sp, -10e3, include="L_SKIN")

# Add inertial (gravity) loads
FEASolver.addInertialLoad(sp)
# rst end loads
# ==============================================================================
#       Evaluate functions
# ==============================================================================
FEASolver(sp)
funcs = {}
FEASolver.evalFunctions(sp, funcs)


if MPI.COMM_WORLD.rank == 0:
    print("\n\n\n--------")
    print("RESULTS:")
    print("--------")
    for funcType in ["Mass", "KSFailure", "MaxFailure"]:
        print(f"\n{funcType} Functions:")
        print("------------------------")
        for f in funcs:
            if funcType in f:
                print(f"{f:30s}: {funcs[f]:6f}")
    print("--------------------------------------\n\n\n")

# Write the final solution
FEASolver.writeOutputFile(args.output + "/" + sp.name + "_final.f5")

# FEASolver.writeDisplacementsFile(sp, "disp.txt")
# rst end evalFuncs
