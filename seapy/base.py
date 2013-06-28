"""
Base
====

The Base module contains some of the foundations of the SEA framework, like the :class:`Base` class.

Base
----

.. autoclass:: seapy.base.Base


LinkedList
----------

.. autoclass:: seapy.base.LinkedList

Descriptors
-----------

.. autoclass:: seapy.base.Spectrum
.. autoclass:: seapy.base.Name
.. autoclass:: seapy.base.Link
.. autoclass:: seapy.base.MaterialLink
.. autoclass:: seapy.base.ComponentLink
.. autoclass:: seapy.base.JunctionLink
.. autoclass:: seapy.base.SubsystemFromLink
.. autoclass:: seapy.base.SubsystemToLink
.. autoclass:: seapy.base.SubsystemLink


.. autoclass:: seapy.base.NameWarning

.. autoclass:: seapy.base.MetaBase

"""

import abc
import math
import cmath
import numpy as np
import logging

import warnings
from weakref import WeakSet

from .tools import plot

#from tabulate import tabulate
import pandas as pd


#class Link(object):
    #"""
    #One-to-Many link from `local` to `remotes`.
    
    #Descriptor.
    #"""
    
    #one = ''
    #"""
    #Name of the attribute this instance is assigned to.
    #"""
        
    #many = ''
    #"""
    #Name of the attribute where this link refers to.
    #"""
        
    #def __get__(self, instance, owner):
        #try:
            #return instance.system.get_object( instance.__dict__[self.one] )
        #except KeyError:
            #return None
        
    #def __set__(self, instance, value):
        
        #"""Log that we are changing the link."""
        #logging.info("Setting {} of {} to {}".format(self.one, instance.name, value))
        
        #"""Get the name of the new object that we link to."""
        #name = value if isinstance(value, str) else value.name
        #del value
        
        #"""Get the object that we link to."""
        #obj = instance.system.get_object(name)

            
        #try:
            #if getattr(instance, self.one) is not None:
                #logging.info("Changing %s of %s from %s to %s. Removing old reference.", one, instance.name, getattr(instance, self.one).name, name)
                #for item in getattr(getattr(instance, one), self.many):
                    #if item.name == instance.name:
                        #getattr(getattr(instance, one), self.many).remove(item)
        #except AttributeError:  # When self.one has not yet been set.
            #pass
        
        #"""We save the  name of the object that is assigned, not the object itself."""
        #instance.__dict__[self.one] = name

        #"""Add name of object in LinkedList of object."""
        #try:
            #l = obj.__dict__[self.many]
        #except KeyError: # In case the list doesn't exist yet...
            #l = obj.__dict__[self.many] = list()
        #l.append(instance.name)
            
    #def __delete__(self, instance):
        #setattr(instance, self.one, None)


class Link(object):
    """One-to-Many link from `local` to `remotes`.
    
    Descriptor.
    """
    
    attribute = ''
    """
    Name of the attribute this instance is assigned to.
    """
        
    remote = ''
    """
    Name of the attribute where this link refers to.
    """
        
    def __get__(self, instance, owner):
        try:
            obj = instance.system.get_object( instance.__dict__[self.attribute] )
        except KeyError:
            instance.__dict__[self.attribute] = None # Clean attribute. Replace by proxy?
            obj = None
        except AttributeError:
            return None
        return obj
        
    def __set__(self, instance, obj):
        
        """Get name and Proxy to object."""
        name = obj if isinstance(obj, str) else obj.name
        obj = instance.system.get_object(name)
        
        """Log that we are changing the link."""
        logging.info("Setting {} of {} to {}".format(self.attribute, instance.name, name))
        
        #try:
            #if getattr(instance, self.attribute) is not None:
                #logging.info("Changing %s of %s from %s to %s. Removing old reference.", one, instance.name, getattr(instance, self.attribute).name, name)
                #for item in getattr(getattr(instance, attribute), self.reference):
                    #if item.name == instance.name:
                        #getattr(getattr(instance, attribute), self.reference).remove(item)
        #except AttributeError:  # When self.attribute has not yet been set.
            #pass
        
        """We save the  name of the object that is assigned, not the object itself."""
        instance.__dict__[self.attribute] = name

        """Add name of object in LinkedList of object."""
        #try:
            #l = obj.__dict__[self.reference]
        #except KeyError: # In case the list doesn't exist yet...
            #l = obj.__dict__[self.reference] = list()
        items = obj.__dict__[self.reference]#getattr(obj, self.reference)#obj.__dict__[self.reference]
        items.add(instance)
            
    def __delete__(self, instance):
        setattr(instance, self.attribute, None)


class MaterialLink(Link):
    """
    Linked from component to material.
    
    .. seealso:: :attr:`seapy.components.component.Component.material`
    
    """
    attribute = 'material'
    reference = 'linked_components'
    
class ComponentLink(Link):
    """
    Link from subsystem to component.
    
    .. seealso:: :attr:`seapy.subsystems.subsystem.Subsystem.component`
    
    """
    attribute = "compattributent"
    reference = "linked_subsystems"

