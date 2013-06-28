"""
Classes describing a one-dimensional cavity.
"""

import numpy as np
from ComponentCavity import ComponentCavity
from ..subsystems import SubsystemCavity

class SubsystemCavity1D(SubsystemCavity):
    """
    Subsystem for a 1D cavity (duct).
    """
    
    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for bending waves. Valid for :math:`f < c_0 / 2 L_c` where :math:`L_c` is the largest cross sectional dimension.
        
        .. math:: \\overline{\\delta f}_0^{1D} = \\frac{c_0}{2L}
        
        See Lyon, eq. 8.1.9
        """
        return self.soundspeed_group / (2.0 * self.component.length)
    
   
    @property
    def impedance(self):
        """
        Impedance for longitudinal waves in a 1D duct.
        
        .. math:: Z_0^{U,1D} = \\frac{2 \\rho c_0}{S}
        
        See Lyon, table 10.1, third row.
        """
        return 2.0 * self.component.material.density * self.soundspeed / self.component.cross_section
       
       
class ComponentCavity1D(ComponentCavity):
    """
    Component for a fluid in a 1D cavity.
    """

    def __init__(self):
        """Constructor."""
        ComponentCavity.__init__(self)
        
        self.subsystem_long = SubsystemLong()
        """
        An instance of :class:`SubsystemLong` describing longitudinal waves.
        """
    