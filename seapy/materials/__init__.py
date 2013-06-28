"""
Materials
=========

Materials.

.. automodule:: seapy.materials.material
.. automodule:: seapy.materails.materialgas
.. automodule:: seapy.materials.materialsolid


"""

from .materialgas import MaterialGas
from .materialsolid import MaterialSolid


import inspect, sys
materials_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available materials.
""" 