class JunctionLink(Link):
    """
    Link from coupling to junction.
    
    .. seealso:: :attr:`seapy.couplings.coupling.Coupling.junction`
    
    """
    attribute = "junction"
    reference = "linked_couplings"

class SubsystemFromLink(Link):
    """
    Linked from coupling `from` to subsystem `from`.
    
    .. seealso:: :attr:`seapy.couplings.coupling.Coupling.subsystem_from`
    
    """
    attribute = "subsystem_from"
    reference = "linked_couplings_from"
    
class SubsystemToLink(Link):
    """
    Link from coupling `to` to subsystem `to`.
    
    .. seealso:: :attr:`seapy.couplings.coupling.Coupling.subsystem_to`
    
    """
    attribute = "subsystem_to"
    reference = "linked_couplings_to"
    
class SubsystemExcitationLink(Link):
    """
    Link from excitation to subsystem.
    """
    attribute = "subsystem"
    reference = "linked_excitations"


#class Linked(object):
    
    #attribute = ''
    
    #def __get__(self, instance, owner):
        
        #pass


class LinkedList(object):
    """
    Receiving Many part of One-to-Many link.
    """
    
    attribute = ''
    """
    Name of attribute of owner of this object.
    """

        
    def __get__(self, instance, owner):
        #try:
        items = instance.__dict__[self.attribute]
        #except KeyError:
            #instance.__dict__[self.attribute] = WeakSet()
            #items = instance.__dict__[self.attribute]
        yield from items
        
        #print (l)
        ##yield from (instance.system.get_object(item) for item in l if item in (obj.name for obj in instance.system.objects))
        ##print( l)
        #for item in l:
            ##print (instance.system)
            #try:
                #obj = instance.system.get_object(item)
            #except ReferenceError:
                #obj = instance.system.get_object(next(l))
            #yield obj
                
        ##yield from (instance.system.get_object(item) for item in l)
        #items = [instance.system.get_object(item) for item in l]
        #yield from items

    #def __set__(self, instance, value):
        #if instance.__dict__[attribute] is None:
            #instance[attribute] = value
        #else:
            #raise ValueError("Does not allows to be set again.")
     
    def __set__(self, instance, value):
        raise ValueError("Cannot set this attribute.")
        

class NameWarning(Warning):
    """
    Duplicate name warning.
    """
    pass

class Name(object):
    """
    Unique Name descriptor.
    
    This data descriptor checks with :class:`seapy.system.System` whether a name is not yet taken.
    In case the name is taken an integer is added to it.
    
    """
    
    #def __init__(self):
        #pass
    
    def __get__(self, instance, owner):
        try:
            return instance.__dict__['name']
        except (KeyError, AttributeError) as e:
            return None
        
    def __set__(self, instance, value):
        if instance.name is None:
            """Set unique name."""
            names = (obj.name for obj in instance.system.objects)
            if value in names:
                msg = 'Name {} is not unique.'.format(str(value))
                warnings.warn(msg, NameWarning)
                value += '1'
            instance.__dict__['name'] = value
        else:
            raise ValueError("Cannot change name.")
        
        
class MetaBase(type):
    """Metaclass that prepares :class:`Base`.
    
    This metaclass
    
    * sets :attr:`LinkedList.attribute`
    * sets :attr:`Spectrum.attribute`
    
    """
    
    def __new__(cls, name, bases, attrs):

        #print(name)
        #print(bases)
        #print(attrs)
        for key, value in attrs.items():
            if isinstance(value, LinkedList):
                value.attribute = key # Inform LinkedList of attribute name.
            if isinstance(value, Spectrum):
                value.attribute = key # Inform Spectrum of attribute name.
        return super(MetaBase, cls).__new__(cls, name, bases, attrs)
    

    #def __init__(cls, name, bases, attrs):
        ## find all descriptors, auto-set their labels
        ##print( cls)
        ##for key, value in attrs.items():
            ##print(key, value)
            ##if isinstance(value, LinkedList):
                ##pass
                
                ###key = list()
                ##print (key, value)
                ##attrs[key] = WeakSet()
                ##cls.__dict__[key] = WeakSet()
                ###setattr(cls, key, WeakSet())
                ##print(getattr(cls, key))
                
                ##print(key)
                ##value.label = key
        #super(MetaBase, cls).__init__(name, bases, attrs)
    
class Spectrum(object):
    """Class capable of containing spectral values.
    
    Descriptor.
    
    """
    
    def __init__(self, dtype='float64'):
        self.dtype = dtype

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = instance.__dict__[self.attribute]
            
            try:
                length = instance.system.frequency.amount
                if length != len(value):
                    if len(value) == 1:
                        value = np.ones(length) * value
                    else:
                        raise AttributeError
            except AttributeError:
                pass
            
            return value
            #return instance.__dict__[self.attribute]
        
    def __set__(self, instance, value):
        
        if not isinstance(value, np.ndarray):   # Check whether it is an array.
            raise TypeError('Expected an ndarray')
        
        if not self.dtype == value.dtype:       # Check whether the array is of the right type.
            value = value.astype(self.dtype)
        
        try:
            length = instance.system.frequency.amount
            if not len(value) == length:    # Check the size of the array.
                raise TypeError('Expected array of length %i', length)
        except AttributeError:  # spectrum size is not yet available. Store despite possible length issue.
            pass
        
        instance.__dict__[self.attribute] = value
   
    def __delete__(self, instance):
        del instance.__dict__[self.attribute]
        
    
    
