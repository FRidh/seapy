
import abc
import math
import cmath
import numpy as np

import weakref

from ..base import Base

class Material(Base):
    """
    Abstract Material Class
    """
    __metaclass__ = abc.ABCMeta
    
    SORT = 'Material'
    


    density = 0.0
    """
    Density :math:`\\rho` of the material.
    """
    
    loss_factor = np.array([0.0])
    """
    Loss factor :math:`\\eta` of the material.
    """
    
    temperature = 0.0
    """
    Temperature :math:`T`
    """
      
    pressure = 0.0
    """
    Pressure :math:`p`
    """

    bulk = 0.0
    """
    Bulk modulus
    """
    
    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: System
        :type system: :class:`SeaPy.system.System`
        
        """

        self.linked_components = list()
        """
        Components linked to this subsystem. The list contains the names of the components.
        """
        
        Base.__init__(self, name, system, **properties)
        
        
        
    def __del__(self):
        """Destructor."""
        for component in self.linked_components:
            logging.info("Deleting linked component %s", component)
            del self.system._objects[component]
        #self.system.materials.remove(self.name)
        BaseClass.__init__(self)

        
        
        