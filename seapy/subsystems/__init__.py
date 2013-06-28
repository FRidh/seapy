

from SubsystemCavity import SubsystemCavity
from SubsystemStructural import SubsystemStructural


import inspect, sys
subsystems_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available subsystems.
""" 