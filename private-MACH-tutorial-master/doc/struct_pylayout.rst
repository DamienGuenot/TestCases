.. _struct_geo:

****************************
Wingbox Geometry and Meshing
****************************

.. TODO: this should probably be moved to pyLayout docs - looking for input!

Introduction
============
The purpose of pyLayout is to generate a surface representation of a conventional wingbox geometry that conforms to the shape and size of the desired wing.
This surface representation can then be meshed in pyLayout or in ICEM, depending on preference and the complexity of the wingbox structure.

Files
=====
In this section we refer to the ``generate_wingbox.py`` file, which uses ``wing.igs`` geometry file from ``INPUT`` folder.

Dissecting the pyLayout script
==============================
To begin, we need to import a few modules.

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst begin import
    :end-before: # rst end import

And define the wingbox characteristics.

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst end import
    :end-before: # rst start refinement

The bulk of the script is devoted to creating data to initialize the creation of the wingbox geometry.
It will make more sense if we start at the end of the script to see what we need to provide.

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst end setup
    :end-before: # rst begin writefiles

The first parameter required to initialize pyLayout is a pyGeo object.
The pyGeo object provides a surface representation of the wing outer mold line (OML) which will be used to ensure that the wingbox fits the wing.

Wingbox Layout
--------------
The rest of the information provided to pyLayout determine the placement of the ribs, spars, and stringers within the wing OML.
Conveniently, the conventional wingbox is basically arranged like a grid, with ribs intersecting spars and stringers at basically perpendicular junctions.
These intersections between ribs, spars, and stringers are provided to pyLayout in the ``X`` parameter, which is a 3D array of shape ncols x nrows x 3.
The columns (of ncols) are aligned with the ribs, whereas the rows (of nrows) are aligned with the spars and stringers.
The upper and lower skins conform to the wing OML and cover the extent of the rib/spar structure.

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst end blanking
    :end-before: # rst end setup


With no further information given, pyLayout would create a grid structure with ribs at every column and spars along every row.
We can blank out certain rows and columns to remove ribs, spars, and stringers using the blanking arrays.
These arrays contain a 1 if the structure should be created a certain location in the grid or a 0 if not.
For example, the ``ribBlank`` array:

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst start ribBlank
    :end-before: # rst end ribBlank

This array contains a 1 for every cell of the grid except those in the first column, which tells pyLayout not to place a rib at the wing root.
The other blanking arrays stipulate spars only on the first and last row, and stringers on every other row.

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst end ribBlank
    :end-before: # rst end blanking

Mesh Refinement
---------------
The number of elements created from this surface representation is determined by the ``ribSpace``, ``spanSpace``, ``vSpace``, ``stringerSpace``, and ``ribStiffenerSpace`` parameters.
These parameters dictate how many elements should be created from each cell of the ``X`` matrix along each of the topological axes.
The stringer height parameters can be used to control the maximum and minimum heights of the stringers.

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst start refinement
    :end-before: # rst end refinement

File output
-----------
pyLayout can output BDF files and Tecplot files for easy visualization

.. literalinclude:: ../tutorial/wing/generate_wingbox.py
    :start-after: # rst begin writefiles
    :end-before: # rst end file

Run it yourself!
================
::

    $ python generate_wingbox.py
