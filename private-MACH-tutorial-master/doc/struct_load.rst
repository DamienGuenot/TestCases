.. _struct_load:

*****************
Aerodynamic Loads
*****************

Introduction
============
Many times we want to apply aerodynamic loads to the structure without going through the trouble of setting up the aerostructural solver.
This can be done by exporting the loads from a CFD solution and applying these static loads in TACS.
In this section, we will show how to obtain a CFD solution for a specific load case and then export the aerodynamic loads to be used in the next section.

Files
=====
In this section we refer to the ``cl_solve.py``, which uses the ``.cgns`` mesh file from ``INPUT``

How to do a :math:`C_L` solve
=============================
.. literalinclude:: ../tutorial/wing/cl_solve.py

The function to do a :math:`C_L` solve is :meth:`CFDSolver.solveCL() <adflow:adflow.pyADflow.ADFLOW.solveCL>`.
All you need to do is provide the desired :math:`C_L` value and ADflow will do a secant search to find the corresponding angle of attack.
Once this is done, the aerodynamic forces can be exported using :meth:`CFDSolver.writeForceFile <adflow:adflow.pyADflow.ADFLOW.writeForceFile>`.

Run it yourself!
================
::

    $ mpirun -np 4 python cl_solve.py
