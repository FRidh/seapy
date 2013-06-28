import numpy as np
from Coupling import Coupling

import Coupling3DPlateCavity

class Coupling3DCavityPlate(Coupling):
    """
    A model describing the coupling between a cavity and a plate.
    """
    
    @property
    def impedance_from(self):
        return self.subsystem_from.impedance
    
    @property
    def impedance_to(self):
        return self.subsystem_to.impedance
    
    @property
    def critical_frequency(self):
        """
        Critical frequency
        """
        return Coupling3DPlateCavity.critical_frequency(self.subsystem_to, self.subsystem_from)
    
    @property
    def critical_wavelength(self):
        """
        Wavelength belonging to critical frequency.
        
        .. math:: \\lambda_c = c_{g} / f_c
        
        """
        try:
            return self.subsystem_from.soundspeed_group / self.critical_frequency
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
        
    @property
    def radiation_efficiency(self):
        """
        Radiation efficiency.
        """
        return Coupling3DPlateCavity.radiation_efficiency(self, self.subsystem_to.component)
    
    @property
    def clf(self):
        """
        Coupling loss factor for transmission from a cavity to a plate.
        
        .. math:: \\eta_{cavity,plate} = \\frac{\\rho_0 c^2 S \\sigma f_c }{8 \\pi f^3 m^{''} V_2}
        
        See BAC, equation 3.9
        """        
        try:
            return self.subsystem_from.component.material.density * \
                   self.subsystem_from.soundspeed_group**2.0 *self.area * self.radiation_efficiency * \
                   self.critical_frequency / (8.0 * np.pi * self.frequency.center**3.0 * \
                   self.subsystem_to.component.mass_per_area * self.subsystem_from.component.volume) 
        except (ZeroDivisionError, FloatingPointError):
            return np.zeros(self.frequency.amount)

        
        