class Base(object, metaclass=MetaBase):#, metaclass=abc.ABCMeta):
    
    """
    Abstract Base Class for all components, junctions, 
    materials, subsystems, couplings and excitation.
    """

    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier of object
        :type name: string
        :param system: system objects belongs to
        :type system: :class:`seapy.system.System`
        :param properties: Optional properties
        :type properties: dict
        """

        #print (self.__class__)
        #for key, value in self.__class__.__dict__.items():
            #print(key, value)
        
        #for key, value in self.__dict__.items():
            #print( key, value)
            #if isinstance(v, LinkedList):
                #value.label = key
                
        super().__init__()
        
        self.system = system
        """Reference to System this object belongs to."""
        
        self.name = name
        """Unique identifier of object."""
        
        """Every LinkedList contains a WeakSet."""
        for cl in self.__class__.__mro__:
            for key, value in cl.__dict__.items():
                if isinstance(value, LinkedList):
                    self.__dict__[key] = WeakSet()
        
        for cl in self.__class__.__mro__:
            for key, value in cl.__dict__.items():
                if isinstance(value, Spectrum):
                    self.__dict__[key] = np.zeros(self.system.frequency.amount)
                    
                    
        #for key, value in self.__class__.__dict__.items():
            ##if isinstance(value, LinkedList):
                #print(key, value)
    
        #for key, value in self.__dict__.items():
            ##if isinstance(value, LinkedList):
                #print(key, value)

        if properties:
            for key, value in properties.items():
                #if key in self.__class__.__dict__.keys():
                #if hasattr(self, key):
                setattr(self, key, value)
        
        logging.info("Constructor %s: Created object %s of type %s", self.name, self.name, str(type(self)))
        
    def __del__(self):
        """Destructor.
        """
        pass
    
    def __str__(self):
        return "{}({})".format(self.SORT, self.name)
    
    name = Name()
    """
    Name of object.
    
    The name of the object is unique.
    
    .. seealso:: :class:`Name`
    
    
    """
    
    @abc.abstractmethod
    def disable(self):
        """
        Disable this object.
        """
    
    @abc.abstractmethod
    def enable(self):
        """
        Enable this object.
        """
    
    _DEPENDENCIES = []
    """
    Dependencies of object on other objects.
    """
    
    @property
    def included(self, extended=False):
        """
        Indicates whether the object is included in the analysis.
        
        :param extended: Whether to show a list of dependencies with outcomes.
        :type extended: bool
        
        :rtype: bool or list
        """
        if extended:
            return [(dep, getattr(getattr(self, dep), 'included')) for dep in self._DEPENDENCIES] + [('enabled', self.enabled)]
        else:
            return self.enabled and all([getattr(getattr(self, dep), 'included') for dep in self._DEPENDENCIES])
       
    _enabled = True
    """
    Container for storing whether the object is enabled or not.
    """
    
    @property
    def enabled(self):
        """
        Switch indicating whether the object is enabled.
        
        :returns: A boolean indicating whether the object is enabled (`True`) or not (`False`)
        :rtype: :func:`bool`
        """
        return self._enabled
    
    @property
    def frequency(self):
        """
        Frequency.
        
        .. seealso:: :meth:`seapy.system.System.frequency`
        
        """
        return self.system.frequency

    #def _get_spectrum(self):
        #pass
    
    #def _set_spectrum(self, x):
        #pass
    
    #def newSpectrum(self, name):
        #setattr(self, '_' + name, Spectrum(self.frequency))
        #setattr(self, name, property(fget=_get_spectrum, fset=_set_spectrum))
    
    @property
    def classname(self):
        """Name of class of the object. This is an alias for ``obj.__class__.__name__``.
        """
        return self.__class__.__name__
    
    
    def plot(self, quantity, yscale='linear'):
        """Plot `quantity`.
        
        :seealso: :func:`seapy.tools.plot`
        
        """
        return plot(self.frequency.center, [getattr(self, quantity)], quantity, self.frequency.enabled, yscale=yscale)
        
    
    def info(self, attributes=None):
        """Return dataframe."""
        data = {attr: getattr(self, attr) for attr in attributes if hasattr(self, attr)}
        df = pd.DataFrame(data, index=self.frequency.center.astype('int')).T
        return df
        
    
    #def info(self, attributes=None, tablefmt='simple'):
        #"""Information about the object."""
        #header = ['Attribute'] + self.frequency.center.astype("int").astype("str").tolist()
        #data = ([attr] + (getattr(self, attr)*np.ones(self.frequency.amount)).tolist() for attr in attributes)
        #return tabulate(data, headers=header, tablefmt=tablefmt)
           
        
                
                
        
        
        
        
        
        
        
        
        

