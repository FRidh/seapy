"""
Point excitation
================

"""

from ..base import Attribute
import numpy as np
from .excitation import Excitation

# from ..subsystems import SubsystemCavity, SubsystemStructural


class ExcitationPoint(Excitation):
    """
    Point excitation
    """

    radius = Attribute()
    """
    Radius :math`r` of the source.
    """

    @property
    def mobility(self):
        """The driving-point mobility or admittance :math:`Y`.
        
        .. math:: Y = \\frac{1}{Z}
        
        """
        return 1.0 / self.impedance

    @property
    def resistance(self):
        return self.impedance.real


class ExcitationPointForce(ExcitationPoint):
    """
    Point excitation by a force.
    """

    force = Attribute()
    """Force :math:`F`.
    """
    velocity = Attribute()
    """Velocity :math:`v`.
    """

    @property
    def power(self):
        """Input power :math:`P`.
        
        The input power is given  by
        
        .. math:: P = F^2 \\Re{Y}
        
        with:
        
        * rms force :math:`F`
        * mobility :math:`Y`.
        
        """
        if self.force.any():
            return self.force ** 2.0 * self.mobility.real
        elif self.velocity.any():
            return self.velocity ** 2.0 * self.impedance.real
        else:
            raise ValueError("Neither force nor velocity is specified.")

    @property
    def impedance(self):
        return self.subsystem.impedance_point_force


class ExcitationPointMoment(ExcitationPoint):
    """
    Point excitation of a moment.
    """

    moment = Attribute()
    """Moment :math:`M`.
    """

    velocity = Attribute()
    """Angular velocity :math:`\\omega`.
    """

    @property
    def power(self):
        """Input power :math:`P`.
        
        The input power is given  by
        
        .. math:: P = M^2 \\Re{Y}
        
        with:
        
        * rms moment :math:`M`
        * mobility :math:`Y`.
    
        """
        if self.moment.any():
            return self.moment ** 2.0 * self.mobility.real
        elif self.velocity.any():
            return self.velocity ** 2.0 * self.impedance.real
        else:
            raise ValueError("Neither moment nor velocity is specified.")

    @property
    def impedance(self):
        return self.subsystem.impedance_point_moment


class ExcitationPointVolume(ExcitationPoint):
    """
    Point excitation by a volume flow.
    """

    pressure = Attribute()
    """Sound pressure :math:`p`.
    """

    velocity = Attribute()
    """Volume velocity :math:`U`.
    """

    @property
    def power(self):
        """Input power :math:`P`.
        
        The input power is given  by
        
        .. math:: P = p^2_{rms} G = p^2_{rms} \\mathrm{Re{(Y)}
        
        with:
        
        * rms pressure :math:`p`
        * conductance :math:`G`
        * mobility :math:`Y`
        
        """
        if self.pressure.any():
            return self.pressure ** 2.0 * self.mobility.real
        elif self.velocity.any():
            return self.velocity ** 2.0 * self.impedance.real
        else:
            raise ValueError("Neither pressure nor velocity is specified.")

    @property
    def impedance(self):
        # try:
        return self.subsystem.impedance_point_volume(self)

    # except TypeError:
    # return self.subsystem.impedance_point_volume()
