.. _opt_aerostruct:

***************************
Aerostructural Optimization
***************************

Introduction
============

In this section we will walk through the aerostructural optimization runscript.
This builds on the aerostructural analysis and structural optimization cases covered in the previous sections of this tutorial.
Some of the auxiliary setup files will be reused to avoid duplicates in the main script.

As a reference example we use a two-point wing aerostructural drag and mass minimization problem with respect to wing twist and structural element thicknesses, while subject to geometrical, lift, and structural failure constraints.
Shape variables can also be included in the problem on user demand.
The objective function is defined :ref:`here <def_objcon>` as the sum of the drag and twice the wing structural mass.
Note that the drag is not scaled here, and its order of magnitude might differ from the mass one.
This potentially reduces the optimization effectiveness and efficiency.
Production runscripts should have a better problem formulation then the one presented here as an example.
As defined later in the :ref:`des_points` code section, we define a single cruise point and a single maneuver design point, which contribute to the objective function and non-linear constraints respectively.
For the case without shape variables, the optimization problem is as follows:

| *minimize*
|    composite objective :math:`D + 2M`
| *with respect to*
|    2 angles of attack
|    7 section twists
|    108 panel thicknesses
| *subject to*
|    cruise lift constraint :math:`L_\text{cruise} - W_\text{ref} = 0`
|    maneuver lift constraint :math:`L_\text{man} - 2.5 W_\text{ref} = 0`
|    stress constraints :math:`\mathrm{KS}_i \le 1.0, i=0,1,2`

The corresponding problem sparsity is::

                                      twist (7)   struct (108)   alpha_cruise (1)   alpha_maneuver (1)  
                                    +------------------------------------------------------------------+
         struct_linear_con(L) (170) |           |       X      |                  |                    |
                                    --------------------------------------------------------------------
       struct_linear_con_0(L) (170) |           |       X      |                  |                    |
                                    --------------------------------------------------------------------
                cruise_lift_con (1) |     X     |       X      |         X        |                    |
                                    --------------------------------------------------------------------
              maneuver_lift_con (1) |     X     |       X      |                  |          X         |
                                    --------------------------------------------------------------------
        maneuver_USkinKSFailure (1) |     X     |       X      |                  |          X         |
                                    --------------------------------------------------------------------
        maneuver_LSkinKSFailure (1) |     X     |       X      |                  |          X         |
                                    --------------------------------------------------------------------
   maneuver_Spars_RibsKSFailure (1) |     X     |       X      |                  |          X         |
                                    +------------------------------------------------------------------+


For the case with shape, there are the following additions:

| *with respect to*
|    96 local shape variables
| *subject to*
|    1 volume constraint
|    100 thickness constraints
|    :math:`4\times2\times2=16` LETE constraints

And the sparsity is::

                                          twist (7)   local (96)   struct (108)   alpha_cruise (1)   alpha_maneuver (1)  
                                        +-------------------------------------------------------------------------------+
             struct_linear_con(L) (170) |           |            |       X      |                  |                    |
                                        ---------------------------------------------------------------------------------
         DVCon1_volume_constraint_0 (1) |     X     |      X     |              |                  |                    |
                                        ---------------------------------------------------------------------------------
   DVCon1_thickness_constraints_0 (100) |     X     |      X     |              |                  |                    |
                                        ---------------------------------------------------------------------------------
  DVCon1_lete_constraint_0_local(L) (8) |           |      X     |              |                  |                    |
                                        ---------------------------------------------------------------------------------
  DVCon1_lete_constraint_1_local(L) (8) |           |      X     |              |                  |                    |
                                        ---------------------------------------------------------------------------------
           struct_linear_con_0(L) (170) |           |            |       X      |                  |                    |
                                        ---------------------------------------------------------------------------------
                    cruise_lift_con (1) |     X     |      X     |       X      |         X        |                    |
                                        ---------------------------------------------------------------------------------
                  maneuver_lift_con (1) |     X     |      X     |       X      |                  |          X         |
                                        ---------------------------------------------------------------------------------
            maneuver_USkinKSFailure (1) |     X     |      X     |       X      |                  |          X         |
                                        ---------------------------------------------------------------------------------
            maneuver_LSkinKSFailure (1) |     X     |      X     |       X      |                  |          X         |
                                        ---------------------------------------------------------------------------------
       maneuver_Spars_RibsKSFailure (1) |     X     |      X     |       X      |                  |          X         |
                                        +-------------------------------------------------------------------------------+



