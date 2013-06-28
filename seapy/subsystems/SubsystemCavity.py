
import abc
import numpy as np

from Subsystem import Subsystem


class SubsystemCavity(Subsystem): 
    """
    Abstract base class for all Cavity subsystems.
    """
    __metaclass__ = abc.ABCMeta  
    
    
    @property
    def wavenumber(self):
        pass
    
    @property
    def soundspeed_group(self):
        """
        Group speed of a fluid in a duct with rigid walls.
        """
        return self.soundspeed_phase
    
    @property
    def soundspeed_phase(self):
        """
        Phase speed of a fluid in a duct with rigid walls.
        
        .. math:: c_0 = c_g = c_{\\phi} = \\sqrt{\\frac{K_0}{\\rho_0}}
        
        See Lyon, above eq 8.1.9.
        """
        try:
            return np.ones(self.frequency.amount) * np.sqrt(self.component.material.bulk / self.component.material.density)
        except ZeroDivisionError:
            return np.zeros(self.frequency.amount)
        
        
    @property
    def pressure(self):
        """Mean sound pressure :math:`p`
        
        """
        
    
    
    @property
    def pressure_level(self):
        """
        Sound pressure level :math:`L_p`.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: L_p = 20 \\log_{10}{\\frac{p}{p_0}}
        """
        try:
            return 20.0 * np.log10(self.pressure / (2.0 * 10**(-5.0)) ) 
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    