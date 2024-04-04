# rst init (begin)
# ==============================================================================
# Import modules
# ==============================================================================
import os
import argparse
import ast
from pprint import pprint
from mpi4py import MPI
from baseclasses import AeroProblem, StructProblem, AeroStructProblem
from multipoint import multiPointSparse#, redirectIO
from pyaerostructure import TACSLDTransfer, AeroStruct
from pyoptsparse import Optimization, OPT

from SETUP import setup_dvgeo, setup_dvcon, setup_tacs, setup_adflow, setup_warp

# ==============================================================================
# Input Information
# ==============================================================================
# Use Python's built-in Argument parser to get commandline options
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output")
parser.add_argument("--gridFile", type=str, default="INPUT/wing_vol.cgns")
parser.add_argument("--bdfFile", type=str, default="INPUT/wingbox.bdf")
parser.add_argument("--shape", action="store_true")
parser.add_argument("--npcruise", type=int, default=2)
parser.add_argument("--npmaneuver", type=int, default=2)
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
parser.add_argument("--structHistFile", type=str, default=None)
args = parser.parse_args()

outputDirectory = args.output
files = {
    "ffdFile": "INPUT/ffd.xyz",
    "gridFile": args.gridFile,
    "bdfFile": args.bdfFile,
}

# ==============================================================================
# Aircraft Data
# ==============================================================================
TOW = 121000  # Aircraft takeoff weight in lbs
Wref = TOW / 2.20462 / 2 * 9.81  # half body weight in Newtons
Sref = 45.5  # half-wing in m^2
chordRef = 3.25  # meters
# rst init (end)
# ==============================================================================
# Processor allocation
# ==============================================================================
#  Create multipoint communication object
MP = multiPointSparse(MPI.COMM_WORLD)
MP.addProcessorSet("cruise", nMembers=1, memberSizes=args.npcruise)
MP.addProcessorSet("maneuver", nMembers=1, memberSizes=args.npmaneuver)
comm, setComm, setFlags, groupFlags, ptID = MP.createCommunicators()

# Extract setName on each processor for convenience and create all directories
setName = MP.getSetName()
ptDirs = MP.createDirectories(args.output)
# rst alloc (end)

# Create a directory for all standard output
stdoutDir = os.path.join(args.output, "stdout")
if MP.gcomm.rank == 0:
    os.system("mkdir -p %s" % stdoutDir)
MP.gcomm.barrier()
if comm.rank == 0:
    fName = os.path.join(stdoutDir, "%s_%d.out" % (setName, ptID))
    outFile = open(fName, "w")
    #redirectIO(outFile)
# rst io (end)
# ==============================================================================
# Set up case problems
# ==============================================================================
# Setup cruise problems
cruiseProblems = []
ap = AeroProblem(
    name="cruise",
    mach=0.8,
    altitude=10000,
    areaRef=Sref,
    alpha=2.0,
    chordRef=chordRef,
    evalFuncs=["lift", "drag"],
)
ap.addDV("alpha", lower=0, upper=10.0, scale=0.1)
sp = StructProblem(ap.name, evalFuncs=["TotalMass"])
cruiseProblems.append(AeroStructProblem(ap, sp))

# Setup maneuver problems
maneuverProblems = []  # List of maneuver AeroStruct problem objects
ap = AeroProblem(
    name="maneuver",
    mach=0.75,
    altitude=5000,
    areaRef=Sref,
    alpha=2.0,
    chordRef=chordRef,
    evalFuncs=["lift"],
)
ap.addDV("alpha", lower=0, upper=10.0, scale=0.1)
sp = StructProblem(ap.name, evalFuncs=["ks0", "ks1", "ks2"], loadFactor=2.5)
maneuverProblems.append(AeroStructProblem(ap, sp))
# rst cases setup (end)
# ==============================================================================
# Geometric Design Variable Set-up
# ==============================================================================
# line that calls the setup_geometry func which returns a DvGeometry object called DVGeo
DVGeo = setup_dvgeo.setup(args, comm, files)

