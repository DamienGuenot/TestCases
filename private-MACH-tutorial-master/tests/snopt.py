from pyoptsparse import Optimization, OPT, History
#
optOptions = {
    "Major step limit": 0.5,
    "Hessian full memory": None,
    "Hessian frequency": 20,
    "Print file": "SNOPT_print.out",
    "Summary file": "SNOPT_summary.out",
}
opt = OPT("snopt", options=optOptions)
