"""
This module contains a class to describe physical junctions between :mod:`Sea.model.components`.
"""
import math
import cmath
import numpy as np

import warnings  # Handling of warnings
import abc  # Abstract base classes
import logging  # Add logging functionality
from weakref import WeakSet, WeakKeyDictionary

import warnings
import itertools

import collections
from toolz import unique

from ..base import Base, LinkedList

from seapy.couplings import couplings_map

coupling_options = {
    ("Point", "Component1DBeam", "Component1DBeam"): "Coupling1DStructural",
    ("Line", "Component1DBeam", "Component1DBeam"): "Coupling1DStructural",
    ("Surface", "Component1DBeam", "Component1DBeam"): "Coupling1DStructural",
    ("Point", "Component2DPlate", "Component2DPlate"): "Coupling1DStructural",
    ("Line", "Component2DPlate", "Component2DPlate"): "CouplingLineStructural",
    # ('Surface', 'Component2DPlate', 'Component2DPlate') : 'CouplingSurfaceStructural',
    (
        "Surface",
        "Component2DPlate",
        "Component3DAcoustical",
    ): "CouplingSurfacePlateAcoustical",
    (
        "Surface",
        "Component3DAcoustical",
        "Component2DPlate",
    ): "CouplingSurfaceAcousticalPlate",
    (
        "Surface",
        "Component3DAcoustical",
        "Component3DAcoustical",
    ): "CouplingSurfaceAcoustical",
}
"""Map of couplings.

The keys are tuples of the form `(shape, component_sort_a, component_sort_b)`.

"""

junction_shapes = ["Point", "Line", "Surface"]
"""Possible junction shapes.
"""

junction_mounts = ["corner", "length"]
"""Possible junction mounts.
"""


