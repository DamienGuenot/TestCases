# ==============================================================================
#         Import modules
# ==============================================================================
# rst imports (start)
import argparse
import os
from mpi4py import MPI
from baseclasses import AeroProblem, StructProblem, AeroStructProblem
from pyaerostructure import AeroStruct, TACSLDTransfer
from SETUP import setup_tacs, setup_adflow, setup_warp

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output_as_run")
parser.add_argument("--gridFile", type=str, default="INPUT/wing_vol.cgns")
parser.add_argument("--bdfFile", type=str, default="INPUT/wingbox.bdf")
args = parser.parse_args()

files = {"gridFile": args.gridFile, "bdfFile": args.bdfFile}

comm = MPI.COMM_WORLD
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)
# rst imports (end)
# ==============================================================================
#         Set up case problems
# ==============================================================================
# rst ASP (start)
# Set up aerodynamic problem
ap = AeroProblem(
    name="cruise", mach=0.8, altitude=10000, areaRef=45.5, alpha=2.0, chordRef=3.25, evalFuncs=["lift", "drag"]
)

# Set up structural problem
sp = StructProblem(ap.name, evalFuncs=["mass"])

# Create aerostructural problem
asp = AeroStructProblem(ap, sp)
# rst ASP (end)
# ==============================================================================
#         Set up solvers
# ==============================================================================
# rst setup solver (start)
CFDSolver = setup_adflow.setup(comm, files, args.output)
mesh = setup_warp.setup(comm, files)
CFDSolver.setMesh(mesh)
FEASolver = setup_tacs.setup(files["bdfFile"], args.output, comm)
# rst setup solver (end)
# ==============================================================================
#         Set up aerostructural analysis
# ==============================================================================
# rst AS object (start)
transferOptions = {}
# Create transfer object
transfer = TACSLDTransfer(CFDSolver, FEASolver, comm, options=transferOptions)
mdOptions = {
    "outputDir": args.output,
    # Tolerances
    "relTol": 1e-5,
    "adjointRelTol": 1e-5,
    # Output Options
    "saveIterations": True,
    # Solution Options
    "damp0": 0.5,
    "nMDIter": 25,
    "MDSolver": "GS",
    "MDSubSpaceSize": 40,
    # Adjoint optoins
    "adjointSolver": "KSP",
    "nadjointiter": 15,
    # Monitor Options
    "monitorVars": ["cl", "cd", "lift", "norm_u", "damp"],
}
# Create the final aerostructural solver
AS = AeroStruct(CFDSolver, FEASolver, transfer, comm, options=mdOptions)
# rst AS object (end)
# ==============================================================================
#         Solve!
# ==============================================================================
# rst ASSolve (start)
# Solve the aerostructural problem
funcs = {}
AS(asp)
AS.evalFunctions(asp, funcs)
if comm.rank == 0:
    print(funcs)
# rst ASSolve (end)
# Also solve adjoints
funcsSens = {}
AS.evalFunctionsSens(asp, funcsSens)
AS.checkAdjointSolutionFailure(asp, funcsSens)
if comm.rank == 0:
    print(funcsSens)
# rst ASAdjoint (end)
