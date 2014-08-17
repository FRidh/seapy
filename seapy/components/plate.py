"""
Plate
-----

.. autoclass:: seapy.components.plate.Component2DPlate

Subsystems
++++++++++

.. autoclass:: seapy.components.plate.SubsystemLong
.. autoclass:: seapy.components.plate.SubsystemBend
.. autoclass:: seapy.components.plate.SubsystemShear

Classes describing a two-dimensional plate.
"""

import numpy as np
from .structural import ComponentStructural
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
        
        with:
        
        * Young's modulus :math:`E`
        * density :math:`\\rho`
        * Poisson's ratio :math:`\\mu`
        
        See Lyon, above eq 8.2.5 
        
        See Craik, table 3.2, third row, page 49.
        
        Often the density is replaced as a surface density (mass per unit area) and the thickness or height of the plate.
        """
        return np.ones(len(self.frequency)) * np.sqrt(self.component.material.young / (self.component.material.density * (1.0 - self.component.material.poisson**2.0)))

            
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
        
        with:
        
        * soundspeed of longitudinal waves :math:`c_L`
        * angular frequency :math:`\\omega`
        * plate area :math:`A`
        
        See Lyon, equation 8.2.8
        """
        #try:
        return  self.soundspeed_group**2.0 / (self.frequency.angular * self.component.area)
        #except FloatingPointError:
            #return np.zeros(len(self.frequency))

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
        raise NotImplementedError
        
    #@property
    #def wavenumber(self):
        #"""
        #Wavenumber of longitudinal waves in a plate.
        
        #.. math:: k_L = \\frac{ \\rho \\omega \\left( 1 - \\nu \\right) }{E h}
        
        #Langley and Heron, 1990, eq 24.
        #"""
        #return self.component.material.density * self.omega * (1.0 - self.component.material.poisson) / (self.component.material.young * self.component.height)
    
        
class SubsystemBend(SubsystemStructural):
    """
    Subsystem for bending waves in a 2D isotropic component.
    """

    @property
    def soundspeed_phase(self):
        """Phase velocity for bending wave.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: \\sqrt{\\omega} \\left( \\frac{B}{\\rho_s}  \\right)^(1/4)
        
        with:
        
        * Angular frequency :math:`\\omega`
        * Bending stiffness :math:`B`
        * surface density :math:`\\rho_s`
        
        See Craik, equation 5.19, page 128.
        
        Note that this is the same as
        
        .. math:: c_{B,\\phi}^{2D} = \\sqrt{\\omega \\kappa c_L^{'}}
        
        See Lyon, above eq. 8.2.5
        """
        return (self.frequency.angular**2.0 * self.flexural_rigidity / self.component.mass_per_area) **(0.25)
        #return np.sqrt(self.frequency.angular * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_phase)
                
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
        
        with:
        
        * radius of gyration :math:`\\kappa`
        * soundspeed of longitudinal waves :math:`c_L`
        * plate area :math:`A`
        
        See Lyon, eq 8.2.5
        """
        return 2.0 * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_group / self.component.area
    
    @property
    def wavenumber(self):
        """Wavenumber of flexural waves in a plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: k_B = \\sqrt[4]{ \\frac{ \\rho \\omega }{B}} 
        
        with:
        
        * density of the plate :math:`\\rho`
        * angular frequency :math:`\\omega`
        * flexural rigidity :math:`B`
        
        See Langley and Heron, 1990, eq 18.
        """
        return np.power(self.component.material.density * self.frequency.angular / self.flexural_rigidity, 0.25)
    
    @property
    def flexural_rigidity(self):
        """Flexural rigidity of a plate.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: B = \\frac{E h^3}{12 \\left( 1 - \\nu^2 \\right)}
        
        with:
        
        * Young's modulus :math:`E`
        * plate thickness/height :math:`h`
        * Poisson's ratio :math:`\\nu`
        
        See Craik, equation 3.2, page 48.
        
        """
        return self.component.material.young * self.component.height**3.0 / (12.0 * (1.0 - self.component.material.poisson**2.0))
    
    #@property
    #def impedance(self):
        #"""Impedance.
        
        #:rtype: :class:`numpy.ndarray`
        
        #"""
        #raise NotImplementedError
    
    
    @property
    def impedance_point_force(self):
        """Point impedance.
        
        .. math:: Z_{B}^{F, 2D} = 8 \\rho h \\kappa_B c_L
        
        with:
        
        * density of the plate :math:`\\rho`
        * radius of gyration :math:`kappa_B`
        * soundspeed of longitudinal waves :math:`c_L`
        
        See Lyon, page 201, table 10.1
        
        """
        return 8.0 * self.component.material.density * self.component.height * self.component.radius_of_gyration * self.component.subsystem_long.soundspeed_group
        
        
    
    
