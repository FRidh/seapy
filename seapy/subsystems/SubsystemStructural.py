import abc
import numpy as np

from Subsystem import Subsystem


class SubsystemStructural(Subsystem):
    """
    Abstract base class for all Structural subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    
    
    @property
    def velocity(self):
        """
        Vibrational velocity :math:`v`.
        
        .. math:: v = \\sqrt{\\frac{E}{m}}
        """
        try:
            return np.sqrt(self.energy / self.component.mass)
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
            
    @property
    def velocity_level(self):
        """
        Velocity level.
        
        .. math:: L_v = 20 \\log_{10}{\\frac{v}{v_0}}
        """
        try:
            return 20 * np.log10(self.velocity / (5 * 10**(-8)) ) 
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    
    