"""
Pipe
----

.. autoclass:: seapy.components.pipe.Component1DPipe

Subsystems
++++++++++

.. autoclass:: seapy.components.pipe.SubsystemLong
.. autoclass:: seapy.components.pipe.SubsystemBend
.. autoclass:: seapy.components.pipe.SubsystemShear


Classes describing a one-dimensional beam.
"""
import numpy as np
from .structural import ComponentStructural
from ..subsystems import SubsystemStructural


class SubsystemLong(SubsystemStructural):
    pass


class SubsystemBend(SubsystemStructural):
    pass

class SubsystemShear(SubsystemStructural):
    pass



class ComponentPipe(ComponentStructural):
    """
    One-dimensional beam component.
    """

    SUBSYSTEMS = {'Long': SubsystemLong, 
                   'Bend': SubsystemBend, 
                   'Shear': SubsystemShear}
    
    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the beam by :math:`\\sqrt{2}`.
        See Lyon, above eq. 8.1.10
        
        .. math:: \\kappa = \\frac{h}{\\sqrt{2}}
        
        """
        return self.height / 12
