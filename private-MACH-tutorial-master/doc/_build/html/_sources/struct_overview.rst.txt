.. _struct_overview:

###################
Structural Analysis
###################

Overview
========
TACS is the Toolkit for Analysis of Composite Structures written in C++.
This tutorial will help you use pyTACS, the Python interface for TACS.

-   Solution types: linear static, nonlinear static, buckling
-   Elements: beams, shells, volumes

TACS supports structural model data in the Nastran Bulk Data File (BDF) format.
A typical BDF file contains grid points, elements, element properties, boundary conditions, and load conditions.
The MeshLoader class in TACS will read in data for grid points, elements, and boundary conditions, but the element properties and load conditions must be formulated in the Python runscript.

Elements are the most basic functional group in TACS.
Each element is linked to its neighbors via the connectivity matrix.
Each element belongs to a component as well.
Components are made up of groups of elements that have the same property ID (PID) in the BDF file.

.. TODO: Add more details about the elements and the physical components of the wingbox - e.g. skins, stiffeners, stringers

Table of Contents
=================

.. toctree::
   :maxdepth: 1

   struct_pylayout
   struct_load
   struct_analysis

Output file
-----------
To visualize the solution, the ``.f5`` file must be converted to a ``.plt`` (Tecplot file). Use the ``f5totec`` command in the terminal.

What outputs are in the file?

.. TODO: these explanations should be moved to pyTacs, here we should just include the link

* **u0, v0, w0, rotx, roty, roty**
    6 DOF displacements at each node

* **ex0, ey0, exy0, exz0, eyz0**
    Mid-plane shell strains

.. TODO: add more details

* **ex1, ey1, exy1**
    Shell curvature/through thickness strain gradient

.. TODO: add more details

* **sx0, sy0, sxy0, sxz0, sxy0**
    Mid-plane stress resultants, (force/length)

.. TODO: what is the difference?


* **sx1, sy1, sxy1**
    Moment resultants, (moment/length)

These outputs are a little confusing but they relate to the constitutive models we use for modelling shells in TACS.
These models rely on Mindlin-Reissner plate theory, also known as First-order Shear Deformation Theory (hence the FSDT in the `isoFSDT` and `bladeFSDT` constitutive model names).
This theory is essentially the plate equivalent of Euler-Bernoulli beam theory and assumes that the in plane strains vary linearly through the thickness of the shell.
The in-plane strains at a given height z from the shell mid-plane is then:

.. math::

   \begin{bmatrix} \epsilon_x(z) \\ \epsilon_y(z) \\ \gamma_{xy}(z) \end{bmatrix} = \begin{bmatrix} \epsilon_x^0 \\ \epsilon_y^0 \\ \gamma_{xy}^0 \end{bmatrix} + z \begin{bmatrix} \epsilon_x^1 \\ \epsilon_y^1 \\ \gamma_{xy}^1 \end{bmatrix}


* **lambda, buckling**
    Failure and buckling constraints (value > 1 means the constraint is violated)

TACS uses different failure criteria for different materials.
For isotropic materials it uses the Von-Mises stress criterion and for composites it can either use a maximum strain or Tsai-Wu criterion.
At any given point in the structure, TACS computes these criteria at the upper and lower surfaces of the shell and, if using the `bladeFSDT` constitutive model, the tip of the blade stiffener.
The maximum of these values is then returned as the failure value for that point.