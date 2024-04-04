from idwarp import USMesh


def setup(comm, files):
    meshOptions = {
        "gridFile": files["gridFile"],
    }
    # Set up mesh warping
    mesh = USMesh(options=meshOptions, comm=comm)
    return mesh
