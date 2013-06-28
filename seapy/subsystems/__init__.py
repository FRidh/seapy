"""
Subsystems
==========

This module contains abstract base classes for subsystems.

.. automodule:: seapy.subsystems.subsystem
.. automodule:: seapy.subsystems.subsystemacoustical
.. automodule:: seapy.subsystems.subsystemstructural


"""
from .subsystemacoustical import SubsystemAcoustical
from .subsystemstructural import SubsystemStructural


import inspect, sys
subsystems_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available subsystems.
""" 
