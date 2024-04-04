# MACH Tutorial
[![Documentation Status](https://readthedocs.com/projects/mdolab-mach-tutorial/badge/?version=latest&token=44ed1e89df388729ba6a2241ccadfd494a9863eed89094a8370aa7b63dacf6ae)](https://mdolab-mach-tutorial.readthedocs-hosted.com/en/latest/?badge=latest)
[![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.private-MACH-tutorial?repoName=mdolab%2Fprivate-MACH-tutorial&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=39&repoName=mdolab%2Fprivate-MACH-tutorial&branchName=master)

This repository contains a step-by-step tutorial for some of the tools in the MACH framework.
The MACH (MDO of Aircraft Configurations with High-fidelity) framework is developed by the [MDO Lab](http://mdolab.engin.umich.edu).
It facilitates the design, analysis, and optimization of large, multi-disciplinary systems.
The tutorial covers the basics needed to optimize the aerodynamic surface and internal wingbox structure of a basic wing.
It also includes an airfoil optimization example.

## Tutorial documentation
You can either view the [online tutorial](https://mdolab-mach-tutorial.readthedocs-hosted.com) or build the tutorial documentation locally.
To generate the tutorial locally, open a terminal and enter the following commands:

    $ cd private-MACH-tutorial/doc
    $ make html

This generates html files in `_build/html/`. You can then open `_build/html/index.html` in your preferred browser to view the tutorial documentation.

## MACH Modules
This is a list of MACH modules that are outside of MACH-Aero:

| Code repository | Functionality | Documentation | CI Status |
| --------------- | ------------- | ------------- | --------- |
| [`tacs_orig`](https://github.com/mdolab/tacs_orig) | FEA solver | [![Documentation Status](https://readthedocs.com/projects/mdolab-tacs-orig/badge/?version=latest&token=b6b545fc34c508b4255d5cfeeeb5da09a08a4d3be5b71662d9fc709a44c6ecfa)](https://mdolab-tacs-orig.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.tacs_orig?repoName=mdolab%2Ftacs_orig&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=22&repoName=mdolab%2Ftacs_orig&branchName=master) |
| [`pytacs`](https://github.com/mdolab/pytacs) | Python wrapper for TACS | [![Documentation Status](https://readthedocs.com/projects/mdolab-pytacs/badge/?version=latest&token=e9368e10f52c289f0e0a3731310a7f86fe5a7fa692a14a3b8afd697405a1a1f7)](https://mdolab-pytacs.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.pytacs?branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=26&branchName=master) |
| [`pyAeroStructure`](https://github.com/mdolab/pyaerostructure) | Aerostructural MDA and CAD solver | [![Documentation Status](https://readthedocs.com/projects/mdolab-pyaerostructure/badge/?version=latest&token=aac0835e22bd7505d243e8147c7b7cc4d8096db8ca0ed61076f43107e5f53b1a)](https://mdolab-pyaerostructure.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.pyaerostructure?branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=18&branchName=master) |
| [`pyFriction`](https://github.com/mdolab/pyfriction) | Viscous drag correction for Euler CFD | [![Documentation Status](https://readthedocs.com/projects/mdolab-pyfriction/badge/?version=latest&token=89be28d8073c5dbd7d0237d922f42d13cf5407ce0625500514de7e08ef807a5b)](https://mdolab-pyfriction.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.pyfriction?repoName=mdolab%2Fpyfriction&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=8&repoName=mdolab%2Fpyfriction&branchName=master) |
| [`pyLayout`](https://github.com/mdolab/pylayout) | Utilities for structural meshing | [![Documentation Status](https://readthedocs.com/projects/mdolab-pylayout/badge/?version=latest&token=9264a90968d07105f16da312b30a69b35fead9b1e70c604b619959316eb9421b)](https://mdolab-pylayout.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.pylayout?repoName=mdolab%2Fpylayout&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=25&repoName=mdolab%2Fpylayout&branchName=master) |
| [`pySurf`](https://github.com/mdolab/pysurf) | Handling geometric intersections for overset | [![Documentation Status](https://readthedocs.com/projects/mdolab-pysurf/badge/?version=latest&token=067843d7a8abdc6f145c3207abe46d4d73bf44ad406656e48b06a15a4cfa37a7)](https://mdolab-pysurf.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.pysurf?repoName=mdolab%2Fpysurf&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=36&repoName=mdolab%2Fpysurf&branchName=master) |
| [`pyFoil`](https://github.com/mdolab/pyfoil) | Utilities for working with airfoils | [![Documentation Status](https://readthedocs.com/projects/mdolab-pyfoil/badge/?version=latest&token=cecc9dced1e15350c0f4fe338b0a533062c234a72ec8a4d433122229362c7525)](https://mdolab-pyfoil.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.pyfoil?repoName=mdolab%2Fpyfoil&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=28&repoName=mdolab%2Fpyfoil&branchName=master)  |
| [`performanceCalcs`](https://github.com/mdolab/performancecalcs) | Aircraft performance calculations | [![Documentation Status](https://readthedocs.com/projects/mdolab-performancecalcs/badge/?version=latest&token=fff3b2c4a6111440c3f3d2bf9922fcc1041ec968c7e7e0f68fc1379549f30560)](https://mdolab-performancecalcs.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.performancecalcs?repoName=mdolab%2Fperformancecalcs&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=12&repoName=mdolab%2Fperformancecalcs&branchName=master) |
| [`weightAndBalance`](https://github.com/mdolab/weightandbalance) | Aircraft weight and balance calculations | [![Documentation Status](https://readthedocs.com/projects/mdolab-weightandbalance/badge/?version=latest&token=b833e975586a615040ecf57a4c94c9f75ed1b58e946e56858ff36343f2f031bc)](https://mdolab-weightandbalance.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.weightandbalance?branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=15&branchName=master) |
| [`wimpressCalc`](https://github.com/mdolab/wimpresscalc) | Aircraft planform calculations | [![Documentation Status](https://readthedocs.com/projects/mdolab-wimpresscalc/badge/?version=latest&token=453ab545adf92392dc81a2139e92e01b6557b5aef5965d5a55c4f87f08421d70)](https://mdolab-wimpresscalc.readthedocs-hosted.com/en/latest/?badge=latest) | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.wimpresscalc?branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=14&branchName=master) |
| [`geograd`](https://github.com/mdolab/geograd) | Spatial integration constraint |  | [![Build Status](https://dev.azure.com/mdolab/Private/_apis/build/status/mdolab.geograd?repoName=mdolab%2Fgeograd&branchName=master)](https://dev.azure.com/mdolab/Private/_build/latest?definitionId=21&repoName=mdolab%2Fgeograd&branchName=master) |