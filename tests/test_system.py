import numpy as np
import seapy

import pytest

from .common import steel_attributes, system


class TestSystem:
    """
    New system.
    """

    def test_new_system(self, system):
        """
        New System.
        """
        pass

    # def test_frequencies(self):
    #     frequency = OctaveBand(fstart=500.0, fstop=8000.0, fraction=1)
    #     system1 = seapy.system.System(frequency)

    # Setting is not yet implemented
    #     system1.frequency.center = [500.0, 1000.0, 2000.0, 4000.0, 8000.0]
    #     system1.frequency.lower = [355.0, 710.0, 1420.0, 2840.0, 5680.0]
    #     system1.frequency.upper = [710.0, 1420.0, 2840.0, 5680.0, 11360.0]
    #     system1.frequency.enabled = [False, False, True, True, True]


class TestNewObject:
    """Test adding a new object to the System.
    """

    def test_add_material(self, system, steel_attributes):
        """
        Add material.
        """
        steel = system.add_material(**steel_attributes)

        assert len(list(system.objects)) == 1
        assert len(list(system.materials)) == 1
        assert len(list(steel.linked_components)) == 0

    def test_add_component(self, system, steel_attributes):
        """
        Add component.
        """
        steel = system.add_material(**steel_attributes)

        beam1 = system.add_component(
            "beam1",
            "Component1DBeam",
            material="steel",
            length=2.0,
            width=0.5,
            height=0.6,
        )

        assert (
            len(list(system.objects)) == 5
        )  # 1 material + 1 component + 3 subsystems = 5
        assert len(list(system.materials)) == 1
        assert len(list(system.components)) == 1
        assert len(list(steel.linked_components)) == 1

        # assert(steel.__dict__['linked_components'][0] == 'beam1')
        # assert(list(steel.linked_components)[0] == beam1)
        # assert(isinstance(list(steel.linked_components)[0], weakref.ProxyTypes))

        system.remove_object("beam1")

    def test_add_junction(self, system):
        """
        Add junction.
        """
        junction1 = system.add_junction("junction1", "Junction", shape="Point")
        assert len(list(system.junctions)) == 1

    def test_add_excitation(self, system, steel_attributes):
        """
        Add junction.
        """
        steel = system.add_material(**steel_attributes)

        beam1 = system.add_component(
            "beam1",
            "Component1DBeam",
            material="steel",
            length=2.0,
            width=0.5,
            height=0.6,
        )

        subsystem1 = beam1.subsystem_long
        ex1 = subsystem1.add_excitation(
            "ex1",
            "ExcitationPointForce",
            force=1.0,
            velocity=0.0,
        )
        assert len(list(system.excitations)) == 1
