# rst begin
import argparse
from cgnsutilities import cgnsutilities

parser = argparse.ArgumentParser()
parser.add_argument("inFile", type=str)
parser.add_argument("outFile", type=str)
args = parser.parse_args()

# Generate background mesh
wingGrid = cgnsutilities.readGrid(args.inFile)

dh = 0.04
hExtra = 20 * 0.64
nExtra = 25
sym = "z"
mgcycle = 3
backgroundFile = "background_tandem.cgns"

wingGrid.simpleOCart(dh, hExtra, nExtra, sym, mgcycle, backgroundFile)
backgroundGrid = cgnsutilities.readGrid(backgroundFile)

# Combine background grid with wing meshes
oversetGrid = cgnsutilities.combineGrids([backgroundGrid, wingGrid], useOldNames=False)
oversetGrid.writeToCGNS(args.outFile)

# rst end
