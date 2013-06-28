"""
This module contains a class to describe physical connections between :mod:`Sea.model.components`.
"""
import math
import cmath
import numpy as np

import warnings # Handling of warnings
import abc      # Abstract base classes
import logging  # Add logging functionality
import weakref

from ..base import Base

class Connection(Base):
    """Class for connections between components."""
    #__metaclass__ = abc.ABCMeta
    
    SORT = 'Connection'
    

    
    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: System
        :type system: :class:`SeaPy.system.System`
        """
        Base.__init__(self, name, system, **properties)
        
        self.components = list()
        """
        List of components that are connected through this connection. 
        Every list item is (or should be ?!) a tuple (component, mount) where mount is a string 
        describing whether the component is mounted at an edge or far from the edge, 
        and component is a weak reference to the component.
        """
    
    @property
    def subsystems(self):
        """
        List of all subsystems in this connection.
        """
        subsystems = list()
        for component in self.components:
            subsystems += component.subsystems
        return subsystems 
    
    
    couplings = list()
    """
    List of all couplings.
    """
    
    
    def addComponent(self, component, mount):
        """
        Add component to connection.
        
        :param component: Component
        :param mount: how component is mounted
        
        """
        if component.name not in [item[0].name for item in self.components]:
            self.components.append((component, mount))
        else:
            pass
    
    def removeComponent(self, component):
        """Remove component from connection."""
        for item in self.components:
            if item[0].name == component.name:
                self.components.remove(item)
        
    def addCouplings(self):
        """Add all possible couplings to the connection."""
        pass
    
    
    @property
    def impedance(self):
        """Total impedance at the coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        imp = np.zeros(len(self.omega))
        print self.subsystems
        for subsystem in self.subsystems.iteritems():
            print subsystem.impedance
            imp = imp + subsystem.impedance
        return impedance
    
    #def get_coupling(self, subsystem_from, subsystem_to):
        #"""Return the coupling between subsystems for calculations.
        #"""
        #return
    
    
    #@property
    #def routes(self):
        #"""
        #Create a list.
        #"""
        #return [(couplings.subsystem_from, coupling.subsystem_to) for coupling in couplings]
    
