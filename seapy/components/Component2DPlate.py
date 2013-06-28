"""
Classes describing a two-dimensional plate.
"""

import numpy as np
from ComponentStructural import ComponentStructural
from ..subsystems import SubsystemStructural


class SubsystemLong(SubsystemStructural):
    """
    Subsystem for longitudinal waves in a 2D isotropic component.
    """
    
    @property
    def soundspeed_group(self):
        """Group velocity for longitudinal waves in a 2D isotopic plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: c_L^{'} = \\sqrt{\\frac{E}{\\rho \\left( 1 - \\mu^2 \\right)}}
        
        See Lyon, above eq 8.2.5 
        """
        try:
            return np.ones(self.frequency.amount) * np.sqrt(self.component.material.young / (self.component.material.density * (1.0 - self.component.material.poisson**2.0)))
        except ZeroDivisionError:
            return np.zeros(self.frequency.amount)
            
    @property
    def soundspeed_phase(self):
        """Phase velocity for longitudinal waves in a 2D isotropic plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: c_{group} = c_{phase} = c_L
        
        See Lyon, above eq 8.2.8
        """
        return self.soundspeed_group
    
    @property
    def average_frequency_spacing(self):
        """Average frequency spacing for a 2D isotropic plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: \\overline{\delta f}_S^{2D} = \\frac{{c_L^1}^2}{\\omega A}
        
        See Lyon, equation 8.2.8
        """
        try:
            return  self.soundspeed_group**2.0 / (self.frequency.angular * self.component.area)
        except FloatingPointError:
            return np.zeros(self.frequency.amount)

    @property
    def wavenumber(self, m, n, delta1, delta2):
        """Wavenumber for longitudinal waves in a plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: k_L = \\sqrt{\\left[ \\left( m - \\delta_1 \\right) \\frac{\\pi}{L_1} \\right] + \\left[ \\left( n - \\delta_2 \\right) \\frac{\\pi}{L_2} \\right]}
       
        See Lyon, equation 8.2.1.
        """
        return np.sqrt( ( ( m - delta1) * np.pi / self.component.length) + ( ( m - delta2) * np.pi / self.component.width) )
    
    
    @property
    def impedance(self):
        """Impedance
        
        :rtype: :class:`numpy.ndarray`
        
        """
        return np.zeros(self.frequency.amount)    
        
    #@property
    #def wavenumber(self):
        #"""
        #Wavenumber of longitudinal waves in a plate.
        
        #.. math:: k_L = \\frac{ \\rho \\omega \\left( 1 - \\nu \\right) }{E h}
        
        #Langley and Heron, 1990, eq 24.
        #"""
        #return self.component.material.density * self.omega * (1.0 - self.component.material.poisson) / (self.component.material.young * self.component.thickness)
    
        
class SubsystemBend(SubsystemStructural):
    """
    Subsystem for bending waves in a 2D isotropic component.
    """

    @property
    def soundspeed_phase(self):
        """Phase velocity for bending wave.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: c_{B,\\phi}^{2D} = \\sqrt{\\omega \\kappa c_L^{'}}
        
        See Lyon, above eq. 8.2.5
        """
        return np.sqrt(self.frequency.angular * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_phase)
                
    @property
    def soundspeed_group(self):
        """Group velocity for bending wave.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: c_{B, g}^{2D} = 2 c_{B,\\phi}^{2D}
        
        See Lyon, above eq. 8.2.5
        """
        return 2.0 * self.soundspeed_phase
    
    @property
    def average_frequency_spacing(self):
        """Average frequency spacing for bending waves in a 2D isotropic plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: \\overline{\\delta f}_B^{2D} = \\frac{2 \\kappa c_L^{', 2D}}{A}
        
        See Lyon, eq 8.2.5
        """
        return 2.0 * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_group / self.component.area
    
    @property
    def wavenumber(self):
        """Wavenumber of flexural waves in a plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: k_B = \\sqrt[4]{ \\frac{ \\rho \\omega }{D}} 
        
        
        See Langley and Heron, 1990, eq 18.
        """
        return np.power(self.component.material.density * self.frequency.angular / self.flexural_rigidity, 0.25)
    
    @property
    def flexural_rigidity(self):
        """Flexural rigidity of a plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: D = \\frac{t^3}{12 \\left( 1 - \\nu^2 \\right)}
        
        
        """
        return self.thickness**3.0 / (12.0 * (1.0 - self.poisson()**2.0))
    
    @property
    def impedance(self):
        """Impedance
        
        :rtype: :class:`numpy.ndarray`
        
        """
        return np.zeros(self.frequency.amount)    
        
    
class SubsystemShear(SubsystemStructural):
    """
    Subsystem for shear waves in a 2D isotopic component.
    """
    
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for shear waves in a 2D isotropic plate.
        
        .. math:: c_S = \\sqrt{\\frac{G}{\\rho}}
        
        See Lyon, above eq. 8.2.5
        """
        try:
            return np.ones(self.frequency.amount) * np.sqrt(self.component.material.shear / self.component.material.density)
        except ZeroDivisionError:
            return np.zeros(self.frequency.amount)
        
    @property
    def soundspeed_group(self):
        """
        Group velocity for shear wavees in a 2D isotropic plate.
        
        .. math:: c_{group} = c_{phase} = 2 C_S
        
        See Lyon, above eq. 8.2.5
        """
        return self.soundspeed_phase

    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for shear waves in a 2D isotropic plate.
        
        .. math:: \\overline{\\delta f}_S^{2D} = \\frac{c_S^2}{\\omega A}
        
        See Lyon, eq 8.2.5
        """
        try:
            return self.soundspeed_group**2.0 / (self.frequency.angular * self.component.area)
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    
    @property
    def wavenumber(self):
        """
        Wavenumber of shear waves.
        
        .. math:: k_S = \\frac{2 \\rho \\omega \\left( 1 + \\nu  \\right) }{E h}
        
        Langley and Heron, 1990, eq 25
        """
        return self.component.material.density * self.frequency.angular * (1.0 + self.component.material.poisson) / (self.component.material.young * self.component.thickness) 
        
    
    @property
    def impedance(self):
        return np.zeros(self.frequency.amount)
   
class Component2DPlate(ComponentStructural):
    """
    Two-dimensional plate component.
    """

    thickness = None
    """
    Thickness of the plate.
    """
    
    area = None
    """
    Area of the plate.
    """
    
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
    def mass_per_area(self):
        """
        Mass per area
        
        .. math:: m^{''} = \\rho t
        
        """
        return self.material.density * self.thickness
    
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the plate by :math:`\\sqrt{12}`.
        
        .. math:: \\kappa = \\frac{h}{\\sqrt{12}}
        
        See Lyon, above eq. 8.2.5
        """
        return self.thickness / np.sqrt(12.0)
        
        
    @property
    def area_moment_of_inertia(self):
        """
        Area moment of inertia.
        
        .. math:: J = \\frac{t^3}{12}
        
        
        Following equation includes resistance to deflection and is thus part of the bending wave subsystem:
        .. math:: J = \\frac{t^3}{12 \\left( 1 - \\nu^2 \\right)}
        """
        return self.thickness**3.0 / 12.0
        #return self.thickness**3.0 / (12.0 * (1.0 - self.poisson()**2.0))
 


   