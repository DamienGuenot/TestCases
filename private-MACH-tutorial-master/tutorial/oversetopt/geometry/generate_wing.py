# rst start
import numpy
from pygeo import pyGeo

airfoil_list = ["NACA642A015.dat"] * 2
naf = len(airfoil_list)  # number of airfoils

# Airfoil leading edge positions
x = [0.0, 0.0]
y = [0.0, 0.0]
z = [0.0, 0.64]
# x-y offset applied to airfoil position before scaling
offset = numpy.zeros((naf, 2))

# Airfoil rotations
rot_x = [0.0, 0.0]
rot_y = [0.0, 0.0]
rot_z = [0.0, 0.0]

# Airfoil scaling
chord = [0.24, 0.24]  # chord lengths

wing = pyGeo(
    "liftingSurface",
    xsections=airfoil_list,
    scale=chord,
    offset=offset,
    x=x,
    y=y,
    z=z,
    rotX=rot_x,
    rotY=rot_y,
    rotZ=rot_z,
    tip="rounded",
    bluntTe=True,
    squareTeTip=True,
    teHeight=0.001,
)

wing.writeTecplot("wing.dat")

wing.writeTin("wing.tin")
# rst end