# ==============================================================================
# Set up aerodynamic analysis
# ==============================================================================
CFDSolver = setup_adflow.setup(comm, files, ptDirs[setName][ptID])
mesh = setup_warp.setup(comm, files)
CFDSolver.setMesh(mesh)
CFDSolver.setDVGeo(DVGeo)

# ==============================================================================
# Set up structural analysis
# ==============================================================================
# line that calls the setup func with FEAsolver object as input and returns the modified object
FEASolver = setup_tacs.setup(files["bdfFile"], args.output, comm)
FEASolver.setDVGeo(DVGeo)

for ASP in cruiseProblems + maneuverProblems:
    FEASolver.addInertialLoad(ASP.SP)

# Add some adjacency constraints between skin, spar and stringer thicknesses
FEASolver.addAdjacencyConstraints(delta=5e-3, include=["SKIN", "SPAR", "STRING"])

# ==============================================================================
# Set up aerostructural analysis
# ==============================================================================
mdOptions = {
    # Tolerances
    "relTol": 1e-5,
    "adjointRelTol": 1e-5,
    # Output Options
    "outputDir": ptDirs[setName][ptID],
    "saveIterations": True,
    # Solution Options
    "damp0": 0.5,
    "nMDIter": 25,
    "MDSolver": "GS",
    "MDSubSpaceSize": 40,
    # Adjoint options
    "adjointSolver": "KSP",
    "nadjointiter": 15,
    # Monitor Options
    "monitorVars": ["cl", "cd", "lift", "norm_u", "damp"],
}

transferOptions = {}

# Create transfer object
transfer = TACSLDTransfer(CFDSolver, FEASolver, comm, options=transferOptions)

# Create the final aerostructural solver
AS = AeroStruct(CFDSolver, FEASolver, transfer, comm, options=mdOptions)

# ==============================================================================
# DVConstraint Setup
# ==============================================================================
# line that calls the setup_constraints func with args, CFDSolver, and comm as inputs, and returns DVConstraints obj DVCon as output
DVCon = setup_dvcon.setup(args, comm, DVGeo, CFDSolver)
# rst setups (end)
# ==============================================================================
# Analysis and Sensitivity Functions
# ==============================================================================

# --- Define the functions whose we calculate the sensitivities of
dispFuncs = FEASolver.functionList.keys()
objConFuncs = ["lift"]
if setName == "cruise":
    objConFuncs += ["TotalMass", "drag"]
elif setName == "maneuver":
    objConFuncs += [f for f in dispFuncs if "KSFailure" in f]


def cruiseObj(x):
    if comm.rank == 0:
        print("Design Variables")
        pprint(x)
    funcs = {}
    DVGeo.setDesignVars(x)
    DVCon.evalFunctions(funcs)
    FEASolver.setDesignVars(x)
    for i in range(len(cruiseProblems)):
        cp = cruiseProblems[i]
        cp.setDesignVars(x)
        AS(cp)
        AS.evalFunctions(cp, funcs, evalFuncs=objConFuncs)
        AS.checkSolutionFailure(cp, funcs)
    if comm.rank == 0:
        print("Cruise functions")
        pprint(funcs)
    return funcs


def cruiseSens(x, funcs):
    funcsSens = {}
    for i in range(len(cruiseProblems)):
        cp = cruiseProblems[i]
        AS.evalFunctionsSens(cp, funcsSens, evalFuncs=objConFuncs)
        AS.checkAdjointSolutionFailure(cp, funcsSens)
    DVCon.evalFunctionsSens(funcsSens)
    return funcsSens


