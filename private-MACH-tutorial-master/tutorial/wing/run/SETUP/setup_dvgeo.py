# ==============================================================================
# Import modules
# ==============================================================================
from pygeo import DVGeometry


def setup(args, comm, files):
    # ======================================================================
    #         Geometric Design Variable Set-up
    # ======================================================================
    # Create DVGeometry object
    DVGeo = DVGeometry(files["ffdFile"])

    # Create reference axis
    nRefAxPts = DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="k")
    nTwist = nRefAxPts - 1

    # Set up global design variables
    def twist(val, geo):
        for i in range(1, nRefAxPts):
            geo.rot_z["wing"].coef[i] = val[i - 1]

    DVGeo.addGeoDVGlobal(dvName="twist", value=[0] * nTwist, func=twist, lower=-10, upper=10, scale=1)

    if args.shape:
        # Set up local design variables
        DVGeo.addGeoDVLocal("local", lower=-0.5, upper=0.5, axis="y", scale=1)

    return DVGeo
