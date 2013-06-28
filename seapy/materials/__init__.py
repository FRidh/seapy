

from MaterialGas import MaterialGas
from MaterialSolid import MaterialSolid


import inspect, sys
materials_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available materials.
""" 