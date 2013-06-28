import abc
import math
import cmath
import numpy as np
import logging

import warnings
import weakref

class Base(object):
    """
    Abstract Base Class for all components, connections, 
    materials, subsystems, couplings and excitation.
    """
    __metaclass__ = abc.ABCMeta

    
    def _get_name(self):
        return self._name
    
    def _set_name(self, x):
        """Allow name only to be set once."""
        if self.name is None:
            """Set unique name."""
            names = [obj.name for obj in self.system.objects]
            if x in names:
                warnings.warn('Name %s is not unique.', x)
                x += '1'
            self._name = x
            
    _name = None
    name = property(fget=_get_name, fset=_set_name)
    
    def _set_link(self, local, remote, x):
        """Set attribute `link` to `x` and inform `remote` of the update.
        
        :param local: Name of local attribute
        :type local: string
        :param remote: Name of remote attribute
        :type remote: string
        :param x: Value of new local attribute.
        :type x: any
        """
        logging.info("Setting % of %s to %s", local, self.name, x.name)
        if getattr(self, '_' + local) is not None:
            logging.info("Changing %s of %s from %s to %s. Removing old reference.", local, self.name, getattr(self, '_'+local).name, x.name)
            for item in getattr(getattr(self, local), remote):
                if item.name == self.name:
                    getattr(getattr(self, local), remote).remove(item)
        setattr(self, '_'+local, x)
        getattr(getattr(self, local), remote).append(weakref.proxy(self))

    
    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier of object
        :type name: string
        :param system: system objects belongs to
        :type system: :class:`SeaPy.system.System`
        :param: properties: Optional properties
        :type properties: dict
        """
        
        self.system = system
        """Reference to System this object belongs to."""
        
        self.name = name
        """Unique identifier of object."""
    
        
        if properties:
            for key, value in properties.iteritems():
                if hasattr(self, key):
                    print key
                    setattr(self, key, value)
        
        logging.info("Constructor %s: Created object %s of type %s", self.name, self.name, str(type(self)))
        
    def __del__(self):
        """Destructor.
        """
        pass
    
    
    @property
    def frequency(self):
        """
        Frequency object
        """
        return self.system.frequency

    def _get_spectrum(self):
        pass
    
    def _set_spectrum(self, x):
        pass
    
    def newSpectrum(self, name):
        setattr(self, '_' + name, Spectrum(self.frequency))
        setattr(self, name, property(fget=_get_spectrum, fset=_set_spectrum))