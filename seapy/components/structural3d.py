"""
Solid
=====

.. autoclass:: seapy.component.structural3d.Component3D

Subsystems
++++++++++

.. autoclass:: seapy.component.structural3d.SubsystemLong

"""


import numpy as np
from .structural import ComponentStructural
from ..subsystems import SubsystemStructural


class SubsystemLong(SubsystemStructural):
    """
    Subsystem from longitudinal waves in a 3D isotropic solid.
    
    """
    
    @property
    def soundspeed_group(self):
        """Group velocity for longitudinal waves in a 3D solid.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: C_L = \\left( \\frac{E}{\\rho} \\frac{\\left( 1-\\mu \\right)}{\\left( 1+\\mu\\right)\\left( 1-2\\mu \\right)}   \\right)^{0.5}

        See Craik, table 3.2, first row, page 49.
        
        """
        poisson = self.component.material.poisson
        young = self.component.material.young
        density = self.component.material.density
        return np.ones(self.frequency.amount) * np.sqrt( young / density * (1.0 - poisson / ((1.0+poisson)*(1.0-2.0*poisson)) ) )


class Component3D(ComponentStructural):
    pass
