"""
Point excitation
================

"""

import numpy as np
from .excitation import Excitation
#from ..subsystems import SubsystemCavity, SubsystemStructural

class ExcitationPoint(Excitation):
    """
    Point excitation
    """

    radius = None
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

    _force = None
    _velocity = None

    @property
    def force(self):
        """Sound force :math:`p`.
        """
        if self._force:
            return self._force
        elif self._velocity:
            return self.resistance * self.velocity 
        else:
            raise ValueError("Neither force nor velocity is specified.")
        
    @force.setter
    def force(self, x):
        self._force = x
        self._velocity = None
    
    @property
    def velocity(self):
        """Structural velocity :math:`u`.
        """
        if self._velocity:
            return self._velocity
        elif self._force:
            return self.force / self.resistance
        else:
            raise ValueError("Neither force nor velocity is specified.")
            
    @velocity.setter
    def velocity(self, x):
        self._velocity = x
        self._force = None
        
    @property
    def power(self):
        """Input power :math:`P`.
        
        The input power is given  by
        
        .. math:: P = F^2 \\Re{Y}
        
        with:
        
        * rms force :math:`F`
        * mobility :math:`Y`.
        
        """
        return self.force**2.0 * self.mobility.real
    
    @property
    def impedance(self):
        return self.subsystem.impedance_point_force
    
    
    
class ExcitationPointMoment(ExcitationPoint):
    """
    Point excitation of a moment.
    """
    
    _moment = None
    _velocity = None

    @property
    def moment(self):
        """Sound moment :math:`p`.
        """
        if self._moment:
            return self._moment
        elif self._velocity:
            return self.resistance * self.velocity 
        else:
            raise ValueError("Neither moment nor angular velocity is specified.")
        
    @moment.setter
    def moment(self, x):
        self._moment = x
        self._velocity = None
    
    @property
    def velocity(self):
        """Angular velocity :math:`\\omega`.
        """
        if self._velocity:
            return self._velocity
        elif self._velocity:
            return self.moment / self.resistance
        else:
            raise ValueError("Neither moment nor angular velocity is specified.")
        
    @velocity.setter
    def velocity(self, x):
        self._velocity = x
        self._moment = None
        
    @property
    def power(self):
        """Input power :math:`P`.
        
        The input power is given  by
        
        .. math:: P = M^2 \\Re{Y}
        
        with:
        
        * rms moment :math:`M`
        * mobility :math:`Y`.
    
        """
        return self.moment**2.0 * self.mobility.real
    
    @property
    def impedance(self):
        return self.subsystem.impedance_point_moment
    
  
class ExcitationPointVolume(ExcitationPoint):
    """
    Point excitation by a volume flow.
    """
    
    _pressure = None
    _velocity = None

    @property
    def pressure(self):
        """Sound pressure :math:`p`.
        """
        if self._pressure:
            return self._pressure
        elif self._velocity:
            return self.resistance * self.velocity 
        else:
            raise ValueError("Neither pressure nor angular velocity is specified.")
        
    @pressure.setter
    def pressure(self, x):
        self._pressure = x
        self._velocity = None
    
    @property
    def velocity(self):
        """Volume velocity :math:`U`.
        """
        if self._velocity:
            return self._velocity
        elif self._pressure:
            return self.pressure / self.resistance
        else:
            raise ValueError("Neither pressure nor angular velocity is specified.")
            
    @velocity.setter
    def velocity(self, x):
        self._velocity = x
        self._pressure = None
        
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
        return self.velocity**2.0 * self.impedance.real
    
    @property
    def impedance(self):
        try:
            return self.subsystem.impedance_point_volume(self)
        except TypeError:
            return self.subsystem.impedance_point_volume
            
    
