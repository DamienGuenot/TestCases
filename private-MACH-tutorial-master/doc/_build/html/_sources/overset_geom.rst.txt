.. _overset_geom:

************************************
Geometry and Surface Mesh Generation
************************************

Introduction
============
First, we will generate a simple rectangular wing geometry, and then we will generate a surface mesh using the same process covered in the public :doc:`MACH-Aero Tutorials <mach-aero:index>`, but with a different planform and airfoil.

.. note::
   At this point we expect that you have completed the :ref:`Aerodynamic Analysis <mach-aero:aero_overview>` and :ref:`Aerodynamic Optimization <mach-aero:opt_overview>` tutorials form the public docs.

Files for geometry generation
=============================
Navigate to the directory ``oversetopt/geometry/`` in your tutorial directory, and copy the following file from the MACHtutorial repository::

    $ cp ../../../tutorial/oversetopt/geometry/NACA642A015.dat .

Create an empty file called ``generate_wing.py`` in the current directory.

The pyGeo runscript
===================
Open ``generate_wing.py`` in your favorite text editor, and copy the following into this file.

.. literalinclude:: ../tutorial/oversetopt/geometry/generate_wing.py
   :start-after: # rst start
   :end-before: # rst end

This will generate a small (0.24 m x 0.64 m) rectangular wing with a NACA 642-A015 airfoil.

Run it yourself!
================
Now you can now run the python script with the command::

    $ python generate_wing.py

This should create ``wing.tin`` and ``wing.dat``.
You can open ``wing.dat`` in Tecplot to view the wing surface:

.. image:: images/overset_geom.png
   :scale: 40

Surface mesh
============
Next, navigate to your ``oversetopt/mesh/surface`` directory and create a surface mesh for this geometry using the same process covered in the :ref:`Surface Meshing <mach-aero:aero_icem>` tutorial.
Or if you want to skip this step, you can use the ``wing.cgns`` surface mesh provided in ``MACHtutorial/tutorial/oversetopt/mesh/surface``.

You can open ``wing.cgns`` in Tecplot to view the surface mesh.
There is certainly some room for improvement in the example mesh shown below.

.. image:: images/overset_surface_mesh.png
   :scale: 40
