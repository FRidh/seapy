from ..base import Base, SubsystemExcitationLink

import abc
import math
import cmath
import numpy as np


class Excitation(Base):
    """Abstract Base Class for excitations."""

    SORT = "Excitation"

    _DEPENDENCIES = ["subsystem"]

    subsystem = SubsystemExcitationLink()
    """
    Subsystem that is being excited by this excitation
    """

    def __init__(self, name, system, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param system: Component
        :type system: :class:`seapy.system.System`
        
        """
        super().__init__(name, system, **properties)

        # self.subsystem = subsystem

    def _save(self):
        attrs = super()._save()
        attrs["subsystem"] = self.subsystem.name
        return attrs

    def disable(self, subsystem=False):
        """
        Disable this excitation. Optionally disable excitations' subsystem.
        
        :param subsystem: Disable subsystem
        :type subsystem: bool
        """
        self.__dict__["enabled"] = False

        if subsystem:
            self.subsystem.disable()

    def enable(self, subsystem=False):
        """
        Enable this excitation. Optionally enable excitations' subsystem.
        
        :param subsystem: Enable subsystem
        :type subsystem: bool
        """
        self.__dict__["enabled"] = True

        if subsystem:
            self.subsystem.enable()

    @property
    @abc.abstractmethod
    def impedance(self):
        """Impedance :math:`Z`.
        """
        pass

    @property
    def resistance(self):
        """The resistance :math:`R` is the real part of the impedance :math:`Z`.
        """
        return self.impedance.real

    @property
    def reactance(self):
        """The reactance :math:`X` is the imaginary part of the impedance :math:`Z`.
        """
        return self.impedance.imag

    @property
    def conductance(self):
        """The conductance :math:`G` is the real part of the mobility :math:`Y`.
        
        .. math:: G = \\mathrm{Re)\\left( Y \\right)
        
        """
        return self.mobility.real

    @property
    def susceptance(self):
        """The susceptance :math:`B` is the imaginary part of the mobility :math:`Y`.
        
        .. math:: B = \\mathrm{Im)\\left( Y \\right)
        
        """
        return self.mobility.imag

    @property
    @abc.abstractmethod
    def power(self):
        """Input power.
        """

    @property
    def power_level(self):
        """Input power level.
        
        .. math:: L_{P} = 10 \\log_{10}{\\left( \\frac{P}{P_0} \\right)}
        
        """
        return 10.0 * np.log10(self.power / self.system.reference_power)
