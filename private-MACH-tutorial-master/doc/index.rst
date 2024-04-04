.. _intro:

#############
MACH Tutorial
#############

Introduction
============

This is the private tutorials page that contains MACH Aerostructural tutorials and advanced MACH-Aero tutorials.
The publicly available tutorials are located in the :doc:`MACH-Aero repo <mach-aero:index>`.
If you are new to MACH, start with the publicly available tutorials.

The files for these additional tutorials are located on `GitHub <https://github.com/mdolab/private-MACH-tutorial/>`_.
The scripts referenced in the tutorial can be found in the tutorial directory.
The files for the overset meshing tutorial are in the ``overset`` directory.
The run files for structural and aerostructural optimization, including the geometry and aerodynamic loads generation, are located in the ``wing`` directory.
We store the input meshes and files in the ``INPUT`` folder, and the shared modules setup files in ``SETUP`` folder within ``wing``.
All the scripts from this section live in the same folder to minimize code duplication, but they are all independent from each other and only need the appropriate setup and input files to run, as illustrated in the following pages.
Although these scripts should be executable without any modifications, **we highly recommend that you create a separate directory and type out the lines of code by yourself.**
As you do this, ask yourself, "Do I understand why the code is written this way?"
This will result in a much deeper understanding of how to use the tools and eventually will help you develop code in a consistent manner.
It is up to the user to define their own directory tree, but we strongly recommend to keep the setup and input files in separate folders for a cleaner layout.


Before continuing with the tutorial, make sure that the MDO Lab framework is already installed on your machine, following the instructions for :ref:`mach-aero:installfromscratch`.

.. TODO: We should have a set of simple but functional cases in the tutorial, and then have a separate FAQ section where we describe more advanced capabilities in detail.

Table of Contents
=================

.. toctree::
   :maxdepth: 2
   :titlesonly:

   struct_overview
   aerostruct_analysis
   opt_overview
   overset_overview
   opt_check_list

Required Software
=================
**Made in the MDOlab**

* `ADflow <https://github.com/mdolab/adflow>`_
* `pyGeo <https://github.com/mdolab/pygeo>`_
* `pySpline <https://github.com/mdolab/pyspline>`_
* `pyHyp <https://github.com/mdolab/pyhyp>`_
* `IDWarp <https://github.com/mdolab/idwarp>`_
* `pyLayout <https://github.com/mdolab/pylayout>`_
* `TACS <https://github.com/mdolab/tacs_orig>`_
* `pyTACS <https://github.com/mdolab/pytacs>`_
* `pyOptSparse <https://github.com/mdolab/pyoptsparse>`_
* `cgnsUtilities <https://github.com/mdolab/cgnsutilities>`_
* `baseclasses <https://github.com/mdolab/baseclasses>`_
* `pyAeroStructure <https://github.com/mdolab/pyaerostructure>`_
* `multipoint <https://github.com/mdolab/multipoint>`_

Note: These links take you to the GitHub repositories.
The documentation site for each package is listed in the README of each GitHub repository.

**External Software**

* ICEM CFD
* Tecplot (for visualization)

Documentation strategy
======================
The tutorial resides on `GitHub <https://github.com/mdolab/private-MACH-tutorial/>`_, but it is a living tutorial, which means that it is constantly updated with corrections and improvements.
We invite you, especially as a new user, to take notes of the parts that you find confusing and bring them to the attention of an admin to the tutorial repository so that changes can be made.

The rst files in the doc directory contain direct links to the python scripts in the tutorial directory to avoid code duplication.
This is done using the ``start-after`` and ``end-before`` options of Sphinx's native ``literalinclude`` directive.
We adopt the convention of using ``# rst <section subject>`` as the marker for the start and end of each ``literalinclude`` section, like so:
::

    # rst Simple addition (begin)
    a = 2
    b = 3
    c = a + b
    # rst Simple addition (end)

Please adopt this same convention for any future developments to the tutorial.
