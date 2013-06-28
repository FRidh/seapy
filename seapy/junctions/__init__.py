"""
Junctions
=========

.. inheritance-diagram:: seapy.junctions

.. automodule:: seapy.junctions.junction
    :members:

"""

from .junction import Junction


import inspect, sys
junctions_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available connections.
""" 
