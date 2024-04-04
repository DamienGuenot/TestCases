.. _overset_ihcc:

*************************
Checking the Overset Mesh
*************************

Introduction
============
Getting different meshes that are overset to work well together can be tricky.
Here we will show how ADflow can be used to check if there will be any problems with the hole-cutting algorithm and connectivities, and also to visualize which cells are compute cells, interpolate cells, blanked cells, and flooded cells.

Files
=====
Navigate to the directory ``oversetopt/ihc_check`` in your tutorial folder.
Copy the following files from the volume meshing directory:
::

    $ cp ../mesh/volume/overset_combined.cgns .

Create the following empty runscript in the current directory:

- ``ihc_check.py``


Dissecting the ADflow runscript
===============================
Open the file ``ihc_check.py`` with your favorite text editor.
Then copy the following into this file.


.. literalinclude:: ../tutorial/oversetopt/ihc_check/ihc_check.py
   :start-after: # rst start
   :end-before: # rst end

This will not actually run a flow simulation, it will just carry out the setup.
Adding ``'blank'`` to the ``volumevariables`` and ``surfacevariables`` (which tells ADflow which variables to save in the results) will allow us to see which cells are compute, interpolate, blanked, and flooded cells.

There are some new parameters here related to overset meshes that we have not seen before.

  - The ``usezippermesh`` option is ``True`` by default so we set it to ``False`` here to skip the zipper mesh generation, because it may crash if the hole cutting does not work. A zipper mesh provides a watertight surface for force integration in the region where cells overlap.

  - The ``nrefine`` option is set to 10 (this is the default). This option specifies the number of times the implicit hole cutting algorithm is run.

  - The ``nearwalldist`` option is set to 0.1 (this is the default). This option controls how compute cells are preserved near walls. Changing this value may prevent flooding. We usually use 0.01 m for a full-scale aircraft mesh.

  - The ``oversetpriority`` option can be used to specify a dictionary in which the key is the family name of a mesh and the corresponding value is a factor to multiply the volumes of that mesh's cells by for the hole-cutting algorithm. The hole-cutting algorithm prioritizes keeping smaller cells, so this can be used to prioritize keeping the cells of a certain volume mesh. We don't specify anything for the ``oversetpriority`` but just include it here to show some of the options available.

There are other overset options that have not been discussed here.
Those can be found in the `pyADflow run script <https://github.com/mdolab/adflow/blob/master/python/pyADflow.py>`_. 

Run it yourself!
================
Run the script::

    $ python ihc_check.py

If all goes well, the output will show that there are 0 ``orphans`` and there will not be any error messages related to connectivities.

Visualizing the iblank values in tecplot
========================================

Now we can check what roles the different cells in the overlapping regions have been given.
Follow the following instructions in Tecplot.

  - Load ``overset_combined_IHC.cgns`` but check ``Advanced options`` before clicking ``Open``
  - Select ``One Tecplot zone per non-poly CGNS zone/solution`` and click ``OK``
  - Check ``Mesh`` under ``Show zone layers`` (select ``yes`` if it asks you if you want to turn on surfaces)
  - Zoom in to the symmetry plane
  - Check ``Contour`` under ``Show zone layers``
  - Click on ``Details...`` next to ``Contour``
  - Select ``iblank`` in the drop-down menu at the top left
  - Click on ``Set levels...`` and set the minimum level to -3 and the maximum level to 0
  - Set the number of levels to 4, then click ``OK`` and ``Close``
  - Click on ``Zone Style...``, go to the ``Contour`` tab, then highlight all the zones (ctrl+A) and change the ``Contour Type`` to ``Primary value flood`` (right click on the contour type of one of the zones)
  - Under the ``Show Contour`` column, uncheck all the ``wing_vols_combine`` zones and then click ``Close``
  - Finally, uncheck ``Shade`` under ``Show zone layers`` if it was selected by default

You should see something like the following image.

.. image:: images/overset_iblank_background.png
  :scale: 50

Now turn off the contours for all the ``background`` zones and switch on the contours for all the ``wing_vols_combine`` zones.

.. image:: images/overset_iblank_wings.png
  :scale: 50

.. note:: In Tecplot, ``Plot`` -> ``Blanking`` -> ``Value Blanking`` is a useful tool to hide or show cells with certain values (e.g., if you want to see only the interpolation cells and hide everything else).