Structural Pre-optimization
---------------------------

.. TODO: (future PR - advanced features) At some point add full multi-structural optimization to the python script. Perhaps its best to keep that separate.

Before performing an aerostructural optimization, its often beneficial to perform a structural pre-optimization.
Two types are often performed, a single structural optimization or a sequence of structural optimizations.
In the former, a single structural optimization is performed with constant maneuver  loads.
In the latter, several structural optimizations are run in a sequence where at the start of each structural optimization the maneuver loads are updated.
This strategy requires only a handful of updates in order to converge, i.e., the last structural optimization returns immediately as the current design is already optimal.
While in general it is not necessary to run a structural pre-optimization it may benefit the subsequent full aerostructural optimization in several ways:

#. The starting point, in terms of mass and stiffness, is closer to the aerostructural optimum.
#. The structural constraints are more easily satisfied during the aerostructural optimization.
#. Accelerate the optimization and reduce the possibility of optimizer exiting prematurely.

The multi structural pre-optimizatation strategy is not demonstrated here.
Rather, in the following example we assume you already completed the :ref:`opt_struct` section, so you can use the history file from that optimization case to "warm start" the following aerostructural optimization.
This optimization history can be thought of as the first iteration in the sequence of optimization described above.
While it may not yield feasible initial structural constraints it still offers a good preconditioning of the structure for the aerostructural optimization.

Files
=====
The reference file for this section is ``as_opt.py``, which uses both the ``.cgns`` and ``.bdf`` input files and the following setup scripts:

- ``setup_dvgeo.py``
- ``setup_dvcon.py``
- ``setup_warp.py``
- ``setup_adflow.py``
- ``setup_tacs.py``

Auxiliary setup files
=====================

Here we report the auxiliary files to set up the geometry, the structural solver, and the constraints respectively.
These files are stored in the ``SETUP`` folder you can create in your main script directory.

Setup geometry
--------------

Copy the following lines in ``setup_dvgeo.py``:

.. literalinclude:: ../tutorial/wing/SETUP/setup_dvgeo.py

This function instantiates the ``pyGeo`` object, defines the twist variable and, if required by the user, adds the local shape variables to the problem

Setup constraints
-----------------

Copy the following lines in ``setup_dvcon.py``:

.. literalinclude:: ../tutorial/wing/SETUP/setup_dvcon.py

This script defines the wing geometrical constraints, similarly to what is discussed in the geometric parametrization section of the :ref:`MACH-Aero tutorial <mach-aero:opt_aero>`.
There are no specific additions related to the aerostructural case.

Setup mesh warping
------------------

Copy the following lines in ``setup_warp.py``:

.. literalinclude:: ../tutorial/wing/SETUP/setup_warp.py

This is the same script we used for :ref:`aerostructural analysis <aux_files>`.

Setup aerodynamics
------------------

Copy the following lines in ``setup_adflow.py``:

.. literalinclude:: ../tutorial/wing/SETUP/setup_adflow.py

This is the same script we used for :ref:`aerostructural analysis <aux_files>`.

Setup structure
---------------

You can copy-paste the script illustrated in :ref:`struct_analysis`, reported below for your convenience:

.. literalinclude:: ../tutorial/wing/SETUP/setup_tacs.py




Dissecting the aerostructural optimization script
=================================================

We now go over the main runscript.

