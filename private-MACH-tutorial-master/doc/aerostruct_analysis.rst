.. _aerostruct_analysis:

********************************************
Aerostructural analysis with ADflow and TACS
********************************************

Overview
========
This tutorial introduces the setup for a basic aerostructural analysis.
The aerostructural analysis scripts in MACH use both the aerodynamics and structures modules. 
Therefore, it is assumed that you have completed both the aerodynamics and structures single discipline tutorials prior to completing this multidisciplinary tutorial.
The wing model we are using, and the related ``.cgns`` and ``.bdf`` meshes, refer to the geometry discussed in the :ref:`MACH-Aero tutorial <mach-aero:aero_pygeo>`.
Note that the aerodynamic and structural analyses are stacked on the same processors.
This is our current bast practice as it tends to make it easier to load balance the problem.
Old scripts that use a "split" approach, pre-allocating the processors for aerodynamic and structural optimization separately, are considered outdated.

.. TODO: Add more details about what is going on 
         Add wingbox to MACH_Aero wing, include aeroelastic deflection 

Files
=====
In this section we refer to ``as_run.py`` run file. It uses ``wingbox.bdf`` and ``wing_vol.cgns`` as input meshes, and the following setup files:

- ``setup_adflow``
- ``setup_warp``
- ``setup_tacs`` which is re-used from the structural analysis and optimization sections.

.. _aux_files:

Auxiliary setup files
=====================

Following our coding best practice, we set up the solvers and additional modules in separate ``setup_`` files, stored in the ``SETUP`` folder.
You should be familiar with these scripts from the previous sections of the tutorial, so we briefly discuss their content in the following sections.
Copy the code in the related files in the ``SETUP`` folder.

Setup aerodynamics
------------------
This script is very concise. It receives the grid file as input and returns an instance of the ADflow solver. If you want to change the solver options, edit the dictionary below according to :ref:`ADflow documentation <adflow:adflow_options>`.

.. literalinclude:: ../tutorial/wing/SETUP/setup_adflow.py


Setup mesh warping
------------------
Another concise file receives the grid file as an input and returns an instance of IDWarp to be later associated with the ``CFDSolver``.

.. literalinclude:: ../tutorial/wing/SETUP/setup_warp.py

To add more specific options, check the :ref:`IDWarp documentation <idwarp:idwarp_options>`

Dissecting the aerostructural runscript
=======================================
Open the file ``as_run.py`` with your favorite text editor.
Then copy the code from each of the following sections into this file.

Import libraries and define common variables
--------------------------------------------
The imports for this runscript should be familiar if you have already run aerodynamic and structural analyses.
The `Problem` classes from ``baseclasses`` instantiate objects that collect all the relevant input data for the single solvers, ``ADflow``, ``TACS``, and ``pyAeroStrucuture`` respectively.
This last solver is imported explicitly here together with the load transfer class, while the other codes (and the mesh warping tool ``IDwarp``) are imported separately in from their respective :ref:`aux_files`.

.. literalinclude:: ../tutorial/wing/as_run.py
   :start-after: # rst imports (start)
   :end-before: # rst imports (end)

Note that the structural input file is called directly from ``setup_tacs`` for consistency with the previous tutorial, but it is good practice to store all the input files in a shared dictionary like the one above.
Check ``setup_adflow`` to see how the info is passed to the setup scripts.

.. _as_prob_setup:

Setup aerostructural problem
----------------------------


We set up the aerodynamic and structural problems separately with the usual approach.
The ``AeroStructProblem()`` class takes care of putting the two problems together and feed the info to the ``pyAeroStructure`` instance.

.. literalinclude:: ../tutorial/wing/as_run.py
   :start-after: # rst ASP (start)
   :end-before: # rst ASP (end)

Setup solvers
-------------
Similarly, the solvers are instantiated separately (with their respective ``setup_`` files)

.. literalinclude:: ../tutorial/wing/as_run.py
   :start-after: # rst setup solver (start)
   :end-before: # rst setup solver (end)


.. _setup_ASsolver: 

Setup pyAeroStructure
---------------------
In this section of the code, we set up the load transfer by instantiating a :class:`TACSLDTransfer() <pyaerostructure:pyaerostructure.TACSLDTransfer.TACSLDTransfer>` object with default options and the instance of :class:`AeroStruct() <pyaerostructure:pyaerostructure.pyAeroStruct.AeroStruct>` taking as input the discipline solvers, the transfer object, and a set of options for the coupled aerostructural solver and sensitivities.

.. literalinclude:: ../tutorial/wing/as_run.py
   :start-after: # rst AS object (start)
   :end-before: # rst AS object (end)

Check :ref:`pyAeroStructure options documentation <pyaerostructure:pyaerostructure_options>` to learn more about the options provided via the ``mdOptions`` dictionary.
This example uses mostly default values, except for reducing the number of maximum iterations for the adjoint solver (``nAdjointIter``) and the MDA loop (``nMDIter``).
The solver's tolerance is also relaxed with respect to the default values.

More information about how the coupled aerostructural system is handled and solved can be found on the :ref:`pyAeroStructure documentation page <pyaerostructure:pyaerostructure>`.

Solve the aerostructural system
-------------------------------
The aerostructural solve is triggered when we explicitly call the ``AeroStruct`` instance with ``AS(asp)``.
Note that only now we feed the solver with the problem case information defined at the top (:ref:`as_prob_setup`).
Once the analysis is complete, we evaluate the functionals of interest, defined by the ``evalFuncs`` options in the Aero and Structural problems, calling the ``.evalFunctions(asp,funcs)`` method.
This method takes the aerostructural problem instance and the empty ``funcs`` dictionary as input.

.. literalinclude:: ../tutorial/wing/as_run.py
   :start-after: # rst ASSolve (start)
   :end-before: # rst ASSolve (end)


Compute the aerostructural gradients
------------------------------------
Similarly to what done for the analysis, ``.evalFunctionsSens()`` now triggers the adjoint solver to compute the coupled sensitivities.

.. literalinclude:: ../tutorial/wing/as_run.py
   :start-after: # rst ASSolve (end)
   :end-before: # rst ASAdjoint (end)

Note that we are not defining any aerodynamic (eg. alpha) or shape design variables (we are not even using pyGeo) for this analysis.
The only DVs are the structural parameters defined in the :ref:`setup_tacs file <aerostruct_structure_setup>`, and thus the sensitivities are calculated with respect to those variables.
Although we only use structural variables, we still have to solve a coupled adjoint equation to take care of the `off-diagonal` terms of the system.
Indeed, the effects of any structural change do not only affect the wingbox characteristics such as mass and stiffness, but propagate to the aerodynamic performance of the deflected wing.
To learn more about how we implement the coupled aerostructural analysis and sensitivity, check :ref:`pyAeroStructure documentation <pyaerostructure:pyaerostructure>`.

Run it yourself!
================
First make the output directory and then run the script::

    $ mkdir output
    $ mpirun -np 4 python as_run.py


.. note::
   Always check the rigid links when you run your aerostructural analysis the first time,
   but no need to print out the rigid links for later production runs.
   To check, provide the ``transferfileName`` option to TACS.
   No need to add an extension.
   It will write out a file (.dat) for each processor, and you can open it in Tecplot.
   The file contains local rigid links (links between every aero node and the struct elements on that processor) and final rigid links selected based on minimum distance.
   Links should look reasonable and connect aero nodes and structural elements.
   An example of the rigid links from this tutorial is shown below.

   .. image:: images/transfer_links.png
      :scale: 30