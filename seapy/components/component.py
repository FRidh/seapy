"""

ABC
---

Abstract class for all components.

.. autoclass:: seapy.components.component.Component

"""

from ..base import Base, MaterialLink, LinkedList, Attribute

import abc
import math
import cmath
import numpy as np
import logging
from weakref import WeakSet


class Component(Base):
    """ Abstract Base Class for components."""

    SORT = "Component"

    material = MaterialLink()
    """
    Material which this component consists of.
    """

    _DEPENDENCIES = ["material"]  # The right way to do it...

    linked_junctions = LinkedList()
    """
    junctions this component is part of.
    """

    linked_subsystems = LinkedList()
    """
    Subsystems.
    """

    SUBSYSTEMS = {}
    """
    Dictionary with systems that are available for this component.
    By default each of these subsystems is added to the component.
    """

    length = Attribute()
    """
    Length.
    """

    height = Attribute()
    """
    Height.
    """

    width = Attribute()
    """
    Width.
    """

    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: System
        :type system: :class:`seapy.system.System`
        :param component: Component
        :type component: :class:`seapy.components.component`
        
        """
        super().__init__(name, system, **properties)

    def __del__(self):
        """Destructor."""
        # subsystems = self.linked_subsystems
        # for subsystem in self.linked_subsystems:
        # logging.info("Destructor %s: Deleting linked subsystem %s", self.name, subsystem)
        # self.system.remove_object(subsystem)

        # logging.info("Destructor %s: Deleting reference to linked material %s", self.name, self.material)
        # self.material.__dict__['linked_component'].remove(self.name)
        # logging.info("Destructor %s: Deleting component from components list", self.name)
        # self.system.components.remove(self.name)
        super().__del__()  # Inherit destructor from base class

    def disable(self, subsystems=False):
        """
        Disable this component. Optionally disable components' subsystems.
        
        :param subsystems: Disable subsystems
        :type subsystems: bool
        """
        self.__dict__["enabled"] = False

        if subsystems:
            for subsystem in self.linked_subsystems:
                subsystem.disable()

    def enable(self, subsystems=False):
        """
        Enable this coupling. Optionally enable components' subsystems.
        
        :param subsystems: Enable subsystems
        :type subsystems: bool
        """
        self.__dict__["enabled"] = True

        if subsystems:
            for subsystem in self.linked_subsystems:
                subsystem.enable()

    def _add_subsystems(self):
        """
        Add subsystems to component.
        
        .. note:: Add the mentioned subsystems to the component. 
        This function can only be called after creation of the Component 
        because it needs a weakref to the object given by system.get_object.
        It would be possible to create a weakref 'manually'.
        """

        for attribute, subsystem in self.SUBSYSTEMS.items():
            self._add_subsystem(self.name + "_" + subsystem.__name__, subsystem)

    def _add_subsystem(self, name, model, **properties):
        """
        Add subsystem to component. 
        This method is called only from :meth:`seapy.components.Component._add_subsystems`, which is called immediately after creation of the component.
        """
        properties["component"] = self.system.get_object(self.name)

        obj = model(name, self.system, **properties)
        # obj = model(name, self.system.get_object(self.name), **properties)
        self.system._objects.append(obj)
        # obj = self.system._add_object(name, model, **properties)
        # obj = model(name, self.system.get_object(self.name), **properties)
        obj = self.system.get_object(obj.name)
        # setattr(self, attribute, obj)
        return obj
        # if obj:
        # """If object is indeed added to the system, then add it to this attribute."""
        # name = obj.__class__.__name__
        # if name == 'SubsystemLong':
        # sort = 'subsystem_long'
        # elif name == 'SubsystemBend':
        # sort = 'subsystem_bend'
        # elif name == 'SubsystemShear':
        # sort = 'subsystem_shear'
        # setattr(self, sort, obj)
        # return

    def _save(self):
        attrs = super()._save()
        attrs["material"] = self.material.name
        return attrs

    @property
    def volume(self):
        """
        Volume :math:`V` of the component.
        """
        return self.length * self.width * self.height

    @property
    def mass(self):
        """Mass :math:`m` of the component.
        
        :rtype: :func:`float`
        
        .. math:: m = \\rho V 

        """
        return self.volume * self.material.density
