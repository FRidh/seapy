from ..base import Base

import abc
import math
import cmath
import numpy as np
import logging
import weakref


class Component(Base):
    """ Abstract Base Class for components."""
    __metaclass__ = abc.ABCMeta
    
    
    SORT = 'Component'
    
    

    
    
    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: System
        :type system: :class:`SeaPy.system.System`
        :param component: Component
        :type component: :class:`SeaPy.components.Component`
        
        """

        self.linked_connections = list()
        """Connections this component is part of."""
    
        self.linked_subsystems = list()
        """Subsystems."""
        
        Base.__init__(self, name, system, **properties)
        
        
    def __del__(self):
        """Destructor."""
        for subsystem in self.linked_subsystems:
            logging.info("Destructor %s: Deleting linked subsystem %s", self.name, subsystem)
            self.system.removeObject(subsystem)
        
        logging.info("Destructor %s: Deleting reference to linked material %s", self.name, self._material) 
        self.material.linked_components.remove(self.name)
        logging.info("Destructor %s: Deleting component from components list", self.name)
        #self.system.components.remove(self.name)
        BaseClass.__del__(self) # Inherit destructor from base class

        
    def addSubsystem(self, name, model, **properties):
        """Add subsystem to component. This method is called from the component constructor only..?"""
        obj = model(name, self.system.getObject(self.name), **properties)
        self.system._objects.append(obj)
        #obj = self.system._addObject(name, model, **properties)
        #obj = model(name, self.system.getObject(self.name), **properties)
        obj = self.system.getObject(obj.name)
        if obj:
            """If object is indeed added to the system, then add it to this component."""
            name = obj.__class__.__name__
            if name == 'SubsystemLong':
                sort = 'subsystem_long'
            elif name == 'SubsystemBend':
                sort = 'subsystem_bend'
            elif name == 'SubsystemShear':
                sort = 'subsystem_shear'
            setattr(self, sort, obj)
        return 
    
    
    def _get_material(self):
        return self._material
    
    def _set_material(self, x):
        self._set_link('material', 'linked_components', x)
        #logging.info("Setting material of %s to %s", self.name, x.name)
        #if self._material is not None:
            #logging.info("Changing material of %s from %s to %s. Removing old reference.", self.name, self._material.name, x.name)
            #for item in self.material.linked_components:
                #if item.name == self.name:
                    #self.material.linked_components.remove(item)
        #self._material = x
        #self.material.linked_components.append(weakref.proxy(self))
        
    def _del_material(self):
        self._material = None
    
    _material = None
    material = property(fget=_get_material, fset=_set_material, fdel=_del_material)
    """
    Material which this component consists of.
    """

    
    volume = None
    """
    Volume :math:`V` of the component.
    """
    
    def _get_mass(self):
        if self._mass == None:
            return self.volume * self.material.density
    
    def _set_mass(self, x):
        self._mass = x
    
    _mass = None
    mass = property(fget=_get_mass, fset=_set_mass)
    """Mass :math:`m` of the component.
    
    :rtype: :class:`float`
    
    .. math:: m = \\rho V 

    """   
    
        
        

