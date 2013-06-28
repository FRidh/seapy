"""
Structural point coupling
-------------------------

"""


import numpy as np
from .coupling import Coupling


class CouplingPointStructural(Coupling):
    """
    Model of a point coupling between structural components.
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
        Frequency averaged transmission coefficient
        
        .. math:: \\overline{\\tau_{12}} = \\frac{8 \\pi \\langle \\overline{G_1} \\rangle f \\eta_1 M_1}{1 + \\frac{\\eta_1}{\\eta_2}} \\frac{\\eta_2 + \\eta_{21}}{\\eta_12}
        
        .. math:: \\tau_{12} = \\frac{4 R_1 R_2}{\\left| \\sum_{i=1}^m Z_i \\right|^2}
        
        See :cite:`1998:lyon`.
        """
        return 4.0 * self.resistance_from * self.resistance_to / self.junction.impedance**2.0
         
    
    @property
    def clf(self):
        """Coupling loss factor."""
        #return self.tau() * self.subsystem_from.c_group() / (self.subsystem_from.omega * self.subsystem_from.component.length() * (2-self.tau()) )
        return np.real(subsystem_to.mobility()) / (2.0 * np.pi * self.frequency.angular * subsystem_from.component.mass + np.abs(self.subsystem_from.mobility() + self.subsystem_to.mobility() )**2.0 )
