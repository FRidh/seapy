"""
Structural subsystem
--------------------

"""
import numpy as np
from .subsystem import Subsystem


class SubsystemStructural(Subsystem):
    """
    Abstract base class for all structural subsystems.
    """

    @property
    def conductance_point_average(self):
        """
        Average point conductance of a structural component.
        
        .. math:: \\overline{G} = \\frac{1}{4} M \overline{\\delta f}
        
        See Lyon, page 149, equation 8.5.2 as well as page 200.
        
        """
        return 0.25 * self.component.mass * self.average_frequency_spacing

    @property
    def resistance_point_average(self):
        """
        Average point resistance.
        """
        return 1.0 / self.conductance_point_average

    @property
    def velocity(self):
        """
        Vibrational velocity :math:`v`.
        
        .. math:: v = \\sqrt{\\frac{E}{m}}
        
        Craik, equation 3.11, page 55.
        
        """
        return np.sqrt(self.energy / self.component.mass)

    @property
    def velocity_level(self):
        """
        Velocity level :math:`L_v`.
        
        :rtype: :class:`numpy.ndarray`
        
        The structural velocity level is calculated as
        
        .. math:: L_v = 20 \\log_{10}{\\left( \\frac{v}{v_0} \\right) }
        
        .. seealso:: :attr:`seapy.system.System.reference_velocity`
        
        """
        return 20.0 * np.log10(self.velocity / self.system.reference_velocity)
