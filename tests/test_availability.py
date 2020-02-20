"""
With seapy it is possible to enable and disable the different nodes. This module
tests whether that behaves as expected.
"""

import argparse
import pytest

import seapy

from .common import steel_attributes, system

@pytest.fixture
def objects(steel_attributes, system):
    objects = argparse.Namespace()
    objects.system = system
    objects.material = objects.system.add_material(**steel_attributes)
    objects.beam1 = objects.system.add_component(
        "beam1",
        "Component1DBeam",
        material=objects.material,
        length=2.0,
        width=0.1,
        height=0.2,
    )
    objects.beam2 = objects.system.add_component(
        "beam2",
        "Component1DBeam",
        material=objects.material,
        length=2.0,
        width=0.1,
        height=0.2,
    )
    objects.junction = objects.system.add_junction(
        "junction1",
        "Junction",
        shape="Point",
    )
    objects.junction.add_component(objects.beam1)  # , "corner")
    objects.junction.add_component(objects.beam2)  # , "corner")
    return objects

class TestAvailabilityObjects:


    def test_disabling_material(self, objects):
        """Test disabling material."""
        objects.material.disable()  # Cause

        # We disable it so its not enabled
        assert not objects.material.enabled

        # Therefore it also is not included in the analysis
        assert not objects.material.included

        # The beams need this material, so they cannot be included either.
        assert not objects.beam1.included
        assert not objects.beam2.included

        # And if the beams are not included, the junction they are used in
        # is not included either.
        # objects.assertFalse(objects.junction.included) # Broken!

    def test_disabling_subsystem(self, objects):
        """Testing disabling a subsystem."""
        sub = list(objects.beam1.linked_subsystems)[0]

        sub.disable()  # Cause

        assert not sub.enabled
        assert not sub.included
        # objects.assertFalse(list(sub.linked_couplings_from(included=True)))
        # objects.assertFalse(list(sub.linked_couplings_from(included=False)))


if __name__ == "__main__":
    unittest.main()
