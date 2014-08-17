import numpy as np
from .coupling import Coupling
    
class CouplingLineStructural(Coupling):
    """Line coupling betweeen two structural subsystems.
    """
    

    @property
    def impedance_from(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """
        if type(self.subsystem_from.impedance) == type(None):
            return self.subsystem_from.impedance
        else:
            return np.zeros(len(self.frequency))
            
    @property
    def impedance_to(self):
        """
        Choses the right impedance of subsystem_from.
        Applies boundary conditions correction as well.
        """     
        if type(self.subsystem_from.impedance) == type(None):
            return self.subsystem_to.impedance
        else:
            return np.zeros(len(self.frequency))
            
    @property
    def clf(self):
        return np.ones(len(self.frequency)) * 0.5