class SubsystemShear(SubsystemStructural):
    """
    Subsystem for shear waves in a 2D isotopic component.
    """
    
    @property
    def soundspeed_phase(self):
        """
        Phase velocity for shear waves in a 2D isotropic plate.
        
        .. math:: c_S = \\sqrt{\\frac{G}{\\rho}}
        
        with:
        
        * shear modulus :math:`G`
        * density of the plate :math:`\\rho`
        
        See Lyon, above eq. 8.2.5
        """
        return np.ones(len(self.frequency)) * np.sqrt(self.component.material.shear / self.component.material.density)
        
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
        
        with:
        
        * soundspeed of shear waves :math:`c_S`
        * angular frequency :math:`\\omega`
        * area of the plate :math:`A`
        
        See Lyon, eq 8.2.5
        """
        #try:
        return self.soundspeed_group**2.0 / (self.frequency.angular * self.component.area)
        #except FloatingPointError:
            #return np.zeros(len(self.frequency))
    
    @property
    def wavenumber(self):
        """
        Wavenumber of shear waves.
        
        .. math:: k_S = \\frac{2 \\rho \\omega \\left( 1 + \\nu  \\right) }{E h}
        
        with:
        
        * density :math:`\\rho`
        * angular frequency :math:`\\omega`
        * Poisson's ratio :math:`\\nu`
        * Young's modulus :math:`E`
        * plate thickness :math:`h`
        
        Langley and Heron, 1990, eq 25
        """
        return self.component.material.density * self.frequency.angular * (1.0 + self.component.material.poisson) / (self.component.material.young * self.component.height) 
        
    
    @property
    def impedance(self):
        raise NotImplementedError
   
class Component2DPlate(ComponentStructural):
    """
    Two-dimensional plate component.
    
    The following subsystems are implemented for this component:
    
    * :class:`seapy.components.plate.SubsystemLong`
    * :class:`seapy.components.plate.SubsystemBend`
    * :class:`seapy.components.plate.SubsystemShear`
    
    """
    
    SUBSYSTEMS = {'subsystem_long': SubsystemLong,
                  'subsystem_bend': SubsystemBend,
                  'subsystem_shear': SubsystemShear}
    @property
    def area(self):
        """Area of the plate.
        
        .. math:: A = l w
        
        with:
        
        * length :math:`l`
        * width :math:`w`
        
        """
        return self.length * self.width
    
    @property
    def mass_per_area(self):
        """
        Mass per unit area. Also called the surface density.
        
        .. math:: m^{''} = \\rho h
        
        with:
        
        * density :math:`\\rho`
        * plate thickness/height :math:`h`
        
        """
        return self.material.density * self.height
    
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the height of the plate by :math:`\\sqrt{12}`.
        
        .. math:: \\kappa = \\frac{h}{\\sqrt{12}}
        
        with:
        
        * plate thickness/height :math:`h`
        
        See Lyon, above eq. 8.2.5
        """
        return self.height / np.sqrt(12.0)
        
        
    @property
    def area_moment_of_inertia(self):
        """
        Area moment of inertia.
        
        .. math:: J = \\frac{h^3}{12}
        
        with:
        
        * plate thickness/height :math:`h`
        
        
        Following equation includes resistance to deflection and is thus part of the bending wave subsystem:
        
        .. math:: J = \\frac{h^3}{12 \\left( 1 - \\nu^2 \\right)}
        
        """
        return self.height**3.0 / 12.0
        #return self.height**3.0 / (12.0 * (1.0 - self.poisson()**2.0))
 
