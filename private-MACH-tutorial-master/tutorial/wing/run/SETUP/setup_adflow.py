from adflow import ADFLOW


def setup(comm, files, outputDirectory):
    aeroOptions = {
        # I/O Parameters
        "gridFile": files["gridFile"],
        "outputDirectory": outputDirectory,
        "monitorvariables": ["resrho", "cl", "cd"],
        "setMonitor": False,
        "printTiming": False,
        "printIterations": False,
        "writeTecplotSurfaceSolution": True,
        # Physics Parameters
        "equationType": "RANS",
        # Solver Parameters
        "smoother": "DADI",
        "MGCycle": "sg",
        # ANK Solver Parameters
        "useANKSolver": True,
        "ankswitchtol": 1.0,
        "ankmaxiter": 80,
        "anklinearsolvetol": 0.05,
        "ankpcilufill": 2,
        "ankasmoverlap": 2,
        "ankcflexponent": 0.5,
        # NK Solver Parameters
        "useNKSolver": True,
        "nkswitchtol": 1e-4,
        # Termination Criteria
        "L2Convergence": 1e-10,
        "L2ConvergenceRel": 1e-1,
        "nCycles": 1000,
        # Adjoint Parameters
        "adjointL2Convergence": 1e-6,
        "adjointMaxIter": 2000,
    }

    # Create solver
    CFDSolver = ADFLOW(options=aeroOptions, comm=comm)
    return CFDSolver
