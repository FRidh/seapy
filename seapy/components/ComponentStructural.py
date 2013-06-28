
import numpy as np
from Component import Component

class ComponentStructural(Component):
    """
    Abstract base class for structural components.
    """
    
    def __init__(self, name, system, **properties):
        Component.__init__(self, name, system, **properties)
        
    availableSubsystems = ['Long', 'Bend', 'Shear']
    
    @property
    def velocity(self):
        """Velocity of the component :math:`v_{component}`. 
        
        :rtype: :class:`numpy.ndarray`
        
        This is the sum of all subsystems velocities.       
        """
        
        velocity = np.zeros(self.frequency.amount)
        for subsystem in self.linked_subsystems:
            velocity = velocity + subsystem.velocity
        return velocity      
    
    @property
    def velocity_level(self):
        """
        Velocity level :math:`L_v`.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        try:
            return 20.0 * np.log10(self.velocity / (5.0 * 10**(-8.0)) ) 
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    