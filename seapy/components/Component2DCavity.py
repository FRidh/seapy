"""
Classes describing a two-dimensional cavity.
"""

import numpy as np
from ComponentCavity import ComponentCavity
from ..subsystems import SubsystemCavity

class SubsystemLong(SubsystemCavity):
    """
    Subsystem for a fluid in a 2D cavity.
    """

    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for a fluid in a thin, flate space.
        Valid for :math:`f < c_0 / 2h` where `h` is the thickness of the layer.
        
        .. math:: \\overline{\\delta f}_0^{2D} = \\frac{c_0^2}{\\omega  A}
        
        See Lyon, eq 8.2.12
        """
        return self.soundspeed / (self.frequency.angular * self.A)
    
    
    
class Component2DCavity(ComponentCavity):
    """
    Component for a fluid in a 2D cavity.
    """

    def __init__(self):
        """Constructor."""
        ComponentCavity.__init__(self)
        
        self.subsystem_long = SubsystemLong()
        """
        An instance of :class:`SubsystemLong` describing longitudinal waves.
        """
    