"""
Acoustical subsystem
--------------------

"""
import numpy as np
from .subsystem import Subsystem

class SubsystemAcoustical(Subsystem):
    """
    Abstract base class for all acoustical subsystems.
    """
    
    @property
    def conductance_point_average(self):
        """Average point conductance of an acoustic component.
        
        .. math:: \\overline{G} = \\frac{1}{\\overline{R}}
        
        """
        return 1.0 / self.resistance_point_average
    
    @property
    def resistance_point_average(self):
        """Average point resistance of an acoustic component.
        
        .. math:: \\overline{R} = \\frac{ \\rho c^2  }{ 4 V \\delta f }
        
        See Lyon, page 149, equation 8.5.3
        
        """
        return self.component.material.density * self.soundspeed_group / (4.0 * self.component.volume * self.average_frequency_spacing)
    
    @property
    def wavenumber(self):
        """Wavenumber."""
        return self.frequency.angular / self.soundspeed_phase
    
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
        return np.sqrt(self.component.material.bulk / self.component.material.density)
        
    @property
    def pressure(self):
        """Mean sound pressure :math:`p`.
        
        
        .. math:: p^2 = \\frac{E \\rho c^2}{V}
        
        Craik, equation 3.12, page 56.
        
        """
        return np.sqrt(self.energy*self.component.material.density*self.soundspeed_group**2.0 / self.component.volume)
        
    @property
    def pressure_level(self):
        """
        Sound pressure level :math:`L_p`.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: L_p = 20 \\log_{10}{\\left( \\frac{p}{p_0} \\right)}
        
        .. seealso:: :attr:`seapy.system.System.reference_pressure`
        
        """
        return 20.0 * np.log10(self.pressure / self.system.reference_pressure)
    
