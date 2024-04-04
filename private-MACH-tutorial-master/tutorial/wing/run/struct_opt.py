# rst Init (begin)
# ==============================================================================
#         Import modules
# ==============================================================================
import argparse
import ast
import os
from mpi4py import MPI
from baseclasses import StructProblem
from pyoptsparse import Optimization, OPT, History
from SETUP import setup_tacs
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, default="output")
parser.add_argument("--bdfFile", type=str, default="INPUT/wingbox.bdf")
parser.add_argument("--optOptions", type=ast.literal_eval, default={}, help="additional optimizer options to be added")
parser.add_argument("--noPlot", action="store_true", help="disable plotting")
args = parser.parse_args()
comm = MPI.COMM_WORLD
if not os.path.exists(args.output):
    if comm.rank == 0:
        os.mkdir(args.output)
# ==============================================================================
#       Initialize TACS
# ==============================================================================
FEASolver = setup_tacs.setup(args.bdfFile, args.output)

# ==============================================================================
#       Set up structural problem
# ==============================================================================
dispFuncs = FEASolver.functionList
objConFuncs = ["TotalMass"] + [f for f in dispFuncs if "KSFailure" in f]
sp = StructProblem("2.5g", loadFile="INPUT/forces.txt", loadFactor=2.5, evalFuncs=dispFuncs)

# Add inertial (gravity) loads
FEASolver.addInertialLoad(sp)

# Add some adjacency constraints between skin, spar and stringer thicknesses
FEASolver.addAdjacencyConstraints(delta=5e-3, include=["SKIN", "SPAR", "STRING"])

# rst Init (end)
# ==============================================================================
#       Set up optimization
# ==============================================================================
def obj(x):
    funcs = {}
    FEASolver.setDesignVars(x)
    FEASolver(sp)
    FEASolver.evalFunctions(sp, funcs)
    if comm.rank == 0:
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
    return funcs


def sens(x, funcs):
    funcsSens = {}
    FEASolver.evalFunctionsSens(sp, funcsSens, evalFuncs=objConFuncs)
    return funcsSens


# rst Funcs (end)
# Set up the optimization problem
optProb = Optimization("Mass minimization", obj)
optProb.addObj("2.5g_TotalMass")
FEASolver.addVariablesPyOpt(optProb)
FEASolver.addConstraintsPyOpt(optProb)

for f in FEASolver.functionList:
    if "KSFailure" in f:
        optProb.addCon(f"{sp.name}_{f}", upper=1.0)

if comm.rank == 0:
    print(optProb)
optProb.printSparsity()

optOptions = {
    "Major step limit": 0.5,
    "Hessian full memory": None,
    "Hessian frequency": 20,
    "Print file": os.path.join(args.output, "SNOPT_print.out"),
    "Summary file": os.path.join(args.output, "SNOPT_summary.out"),
}
optOptions.update(args.optOptions)
opt = OPT("snopt", options=optOptions)
sol = opt(optProb, sens=sens, storeHistory=os.path.join(args.output, "struct.hst"))

# rst Post (start)
# Write the final solution
FEASolver.writeOutputFile(os.path.join(args.output, sp.name + "_final.f5"))

if comm.rank == 0 and not args.noPlot:
    # load the optimisation history
    optHist = History(os.path.join(args.output, "struct.hst"))
    histValues = optHist.getValues()

    # Plot Feasibility, optimality, wingbox mass and failure constraints over optimisation history
    fig, axes = plt.subplots(nrows=3, sharex=True, constrained_layout=True, figsize=(14, 10))

    axes[0].plot("nMajor", "optimality", data=histValues, label="Optimality")
    axes[0].plot("nMajor", "feasibility", data=histValues, label="Feasibility")
    axes[0].set_yscale("log")
    axes[0].axhline(1e-6, linestyle="--", color="gray")
    axes[0].annotate("Convergence Criteria", xy=(10, 1e-6), ha="left", va="top", fontsize=24, color="gray")
    axes[0].legend(fontsize=20, labelcolor="linecolor", loc="upper right", frameon=False)
    axes[0].autoscale(enable=True, tight=True)

    for f in histValues.keys():
        if "mass" in f.lower():
            legName = f.replace("2.5g_", "").replace("Mass", "")
            axes[1].plot("nMajor", f, data=histValues, label=legName)
        if "ksfailure" in f.lower():
            legName = f.replace("2.5g_", "").replace("KSFailure", "")
            axes[2].plot("nMajor", f, data=histValues, label=legName)

    axes[1].legend(fontsize=20, labelcolor="linecolor", loc="upper right", frameon=False, ncol=3)
    axes[2].legend(fontsize=20, labelcolor="linecolor", loc="upper right", frameon=False, ncol=3)
    axes[1].autoscale(enable=True, tight=True)
    axes[2].autoscale(enable=True, tight=True)

    axes[1].set_ylabel("Mass\n(kg)", rotation="horizontal", ha="right", fontsize=24)
    axes[2].set_ylabel("Failure\nConstraint", rotation="horizontal", ha="right", fontsize=24)
    axes[2].set_xlabel("Major Iterations", fontsize=24)
    axes[2].axhline(1, linestyle="--", color="gray")

    for ax in axes:
        ax.tick_params(axis="both", labelsize=20)

    plt.show()
