"""
Components
==========

.. toctree::
    :maxdepth: 2


Module with all components that are available.

.. inheritance-diagram:: seapy.components

.. automodule:: seapy.components.component

Structural
**********

.. automodule:: seapy.components.structural
.. automodule:: seapy.components.beam
.. automodule:: seapy.components.pipe
.. automodule:: seapy.components.plate


Acoustical
**********

.. automodule:: seapy.components.acoustical
.. automodule:: seapy.components.acoustical1d
.. automodule:: seapy.components.acoustical2d
.. automodule:: seapy.components.acoustical3d


"""

from .beam import Component1DBeam
from .plate import Component2DPlate
from .pipe import ComponentPipe

from .acoustical2d import Component2DAcoustical
from .acoustical3d import Component3DAcoustical


import inspect, sys

components_map = {
    item[0]: item[1]
    for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)
}
"""
Dictionary with all available components.
"""
