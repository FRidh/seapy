"""
Room 2D
-------

Classes describing a two-dimensional cavity.

.. autoclass:: seapy.components.acoustical2d.Component2DAcoustical

Subsystems
++++++++++

.. autoclass:: seapy.components.acoustical2d.SubsystemLong

"""
import numpy as np
from .acoustical import ComponentAcoustical
from ..subsystems import SubsystemAcoustical

class SubsystemLong(SubsystemAcoustical):
    """
    Subsystem for a fluid in a 2D cavity.
    """

    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for a fluid in a thin, flate space.
        Valid for :math:`f < c_0 / 2h` where `h` is the thickness of the layer.
        
        .. math:: \\overline{\\delta f}_0^{2D} = \\frac{c_0^2}{\\omega  A}
        
        See Lyon, eq 8.2.12
        """
        return self.soundspeed_group**2.0 / (self.frequency.angular * self.component.area)
    

class Component2DAcoustical(ComponentAcoustical):
    """
    Component for a fluid in a 2D cavity.
    """

    SUBSYSTEMS = {'Long': SubsystemLong}


    area = None
    """Area :math:`A` of cavity.
    """
    
    thickness = None
    """Thickness or width of cavity.
    """
    
    @property
    def volume(self):
        """Volume of cavity.
        """
        return self.area * self.thickness
