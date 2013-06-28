"""
Module with all components that are available.
"""

from Component1DBeam import Component1DBeam
from Component2DPlate import Component2DPlate

from Component2DCavity import Component2DCavity
from Component3DCavity import Component3DCavity


import inspect, sys
components_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available components.
""" 