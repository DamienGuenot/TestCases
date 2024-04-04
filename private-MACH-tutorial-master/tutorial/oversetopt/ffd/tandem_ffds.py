# rst start
import numpy

# Front wing
# Bounding box for root airfoil
x_root_range = [-0.02, 0.27]
y_root_range = [-0.05, 0.05]
z_root = -0.01

# Bounding box for tip airfoil
x_tip_range = [-0.02, 0.27]
y_tip_range = [-0.05, 0.05]
z_tip = 0.67

# Number of FFD control points per dimension
nX = 6  # streamwise
nY = 2  # perpendicular to wing planform
nZ = 8  # spanwise

# Compute grid points
span_dist = numpy.linspace(0, 1, nZ) ** 0.8
z_sections = span_dist * (z_tip - z_root) + z_root

x_te = span_dist * (x_tip_range[0] - x_root_range[0]) + x_root_range[0]
x_le = span_dist * (x_tip_range[1] - x_root_range[1]) + x_root_range[1]
y_coords = numpy.vstack(
    (
        span_dist * (y_tip_range[0] - y_root_range[0]) + y_root_range[0],
        span_dist * (y_tip_range[1] - y_root_range[1]) + y_root_range[1],
    )
)

X = numpy.zeros((nY * nZ, nX))
Y = numpy.zeros((nY * nZ, nX))
Z = numpy.zeros((nY * nZ, nX))
row = 0
for k in range(nZ):
    for j in range(nY):
        X[row, :] = numpy.linspace(x_te[k], x_le[k], nX)
        Y[row, :] = numpy.ones(nX) * y_coords[j, k]
        Z[row, :] = numpy.ones(nX) * z_sections[k]
        row += 1

# Write FFD to file
filename = "ffd_front_wing.xyz"
f = open(filename, "w")
f.write("\t\t1\n")
f.write("\t\t%d\t\t%d\t\t%d\n" % (nX, nY, nZ))
for set in [X, Y, Z]:
    for row in set:
        vals = tuple(row)
        f.write("\t%3.8f\t%3.8f\t%3.8f\t%3.8f\t%3.8f\t%3.8f\n" % vals)
f.close()

# rst front_end

# displacement of the back wing relative to the front wing
delta_x = 1.0
delta_y = 0.5

# Bounding box for root airfoil
x_root_range = [-0.02 + delta_x, 0.27 + delta_x]
y_root_range = [-0.05 + delta_y, 0.05 + delta_y]
z_root = -0.01

# Bounding box for tip airfoil
x_tip_range = [-0.02 + delta_x, 0.27 + delta_x]
y_tip_range = [-0.05 + delta_y, 0.05 + delta_y]
z_tip = 0.67

# Number of FFD control points per dimension
nX = 6  # streamwise
nY = 2  # perpendicular to wing planform
nZ = 8  # spanwise

# Compute grid points
span_dist = numpy.linspace(0, 1, nZ) ** 0.8
z_sections = span_dist * (z_tip - z_root) + z_root

x_te = span_dist * (x_tip_range[0] - x_root_range[0]) + x_root_range[0]
x_le = span_dist * (x_tip_range[1] - x_root_range[1]) + x_root_range[1]
y_coords = numpy.vstack(
    (
        span_dist * (y_tip_range[0] - y_root_range[0]) + y_root_range[0],
        span_dist * (y_tip_range[1] - y_root_range[1]) + y_root_range[1],
    )
)

X = numpy.zeros((nY * nZ, nX))
Y = numpy.zeros((nY * nZ, nX))
Z = numpy.zeros((nY * nZ, nX))
row = 0
for k in range(nZ):
    for j in range(nY):
        X[row, :] = numpy.linspace(x_te[k], x_le[k], nX)
        Y[row, :] = numpy.ones(nX) * y_coords[j, k]
        Z[row, :] = numpy.ones(nX) * z_sections[k]
        row += 1

# Write FFD to file
filename = "ffd_back_wing.xyz"
f = open(filename, "w")
f.write("\t\t1\n")
f.write("\t\t%d\t\t%d\t\t%d\n" % (nX, nY, nZ))
for set in [X, Y, Z]:
    for row in set:
        vals = tuple(row)
        f.write("\t%3.8f\t%3.8f\t%3.8f\t%3.8f\t%3.8f\t%3.8f\n" % vals)
f.close()

# rst back_end

# some extra space for the outer parent FFD
extra_space = 0.1

# Bounding box for root
x_root_range = [-0.02 - extra_space, 0.27 + delta_x + extra_space]
y_root_range = [-0.05 - extra_space, 0.05 + delta_y + extra_space]
z_root = -0.01 - extra_space

# Bounding box for tip
x_tip_range = [-0.02 - extra_space, 0.27 + delta_x + extra_space]
y_tip_range = [-0.05 - extra_space, 0.05 + delta_y + extra_space]
z_tip = 0.67 + extra_space

# Number of FFD control points per dimension
nX = 2  # streamwise
nY = 2  # perpendicular to wing planform
nZ = 2  # spanwise

# Compute grid points
span_dist = numpy.linspace(0, 1, nZ) ** 0.8
z_sections = span_dist * (z_tip - z_root) + z_root

x_te = span_dist * (x_tip_range[0] - x_root_range[0]) + x_root_range[0]
x_le = span_dist * (x_tip_range[1] - x_root_range[1]) + x_root_range[1]
y_coords = numpy.vstack(
    (
        span_dist * (y_tip_range[0] - y_root_range[0]) + y_root_range[0],
        span_dist * (y_tip_range[1] - y_root_range[1]) + y_root_range[1],
    )
)

X = numpy.zeros((nY * nZ, nX))
Y = numpy.zeros((nY * nZ, nX))
Z = numpy.zeros((nY * nZ, nX))
row = 0
for k in range(nZ):
    for j in range(nY):
        X[row, :] = numpy.linspace(x_te[k], x_le[k], nX)
        Y[row, :] = numpy.ones(nX) * y_coords[j, k]
        Z[row, :] = numpy.ones(nX) * z_sections[k]
        row += 1

# Write FFD to file
filename = "ffd_parent.xyz"
f = open(filename, "w")
f.write("\t\t1\n")
f.write("\t\t%d\t\t%d\t\t%d\n" % (nX, nY, nZ))
for set in [X, Y, Z]:
    for row in set:
        vals = tuple(row)
        f.write("\t%3.8f\t%3.8f\n" % vals)
f.close()
# rst end