def maneuverObj(x):
    if comm.rank == 0:
        print("Design Variables")
        pprint(x)
    funcs = {}
    DVGeo.setDesignVars(x)
    FEASolver.setDesignVars(x)
    for i in range(len(maneuverProblems)):
        mp = maneuverProblems[i]
        mp.setDesignVars(x)
        AS(mp)
        AS.evalFunctions(mp, funcs, evalFuncs=objConFuncs)
        AS.checkSolutionFailure(mp, funcs)
    if comm.rank == 0:
        print("Maneuver functions")
        pprint(funcs)
    return funcs


def maneuverSens(x, funcs):
    funcsSens = {}
    for i in range(len(maneuverProblems)):
        mp = maneuverProblems[i]
        AS.evalFunctionsSens(mp, funcsSens, evalFuncs=objConFuncs)
        AS.checkAdjointSolutionFailure(mp, funcsSens)
    return funcsSens


def objCon(funcs, printOK):
    funcs["obj"] = funcs["cruise_drag"] + funcs["cruise_TotalMass"] * 2
    funcs["cruise_lift_con"] = funcs["cruise_lift"] - Wref
    funcs["maneuver_lift_con"] = funcs["maneuver_lift"] - Wref * 2.5
    if printOK:
        pprint(funcs)
    return funcs


# rst funcs (end)
# ==============================================================================
# Optimization Problem Setup
# ==============================================================================
# Setup Optimization Problem
optProb = Optimization("Basic Aero-Structural Optimization", MP.obj)

# Add variables
DVGeo.addVariablesPyOpt(optProb)
FEASolver.addVariablesPyOpt(optProb)
for i in range(len(cruiseProblems)):
    cruiseProblems[i].addVariablesPyOpt(optProb)
for i in range(len(maneuverProblems)):
    maneuverProblems[i].addVariablesPyOpt(optProb)
geoVars = list(DVGeo.getValues().keys())

# Add constraints
DVCon.addConstraintsPyOpt(optProb)
FEASolver.addConstraintsPyOpt(optProb)
optProb.addCon(
    "cruise_lift_con",
    lower=0.0,
    upper=0.0,
    scale=1.0 / Wref,
    wrt=["struct", "alpha_cruise"] + geoVars,
)
optProb.addCon(
    "maneuver_lift_con",
    lower=0.0,
    upper=0.0,
    scale=1.0 / Wref,
    wrt=["struct", "alpha_maneuver"] + geoVars,
)
for f in FEASolver.functionList:
    if "KSFailure" in f:
        optProb.addCon(f"{sp.name}_{f}", upper=1.0, wrt=["struct", "alpha_maneuver"] + geoVars)

# Objective:
optProb.addObj("obj", scale=1.0e-4)

# The MP object needs the 'obj' and 'sens' function for each proc set,
# the optimization problem and what the objcon function is:
MP.addProcSetObjFunc("cruise", cruiseObj)
MP.addProcSetSensFunc("cruise", cruiseSens)
MP.addProcSetObjFunc("maneuver", maneuverObj)
MP.addProcSetSensFunc("maneuver", maneuverSens)
MP.setObjCon(objCon)
MP.setOptProb(optProb)

# ==============================================================================
# Run optimization
# ==============================================================================
# Create optimizer
optOptions = {
    "Function precision": 1.0e-4,
    "Major feasibility tolerance": 1.0e-4,
    "Major optimality tolerance": 1.0e-4,
    "Difference interval": 1.0e-3,
    "Print file": os.path.join(outputDirectory, "SNOPT_print.out"),
    "Summary file": os.path.join(outputDirectory, "SNOPT_summary.out"),
}
optOptions.update(args.optOptions)
opt = OPT("snopt", options=optOptions)

# Load the optimized structural variables
if args.structHistFile is not None:
    optProb.setDVsFromHistory(args.structHistFile)

# Print Optimization Problem and sparsity
if comm.rank == 0:
    print(optProb)
optProb.printSparsity()

# Run Optimization
histFile = os.path.join(outputDirectory, "opt_hist.hst")
MP.gcomm.barrier()
sol = opt(optProb, MP.sens, storeHistory=histFile)
if comm.rank == 0:
    print(sol)
# rst end
