"""
Room 3D
-------

Classes describing a three-dimensional cavity.

.. autoclass:: seapy.components.acoustical3d.Component3DAcoustical

Subsystems
++++++++++

.. autoclass:: seapy.components.acoustical3d.SubsystemLong

"""
import numpy as np
from .acoustical import ComponentAcoustical
from ..subsystems import SubsystemAcoustical


class SubsystemLong(SubsystemAcoustical):
    """
    Subsystem for a fluid in a 3D cavity.
    """

    @property
    def average_frequency_spacing(self):
        """
        Average frequency spacing for a fluid in a 3D cavity.

        .. math:: \\overline{\\delta f}_0^{3D} = \\frac{c_0^^3}{4 \\pi V f^2}

        See Lyon, eq 8.3.7
        """
        # try:
        return self.soundspeed_phase ** 3.0 / (
            4.0 * np.pi * self.component.volume * self.frequency.center ** 2.0
        )

    def impedance_point_volume(self, excitation):
        """
        Specific acoustic impedance of a 3D cavity when there is a monopole (volume) source in the cavity.

        :param excitation: Excitation.
        :type excitation: :class:`seapy.excitations.ExcitationPoint`

        .. math:: Z_0^{U,3D} = \\frac{\\pi \\rho f^2}{c_0} \\left( 1 + \\frac{j}{k_0 r}   \\right)

        See Lyon, table 10.1, last row.

        .. note:: This is the specific acoustic impedance i.e. pressure over volume velocity, and not pressure of particle velocity.

        """
        return (
            np.pi
            * self.component.material.density
            * self.frequency.center ** 2.0
            / self.soundspeed_phase
            * (1.0 + 1.0j / (self.wavenumber * excitation.radius))
        )


class Component3DAcoustical(ComponentAcoustical):
    """
    Component for a fluid in a 3D cavity.
    """

    SUBSYSTEMS = {"subsystem_long": SubsystemLong}

    def mean_free_path(self):
        """Mean free path.

        .. math:: m = \\frac{4V}{S^{'}}

        with:

        * volume :math:`V`
        * total surface area :math:`S^{'}`

        """
        raise NotImplementedError
