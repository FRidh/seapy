import numpy as np
from Coupling import Coupling
    
class Coupling2DCavities3D(Coupling):
    """
    Coupling for cavity3D to cavity transmission.
    """

    @property
    def impedance_from(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """
        return self.subsystem_from.impedance

    @property
    def impedance_to(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """     
        return self.subsystem_to.impedance
    
    @property
    def tau(self):
        """
        Transmission coefficient.
        """
        return 0.1
    
    
    @property
    def clf(self):
        """
        Coupling loss factor for transmission from a 3D cavity to a 3D cavity.
        
        .. math:: \\eta_{12} = \\frac{c S}{8 \\pi f V} \\tau_{12}
        
        See BAC, equation 3.14
        
        """
        return self.subsystem_from.soundspeed_group * self.area / (8.0 * np.pi * self.frequency.center * self.subsystem_from.volume) * self.tau