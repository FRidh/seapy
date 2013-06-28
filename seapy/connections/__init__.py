

from Connection import Connection


import inspect, sys
connections_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available connections.
""" 