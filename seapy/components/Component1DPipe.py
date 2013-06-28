
import numpy as np
from ComponentStructural import ComponentStructural
from ..subsystems import SubsystemStructural



class SubsystemLong(SubsystemStructural):
    pass


class SubsystemBend(SubsystemStructural):
    pass

class SubsystemShear(SubsystemStructural):
    pass



















    
class ComponentPipe(ComponentStructural):
    """
    One-dimensional beam component.
    """
    pass
    
    
    def __init__(self):
        """Constructor."""
        ComponentStructural.__init__(self)
        
        self.subsystem_long = SubsystemLong()
        """
        An instance of :class:`SubsystemLong` describing longitudinal waves.
        """
        self.subsystem_bend = SubsystemBend()
       """
        An instance of :class:`SubsystemBend` describing bending waves.
        """
        self.subsystem_shear = SubsystemShear()
        """
        An instance of :class:`SubsystemShear` describing shear waves.
        """
    
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the beam by :math:`\\sqrt{2}`.
        See Lyon, above eq. 8.1.10
        .. math:: \\kappa = \\frac{h}{\\sqrt{2}}
        """
        return self.height / 12