import seapy
import numpy as np
import unittest


class TestFrequencySpectrum(unittest.TestCase):
    """
    Test Frequency and Spectrum objects.
    """

    def setUp(self):
        """Code run before each unit test."""
        self.system1 = seapy.system.System()
        self.system1.frequency.center = [500.0, 1000.0, 2000.0, 4000.0, 8000.0]
        self.steel = self.system1.addMaterial(
            "steel",
            "MaterialSolid",
            loss_factor=np.ones(len(self.system1.frequency.center)) * 0.2,
        )

    def tearDown(self):
        """Code run after each test."""
        # self.system1.dispose()
        self.system1 = None
        # self.steel.dispose()
        self.steel = None

    def test_new_object_with_spectrum(self):
        """
        Test whether the Spectrum of a new object has the same size as that of the Frequency object.
        """

        """should raise an exception when the size has not changed."""
        self.assertTrue(self.system1.frequency.amount == len(self.steel.loss_factor))

    def test_add_band(self):
        """
        Test of :meth:`seapy.system.Frequency.addBand`.
        Test whether adding a band adds it to the Spectrum.
        """

        s = self.system1.frequency.amount
        m = len(self.steel.loss_factor)

        self.assertTrue(s == m)

        self.system1.frequency.addBand(3)
        print(self.system1.objects())
        self.assertTrue(self.system1.frequency.amount == s + 1)
        self.assertTrue(len(self.steel.loss_factor) == m + 1)
        self.assertTrue(self.system1.frequency.amount == len(self.steel.loss_factor))

    def test_append_band(self):
        """
        Test of :meth:`seapy.system.Frequency.appendBand`.
        Test whether appending a band appends one to the Spectrum.
        """
        s = self.system1.frequency.amount
        m = len(self.steel.loss_factor)

        self.assertTrue(s == m)

        self.system1.frequency.appendBand()

        self.assertTrue(self.system1.frequency.amount == s + 1)
        self.assertTrue(len(self.steel.loss_factor) == m + 1)
        self.assertTrue(self.system1.frequency.amount == len(self.steel.loss_factor))

    def test_remove_band(self):
        """
        Test of :meth:`seapy.system.Frequency.removeBand`.
        Test whether removing a band removes it from the Spectrum.
        """
        s = self.system1.frequency.amount
        m = len(self.steel.loss_factor)

        self.assertTrue(s == m)

        self.system1.frequency.removeBand(3)

        self.assertTrue(self.system1.frequency.amount == s - 1)
        self.assertTrue(len(self.steel.loss_factor) == m - 1)
        self.assertTrue(self.system1.frequency.amount == len(self.steel.loss_factor))


if __name__ == "__main__":
    unittest.main()
