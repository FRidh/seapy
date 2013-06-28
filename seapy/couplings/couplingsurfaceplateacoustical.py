import numpy as np
from .coupling import Coupling


def radiation_efficiency(coupling, component):
    """
    Radiation efficiency of a plate to a cavity and vice versa.

    Where:
        
    * area of plate :math:`S = L_x L_y`
    * circumference of plate :math:`U = 2 (L_x + L_y)`
    
    * :math:`\\alpha  = \\sqrt{\\frac{f}{f_c}}`
    
    When :math:`f < 0.5 f_c`:
    
    .. math:: g_1 = \\frac{4}{\\pi^4} (1 - 2 \\alpha^2) (1 - \\alpha^2)^(-0.5) 
    
    When :math:`f > 0.5 f_c`:
    
    .. math:: g_1 = 0
    
    
    .. math::

    See TA2 Radiation plateapp_ta2
    """      
    
    #component = self.subsystem_from.component
    
    
    f = np.array(component.frequency.center, dtype=complex)
    """Cast to complex numbers to prevent errors with sqrt further down."""
    
    fc = coupling.critical_frequency
    lc = coupling.critical_wavelength
        
    Lx = component.length
    Ly = component.width
    S = component.area
    U = 2.0 * (Lx + Ly)
    
    fc_band = (fc > coupling.frequency.lower) * (fc < coupling.frequency.upper)
    f_lower = fc > coupling.frequency.upper
    f_upper = fc < coupling.frequency.lower
    
    alpha = np.sqrt(f/fc)
    g1 =  ( 4.0 / np.pi**4.0 * (1.0 - 2.0 * alpha**2.0) / np.sqrt(1.0 - alpha**2.0) ) * (f < 0.5 * fc)
    g2 = 1.0 / (4.0 * np.pi**4.0) * (  (1.0 - alpha**2) * np.log((1.0+alpha)/(1.0-alpha)) + 2.0 * alpha ) / (1.0-alpha**2.0)**1.5
    
    sigma1 = lc**2.0 / S * (2.0 * g1 + U / lc * g2)
    sigma2 = np.sqrt(Lx/lc) + np.sqrt(Ly/lc)
    sigma3 = (1.0 - fc/f)**(-0.5)
    
    sigma1 = np.nan_to_num(sigma1)
    sigma2 = np.nan_to_num(sigma2)
    sigma3 = np.nan_to_num(sigma3)
    """Replace NaN with zeros"""
    
    sigma = sigma1 * f_lower + sigma2 * fc_band  + sigma3 * f_upper * (sigma3 < sigma2)
    sigma = np.real(np.nan_to_num(sigma))
    return sigma

    
def critical_frequency(subsystem_plate, subsystem_cavity):
    """
    Critical frequency.
    
    .. math:: f_c = \\frac{ c_0^2 \\sqrt{3}  } {\\ pi c_L h}
    
    .. math:: f_c = \\frac{f c_0^2}{c_B^2}
    
    See Craik, table 3.3, page 51.
    """
    return subsystem_plate.frequency.center * (subsystem_cavity.soundspeed_group / subsystem_plate.component.subsystem_bend.soundspeed_phase)**2.0
    #return subsystem_cavity.soundspeed_group**2.0 / (1.81818181 * subsystem_plate.component.subsystem_long.soundspeed_group * subsystem_plate.component.height)
    
class CouplingSurfacePlateAcoustical(Coupling):
    """
    A model describing the coupling between a plate and a cavity.
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
        Critical frequency.
        
        .. math:: f_c = \\frac{ c_0^2  } {1.8 c_L t}
        
        See BAC, 3.2.2 script.
        """
        return critical_frequency(self.subsystem_from, self.subsystem_to)
        
    @property
    def critical_wavelength(self):
        """
        Wavelength belonging to critical frequency.
        
        .. math:: \\lambda_c = c_{g} / f_c
        
        """
        try:
            return self.subsystem_to.soundspeed_group / self.critical_frequency
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
            
    @property
    def radiation_efficiency(self):
        """
        Radiation efficiency of a plate for bending waves.
        """
        return radiation_efficiency(self, self.subsystem_from.component)
        
    @property
    def clf(self):
        """
        Coupling loss factor for plate to cavity radiation.
        
        .. math:: \\eta_{plate, cavity} = \\frac{\\rho_0 c_0 \\sigma}{\\omega m^{''}}
        
        .. attention::
            Which speed of sound???
        
        See BAC, equation 3.6
        """
        try:
            return self.subsystem_from.component.material.density * self.subsystem_to.soundspeed_group * \
                   self.radiation_efficiency / (self.frequency.angular * self.subsystem_from.component.mass_per_area)
        except (ZeroDivisionError, FloatingPointError):
            return np.zeros(self.frequency.amount)
