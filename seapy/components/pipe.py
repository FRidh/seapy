"""
Pipe
----

.. autoclass:: seapy.components.pipe.Component1DPipe

Subsystems
++++++++++

.. autoclass:: seapy.components.pipe.SubsystemLong
.. autoclass:: seapy.components.pipe.SubsystemBend
.. autoclass:: seapy.components.pipe.SubsystemShear


Classes describing a one-dimensional beam.
"""
import numpy as np
from ..base import Attribute
from .structural import ComponentStructural
from ..subsystems import SubsystemStructural

from .beam import SubsystemLong

"""The longitudinal waves can be modelled as if we have a beam.

Page 142, Lyon.
"""

from .plate import SubsystemShear

"""The torsional waves can be modelled as if we have shear waves in a plate.

Page 142, Lyon.
"""


class SubsystemBend(SubsystemStructural):
    """Flexural radial modes.

    Page 142, Lyon.
    """

    @property
    def frequency_ring(self):
        """Ring frequency.

        .. math:: \\f_r = \\frac{c_L}{2 \pi r}

        Page 143, Lyon.
        """
        return (
            self.component.subsystem_long.soundspeed_group
            * self.component.circumference
        )

    @property
    def average_frequency_spacing(self):
        """Average frequency spacing.

        Page 143, equation 8.2.16 in Lyon.
        """
        mode_count = lambda frequency: self.compute_mode_count(
            self.component.length,
            self.component.radius_of_gyration,
            self.frequency_ring,
            frequency,
        )
        mode_count_upper = mode_count(self.frequency.upper)
        mode_count_lower = mode_count(self.frequency.lower)
        return self.frequency.bandwidth / (mode_count_upper - mode_count_lower)

    @staticmethod
    def compute_mode_count(length, radius_of_gyration, frequency_ring, frequency):
        """Compute the mode count up until a certain frequency.

        Page 143, equation 8.2.16 in Lyon.
        """
        return (
            length
            / (2.0 * np.pi)
            * frequency
            / frequency_ring
            * (
                1.0
                + (
                    np.pi
                    / 2.0
                    / (
                        np.sqrt(frequency / frequency_ring)
                        + 0.5 * (frequency / frequency_ring) ** 3.5
                    )
                )
                ** 4.0
            )
            ** 0.25
        )


class ComponentPipe(ComponentStructural):
    """Pipe component."""

    SUBSYSTEMS = {
        "subsystem_long": SubsystemLong,
        "subsystem_bend": SubsystemBend,
        "subsystem_shear": SubsystemShear,
    }

    length = Attribute()
    """Length of the pipe."""

    radius = Attribute()
    """Radius of the pipe."""

    thickness = Attribute()
    """Wall thickness."""

    @property
    def area(self):
        """Area of the open cylinder.

        .. math:: A = 2 \\pi r l
        """
        return 2.0 * np.pi * self.radius * self.length

    @property
    def circumference(self):
        """Circumference of pipe.

        .. math:: c = 2 \\pi r
        """
        return 2.0 * np.pi * self.radius

    @property
    def radius_of_gyration(self):
        """
        Radius of gyration :math:`\\kappa` is given by dividing the thickness of the beam by :math:`\\sqrt{2}`.

        .. math:: \\kappa = \\frac{h}{\\sqrt{12}}

        Page 143, Lyon.
        """
        return self.thickness / np.sqrt(12)


__all__ = ["ComponentPipe", "SubsystemLong", "SubsystemBend", "SubsystemShear"]