Inputs and aircraft data
------------------------

We import most of the MACH core classes at the top of the script, together with the auxiliary setup files discussed above.
Note that we store the input file names in a separate ``files`` dictionary that is passed to the setup files.

.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst init (begin)
    :end-before: # rst init (end)

For this example we use a few input arguments:

    - ``output``: the name of the folder where solver outputs are stored
    - ``shape``: by default, shape variables are not added to the optimization problem. You need to specifically use this argument when running the script in order to run the `full` example
    - ``npcruise`` and ``npmaneuver``: define the number of procs allocated to the cruise and maneuver aerostruct problems respectively. Remember that you need to call ``mpirun`` with the exact number of allocated procs, in this case ``-np 4``

Setting up MPI communicators
----------------------------
To enable multiple flight conditions or other processes to be run in parallel (were each is by itself a parallel process) we rely on the ``multipoint`` package.
More specifically, we use the :class:`multipoint.multiPointSparse <multipoint.multiPointSparse>` module.
For more detailed information on any of the calls described here please see the :ref:`multipoint <multipoint:multipoint>` documentation.

Once the multipoint object has been created two processor sets are created with :meth:`MP.addProcessorSet() <multipoint:multipoint.multiPointSparse.addProcessorSet>` for each flight condition, cruise and maneuver, with each set receiving ``npcruise`` and ``npmaneuver`` processors, respectively.
Note that the ``nMembers`` argument is set to 1 since we only have one cruise and one maneuver flight conditions.
For example, running 5 cruise and 3 maneuver flight conditions ``nMembers`` are 5 and 3 for the cruise and maneuver calls, respectively.

The :meth:`MP.createCommunicators() <multipoint:multipoint.multiPointSparse.createCommunicators>` creates communicators based on the processor sets defined previously.
This ``comm`` object is shared within each processor set, in this case all the cruise processors share one instance and all the maneuver objects share another.
Since we want separate solver instances for each analysis point, we use this ``comm`` object when instantiating these solvers.
On the other hand, ``MP.gcomm`` refers to the "global" ``comm`` object, which is shared for `all` processors.
More specifically, ``MP.gcomm`` is the communicator that was used to instantiate the MP object, which in this case is ``MPI.COMM_WORLD``.
This is used for tasks that are not dependent on each analysis point, e.g. creating the output directory (which is done only on the root processor, hence the ``if MP.gcomm.rank == 0`` line).

The ``setComm`` communicator is not needed here and is in general rarely used as communication within a set is rarely needed.
The ``setFlags`` and ``ptID`` variables are important and can be used to perform operations on a specific group withing a set.
However, since we have only one group within a processor set this will not be explicitly demonstrated here.
Finally, ``groupFlags`` is rarely needed and is not demonstrated here.

Storing the ``setName`` of a given processor is useful and can in many cases simplify the run script.
The :meth:`MP.getSetName() <multipoint:multipoint.multiPointSparse.getSetName>` conveniently returns the ``setName`` for a given processor.
Similarly, :meth:`MP.createDirectories() <multipoint:multipoint.multiPointSparse.createDirectories>` conveniently creates output directories on disk for each processor group in all processor sets.
Since we only have two flight conditions in this example two output directories, ``cruise_0`` and ``maneuver_0`` are created for the ``cruise`` and ``maneuver`` conditions, respectively.
In conjunction with the ``setName`` and ``ptID`` we can access the ``ptDirs`` dictionary that contains the output directory for each of the processor groups.


.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst init (end)
    :end-before: # rst alloc (end)


During the analysis or an optimization a large amount of output is printed to the screen.
To save and organize the output based on the flight condition of interest ``redirectIO`` can be used to redirect the ``stdout`` stream directly to files.
Before doing so, first the necessary folder is created, followed by file handles for each ``ptID``.

.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst alloc (end)
    :end-before: # rst io (end)


.. _des_points:

