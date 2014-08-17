"""
Acoustical component
--------------------

This is an abstract base class for acoustical components.

"""

import numpy as np
from .component import Component
from ..base import Attribute

class ComponentAcoustical(Component):
    """Abstract base class for acoustical components.
    """
    
    #@property
    #def subsystem_long(self):
        #"""Subsystem for longitudinal waves.
        #"""
        #for obj in self.linked_subsystems:
            #if isinstance(
    
    
    

    @property
    def pressure(self):
        """Pressure within the component :math:`p_{component}`. 
        
        :rtype: :class:`numpy.ndarray`
        
        This is the sum of all subsystems velocities.       
        """
        return sum(subsystem.pressure for subsystem in self.linked_subsystems)
    
    @property
    def pressure_level(self):
        """
        Sound pressure level :math:`L_p`.
        
        :rtype: :class:`numpy.ndarray`
        
        .. seealso:: :attr:`seapy.subsystems.subsystemacoustical.SubsystemAcoustical`
        
        .. math:: L_p = 20 \\log_{10}{\\left( \\frac{p}{p_0} \\right)}
        
        .. seealso:: :attr:`seapy.system.System.reference_pressure`
        
        """
        return 20.0 * np.log10(self.pressure / self.system.reference_pressure)