class Junction(Base):
    """Class for junctions between components."""

    # __metaclass__ = abc.ABCMeta

    SORT = "Junction"

    _DEPENDENCIES = []

    @property
    def shape(self):
        """Shape of the junction.
        
        .. seealso:: :attr:`seapy.junctions.junction_shapes`
        """
        return self.__dict__["shape"]

    @shape.setter
    def shape(self, x):
        if x in junction_shapes:
            self.__dict__["shape"] = x
        else:
            raise ValueError("Invalid shape.")

    # _components = WeakKeyDictionary()
    """
    Dictionary containing how components are connected/mounted.
    
    The keys are the names of the components and the values are names of the mount types.
    
    When a component is removed from :attr:`components` it is removed from this dictionary as well.
    """

    linked_couplings = LinkedList()
    """
    All couplings.
    """

    def __init__(self, name, system, shape, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: System
        :type system: :class:`SeaPy.system.System`
        """
        self._components = WeakSet()

        super().__init__(name, system, **properties)

        # self._components = WeakKeyDictionary()
        """
        Set of components that are connected through this junction. 
        
        Every list item is (or should be ?!) a tuple (component, mount) where mount is a string 
        describing whether the component is mounted at an edge or far from the edge, 
        and component is a weak reference to the component.
        
        Convert to a custom many-to-many link! 
        """

        self.shape = shape

    def _save(self):
        attrs = super()._save()
        attrs["shape"] = self.shape
        return attrs

    @property
    def components(self):
        """
        Components that are part of this junction.
        """
        yield from self._components

    @components.setter
    def components(self, items):
        if isinstance(items, collections.abc.Iterable):
            objects = (self.system._get_real_object(obj) for obj in items)
            self._components.clear()
            self._components.update(objects)
        else:
            raise ValueError("Components can only be set with an iterable.")

    @property
    def subsystems(self):
        """Subsystems that are used in this junction.
        
        :returns: Generator
        
        .. seealso:: :meth:`subsystems_available`
        
        """
        yield from (
            self.system.get_object(name)
            for name in unique(
                itertools.chain(
                    *(
                        (coupling.subsystem_from.name, coupling.subsystem_to.name)
                        for coupling in self.linked_couplings
                    )
                )
            )
        )

    @property
    def subsystems_available(self):
        """All available subsystems in this junction.
                
        :returns: Generator
        
        The method :meth:`subsystems` lists all the subsystems that are used in couplings in this junction.
        This method lists all the subsystems that are part of the components in this junction. 
        It therefore also includes subsystems that are not coupled to others.
        
        .. seealso:: :meth:`subsystems`
        
        """
        yield from itertools.chain(
            *(component.linked_subsystems for component in self.components)
        )

    def add_component(self, component):
        """Add component to junction.
        """
        component = self.system._get_real_object(component)
        self._components.add(component)
        return self

    def remove_component(self, component):
        """
        Remove component from junction.
        
        :param component: Component to be removed.
        
        """
        obj = self.system.get_object(component)
        self._components.remove(obj)

        # for item in self.components.filter(name=component.name):
        # self._removeMount()
        # self.components.remove(item)
        # for item in self.components:
        # if item.name == component.name:
        # self.components.remove(item)

    # def add_component(self, component, mount):
    # """
    # Add component to junction. Updates couplings automatically.

    #:param component: Component
    #:param mount: how component is mounted

    # """
    # component = self.system.get_object(component)
    # if component not in self.components:
    # self._components.add(component)
    # self.setMount(component, mount)
    # self._update_couplings()
    # else:
    # warnings.warn('Component is already part of junction. Not adding again.')

    # @property
    # def mounts(self):
    # """
    # Dictionary describing how components are mounted/connected.

    #:rtype: dict
    # """
    # yield from self._components.items()
    ##return self._mount.copy()#[(c, m) for c, m in self._mount.items()]

    # def get_mount(self, component):
    # """
    # Retrieve how the component is mounted/connected.
    # """
    # try:
    # return self._mount[component.name]
    # except KeyError:
    # warnings.warn('Component does not exist.')

    # def setMount(self, component, mount):
    # """
    # Set how a component is mounted/connected.

    #:param component: Component. Type or name.
    #:param mount: Type of mounting.
    #:type mount: :func:`str()`

    #:returns: None
    # """
    # component = self.system.get_object(component)
    # if component in self.components:
    # if mount in junction.mounts:
    # self._mount[component] = mount
    # else:
    # warnings.warn('Mount type does not exist.')
    # else:
    # warnings.warn('Component does not exist.')

    # def _removeMount(self, component):
    # """Remove mount."""
    # del self._mount[component]

    def disable(self, couplings=False):
        """
        Disable this junction. Optionally disable junctions' couplings.
        
        :param couplings: Disable couplings
        :type couplings: bool
        """
        self.__dict__["enabled"] = False

        if couplings:
            for coupling in self.linked_couplings:
                coupling.disable()

    def enable(self, couplings=False):
        """
        Enable this junction. Optionally enable junctions' couplings.
        
        :param couplings: Enable couplings
        :type couplings: bool
        """
        self.__dict__["enabled"] = True

        if couplings:
            for coupling in self.linked_couplings:
                coupling.enable()

    def add_coupling_manual(
        self, name, model, subsystem_from, subsystem_to, **properties
    ):
        """
        Add a coupling to the junction, specifying manually which `model` to use for the coupling.
        
        :param name: Name of coupling.
        :param model: Model or type of coupling. See :attr:`seapy.couplings.couplings_map`.
        :param properties: Other properties. Note that `subsystem_from` and `subsystem_to` are required.
        
        """
        properties["subsystem_from"] = subsystem_from
        properties["subsystem_to"] = subsystem_to
        properties["junction"] = self
        obj = self.system.add_coupling(name, model, **properties)

        # obj = self.system._add_object(name, objects_map['couplings'][model] , **properties)
        return obj

    def add_coupling(self, subsystem_from, subsystem_to, name=None, **properties):
        """
        Add coupling to junction.
        
        :param subsystem_from: Subsystem from
        :param subsystem_to: Subsystem to
        """

        try:
            model = coupling_options[
                (
                    self.shape,
                    subsystem_from.component.__class__.__name__,
                    subsystem_to.component.__class__.__name__,
                )
            ]
        except KeyError:
            raise ValueError(
                "No suitable model found for the combination of subsystems and junction shape."
            )
        if not name:
            name = subsystem_from.name + "_" + subsystem_to.name

        obj = self.add_coupling_manual(name, model, subsystem_from, subsystem_to)
        return obj
        # coupling = couplings_map[model](name, self.system.get_object(self.name), sub_from, sub_to)

        # self.system._objects.append(coupling)

        # print( self.system.couplings())

        # coupling = self.system.get_object(coupling.name)

    def remove_coupling(self, coupling):
        """
        Remove coupling from junction.
        """
        self.system.remove_object(coupling)

    def _remove_couplings(self):
        """
        Remove all couplings from junction.
        """
        for coupling in self.linked_couplings:
            self.remove_coupling(coupling)

    def _update_couplings(self):
        """
        Add all possible couplings to the junction.
        """
        self._remove_couplings()  # This is not so elegant. Instead try to apply only the changes, since this might delete user-added values

        for sub_a, sub_b in itertools.permutations(self.subsystems_available, 2):
            try:
                self.add_coupling(sub_a, sub_b)
            except ValueError:
                pass

    def update_couplings(self):
        """
        Update couplings. 
        
        .. attention:: List of couplings should already be kept up to date. Is it neccessary to expose this function?
        """
        self._update_couplings()

    @property
    def impedance(self):
        """Total impedance at the coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        impedance = np.zeros(len(self.frequency))
        for subsystem in self.subsystems:
            impedance += subsystem.impedance
        return impedance

    # def info(self):
    # """

    # def get_coupling(self, subsystem_from, subsystem_to):
    # """Return the coupling between subsystems for calculations.
    # """
    # return

    # @property
    # def routes(self):
    # """
    # Create a list.
    # """
    # return [(couplings.subsystem_from, coupling.subsystem_to) for coupling in couplings]
