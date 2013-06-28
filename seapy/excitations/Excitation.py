from ..base import Base

import abc
import math
import cmath
import numpy as np

class Excitation(Base):
    """Abstract Base Class for excitations."""
    __metaclass__ = abc.ABCMeta
    
    SORT = 'Excitation'

    
    power = None
    """
    Input power in watt :class:`numpy.ndarray`
    """
    
    def __init__(self, name, subsystem, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: Component
        :type system: :class:`SeaPy.system.System`
        
        """
        self.subsystem = subsystem
        Base.__init__(self, name, subsystem.system, **properties)
    
        

    def _get_subsystem(self):
        return self._subsystem
    
    def _set_subsystem(self, x):
        self._set_link('subsystem', 'linked_excitations', x)
    
    _subsystem = None
    subsystem = property(fget=_get_subsystem, fset=_set_subsystem)
    """
    Subsystem that is being excited by this excitation
    """
    