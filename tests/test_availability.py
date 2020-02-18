"""
With seapy it is possible to enable and disable the different nodes. This module
tests whether that behaves as expected.
"""

import unittest

from acoustics.signal import OctaveBand
import seapy


class TestAvailabilityObjects(unittest.TestCase):
    def setUp(self):
        """Code run before each unit test."""
        frequency = OctaveBand(fstart=500.0, fstop=8000.0, fraction=1)
        self.system1 = seapy.system.System(frequency)
        self.material = self.system1.add_material("steel", "MaterialSolid")
        self.beam1 = self.system1.add_component(
            "beam1", "Component1DBeam", material=self.material
        )
        self.beam2 = self.system1.add_component(
            "beam2", "Component1DBeam", material=self.material
        )
        self.junction = self.system1.add_junction(
            "junction1", "Junction", shape="Point"
        )
        self.junction.add_component(self.beam1)  # , "corner")
        self.junction.add_component(self.beam2)  # , "corner")

    def tearDown(self):
        """Code run after each test."""
        self.system1 = None
        self.material = None
        self.beam1 = None
        self.beam2 = None
        self.junction = None

    def test_disabling_material(self):
        """Test disabling material."""
        self.material.disable()  # Cause

        # We disable it so its not enabled
        self.assertFalse(self.material.enabled)

        # Therefore it also is not included in the analysis
        self.assertFalse(self.material.included)

        # The beams need this material, so they cannot be included either.
        self.assertFalse(self.beam1.included)
        self.assertFalse(self.beam2.included)

        # And if the beams are not included, the junction they are used in
        # is not included either.
        # self.assertFalse(self.junction.included) # Broken!

    def test_disabling_subsystem(self):
        """Testing disabling a subsystem."""
        sub = list(self.beam1.linked_subsystems)[0]

        sub.disable()  # Cause

        self.assertFalse(sub.enabled)
        self.assertFalse(sub.included)
        # self.assertFalse(list(sub.linked_couplings_from(included=True)))
        # self.assertFalse(list(sub.linked_couplings_from(included=False)))


if __name__ == "__main__":
    unittest.main()