Defining the cruise and maneuver design points
-----------------------------------------------

For this example we define a two-point problem, with one cruise and one maneuver design point.
As mentioned above, the cruise design point is used to provide the mass and drag of the wing for the objective function of the problem.
The maneuver case conversely is used to estimate the stress constraints using the KS function with a 2.5g load factor.
Both design points must satisfy a lift (equality) constraint.
The two :class:`Aerostruct() <pyaerostruct:pyaerostruct.pyaerostruct.Aerostruct()>` instances are appended to two separate cases that are later passed to separate methods for function and sensitivity evaluations.

.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst io (end)
    :end-before: # rst cases setup (end)

The code closely resembles what was discussed in :ref:`aerostruct_analysis`.
Note that we include the angle of attack ``alpha`` as a design variable (``ap.addDV("alpha",[...])``) for both design points, to facilitate the satisfaction of the lift constraints.

Setting up the solvers and geometry objects
-------------------------------------------

In this section of the code we put together several snippets and components we have already discussed.
Similarly to what is done in :ref:`MACH-Aero optimization tutorial <mach-aero:opt_aero>`, we setup the ``pyGeo`` and ``IDWarp`` objects and associate them to the ``ADflow`` solver.
The ``pyGeo`` object is also associated with the structural solver (``FEASolver.setDVGeo(DVGeo)``), to ensure that geometry changes are reflected on the structural mesh.
The aerostructural solver setup is identical to what was shown in the previous :ref:`setup_ASsolver` section.
We use the block Gauss-Seidel method (``MDSolver: "GS"``) to iterate the MDA to convergence.
Note that at the end of this snippet, the geometric constraints are added to the problem using the separate setup file mentioned in the previous section.

.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst cases setup (end)
    :end-before: # rst setups (end)

.. _def_objcon:

Defining the functions of interests and their sensitivities
-----------------------------------------------------------
We define the function evaluation and sensitivities here, for each processor set.
These functions are almost identical between cruise and maneuver, except for looping over different aerostructural problems.
We also evaluate geometric constraints (and their sensitivities) on the cruise processor set only, since the geometry is shared and the jig shape is the same between the two.
Lastly, we define the ``objCon`` function for combining functionals into objective and constraint values.

.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst setups (end)
    :end-before: # rst funcs (end)

Note that for this specific problem, the reference weight for lift constraints ``Wref`` is the aircraft MTOW, which does not change during the optimization. 

Setting up and running the optimization
---------------------------------------
Setting up the optimization problem follows a similar strategy as is discussed in the :ref:`MACH-Aero tutorial <mach-aero:opt_aero>`.
Here we only discuss the differences.

In addition to the geometric design variables and constraints, we also define structural design variables and constraints that must be added to the optimization problem ``optProb``.
As before, this is achieved with the ``addVariablesPyOpt`` function.

Lift equality constraints are also defined here for both cruise and maneuver cases.
These constraints are added directly to the optimization problem using the ``optProb.addcon`` function.
For both, the idea here is that lift should equal the weight.
Note that derivatives are computed with respect to all design variables relevant to its respective flight condition.
For example, the ``cruise_lift_con`` derivative is computed with respect to the structure, angle of attack, and geometric design variables, but not the maneuver angle of attack.
Three KS constraints corresponding to the maneuver flight condition are then added.
Note that the constraint name has to be composed of the structural problem name and the function names listed in the ``evalFuncs`` list of that structural problem.

Finally, we add the objective name and a scaling value.
The scaling value is chosen to be of similar order of magnitude as the drag.
Once the function handles have been provided to the multipoint object the optimizer setup is done in a similar way as before.
To make sure the optimization problem, i.e., design variables and constraints, is correctly set up the user should study the stdout from the ``print(optProb)`` and the ``printSparsity()``.


.. literalinclude:: ../tutorial/wing/as_opt.py
    :start-after: # rst funcs (end)
    :end-before: # rst end

