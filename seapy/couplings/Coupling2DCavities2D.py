import numpy as np
from Coupling import Coupling
    
class Coupling2DCavities2D(Coupling):
    """
    Coupling for cavity2D to cavity transmission.
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
        return np.zeros(self.frequency.amount)
    
    
    @property
    def clf(self):
        """
        Coupling loss factor for transmission from a 2D cavity to a cavity.
        
        .. math:: \\eta_{12} = \\frac{ \\tau_{12}}{4 \\pi}
        
        See BAC, equation 3.14
        
        """
        return self.tau / (4.0 * np.pi)