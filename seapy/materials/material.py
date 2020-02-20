"""
Material
--------

This module defines the base class for materials.

An instance of a material represents a material in a certain state.
When state variables such as temperature, pressure and volume
are different between components, new materials need to be added.

.. autoclass:: Material

"""
import abc
import math
import cmath
import numpy as np

from weakref import WeakSet
import logging

from ..base import Base, Attribute, LinkedList


class Material(Base):
    """
    Abstract Material Class
    """

    SORT = "Material"

    _DEPENDENCIES = []

    density = Attribute()
    """
    Density :math:`\\rho` of the material.
    """

    temperature = Attribute()
    """
    Temperature :math:`T` in kelvin.
    """

    bulk = Attribute()
    """
    Bulk modulus
    """

    loss_factor = Attribute()
    """
    Loss factor :math:`\\eta` of the material.
    """

    linked_components = LinkedList()
    """
    Components linked to this subsystem.
    """

    def __init__(self, name, system, **properties):
        """Constructor.

        :param name: Name
        :type name: :func:`str`
        :param system: System
        :type system: :class:`seapy.system.System`

        """
        super().__init__(name, system, **properties)

    def disable(self, components=False):
        """
        Disable this material. Optionally disable dependent components.

        :param components: Disable components
        :type components: bool
        """
        self.__dict__["enabled"] = False

        if components:
            for component in self.linked_components:
                component.disable()

    def enable(self, components=False):
        """
        Enable this material. Optionally enable dependent components.

        :param components: Enable components
        :type components: bool
        """
        self.__dict__["enabled"] = True

        if components:
            for component in self.linked_components:
                component.enable()

    def __del__(self):
        """Destructor."""
        for component in self.linked_components:
            logging.info("Deleting linked component %s", component)
            self.system.remove_object(component)
            # del self.system._objects[component]
        # self.system.materials.remove(self.name)
        super().__del__()
