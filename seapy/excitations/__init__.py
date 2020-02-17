"""
Excitations
===========

.. inheritance-diagram:: seapy.excitations.excitation

.. automodule:: seapy.excitations.excitation

.. automodule:: seapy.excitations.excitationpoint

"""

# from .excitationrain import ExcitationRain
from .excitationpoint import (
    ExcitationPointForce,
    ExcitationPointMoment,
    ExcitationPointVolume,
)


import inspect, sys

excitations_map = {
    item[0]: item[1]
    for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)
}
"""
Dictionary with all available excitations.
"""
