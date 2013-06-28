"""
Couplings
=========

.. toctree::
    :maxdepth: 2

Module with all available couplings.

As a general note:

* Points have dimension 0
* Lines have dimension 1
* Surfaces have dimension 2

.. automodule:: seapy.couplings.coupling
.. automodule:: seapy.couplings.couplingpointstructural

.. automodule:: seapy.couplings.couplingsurfaceacoustical

Subsystems are connected to eachother through couplings.
"""

from .couplingpointstructural import CouplingPointStructural
from .couplinglinestructural import CouplingLineStructural

from .couplingsurfaceacoustical import CouplingSurfaceAcoustical

from .couplingsurfaceplateacoustical import CouplingSurfacePlateAcoustical
from .couplingsurfaceacousticalplate import CouplingSurfaceAcousticalPlate


import inspect, sys
couplings_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available couplings.
""" 
