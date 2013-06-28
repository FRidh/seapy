
from ExcitationRain import ExcitationRain
from ExcitationPoint import ExcitationPoint


import inspect, sys
excitations_map = {item[0]: item[1] for item in inspect.getmembers(sys.modules[__name__], inspect.isclass)}
"""
Dictionary with all available excitations.
""" 