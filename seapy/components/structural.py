"""
Structural component
--------------------

This is an abstract base class for structural components.

"""

import numpy as np
from .component import Component

class ComponentStructural(Component):
    """Abstract base class for structural components.
    """
    
    availableSubsystems = ['Long', 'Bend', 'Shear']
    
    
    @property
    def velocity(self):
        """Velocity of the component :math:`v_{component}`. 
        
        :rtype: :class:`numpy.ndarray`
        
        This is the sum of all subsystems velocities.       
        """
        return sum(subsystem.velocity for subsystem in self.linked_subsystems)
    
    @property
    def velocity_level(self):
        """
        Velocity level :math:`L_v`.
        
        :rtype: :class:`numpy.ndarray`
        
        The structural velocity level is calculated as
        
        .. math:: L_v = 20 \\log_{10}{\\left( \\frac{v}{v_0} \\right) }
        
        .. seealso:: :attr:`seapy.system.System.reference_velocity`
        
        """
        return 20.0 * np.log10(self.velocity / self.system.reference_velocity ) 

