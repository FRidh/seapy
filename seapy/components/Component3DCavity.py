"""
Classes describing a three-dimensional cavity.
"""

import numpy as np
from ComponentCavity import ComponentCavity
from ..subsystems import SubsystemCavity


class SubsystemLong(SubsystemCavity):
    """
    Subsystem for a fluid in a 3D cavity.
    """

    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for a fluid in a 3D cavity.
        
        .. math:: \\overline{\\delta f}_0^{3D} = \\frac{c_0^^3}{4 \\pi V f^2}
        
        See Lyon, eq 8.3.7
        """
        try:
            return self.soundspeed_phase**2.0 / (4.0 * np.pi * self.component.volume * self.frequency.center**2.0)
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    @property
    def impedance(self):
        """
        Impedance of a 3D cavity.
        
        .. math:: Z_0^{U,3D} = \\frac{\\pi \\rho f^2}{c_0} \\left( 1 + \\frac{j}{k_0 r}   \\right)
        
        See Lyon, table 10.1, last row.
        """
        #try:
            #return np.pi * self.component.material.density * self.frequency.center**2.0 / self.soundspeed_phase * (1.0 + 1.0j / (self.wavenumber * self.excitation.radius)) 
        #except FloatingPointError:
        return np.zeros(self.frequency.amount)

        
class Component3DCavity(ComponentCavity):
    """
    Component for a fluid in a 3D cavity.
    """

    
    subsystem_long = None
    """
    An instance of :class:`SubsystemLong` describing longitudinal waves.
    """