import numpy as np
from .coupling import Coupling

from .couplingsurfaceplateacoustical import (
    radiation_efficiency,
    critical_frequency,
)  # CouplingSurfacePlateAcoustical


class CouplingSurfaceAcousticalPlate(Coupling):
    """
    A model describing the coupling between a cavity and a plate.
    """

    @property
    def impedance_from(self):
        return self.subsystem_from.impedance

    @property
    def impedance_to(self):
        return self.subsystem_to.impedance

    @property
    def critical_frequency(self):
        """
        Critical frequency
        """
        return critical_frequency(self.subsystem_to, self.subsystem_from)

    @property
    def critical_wavelength(self):
        """
        Wavelength belonging to critical frequency.
        
        .. math:: \\lambda_c = c_{g} / f_c
        
        """
        try:
            return self.subsystem_from.soundspeed_group / self.critical_frequency
        except FloatingPointError:
            return np.zeros(len(self.frequency))

    @property
    def radiation_efficiency(self):
        """
        Radiation efficiency.
        """
        return radiation_efficiency(self, self.subsystem_to.component)

    # @property
    # def clf(self):
    # """
    # Coupling loss factor for transmission from a cavity to a plate.

    # .. math:: \\eta_{cavity,plate} = \\frac{\\rho_0 c^2 S \\sigma f_c }{8 \\pi f^3 m^{''} V_2}

    # See BAC, equation 3.9

    # .. warning:: This one uses the consistency relation!

    # """
    # try:
    # return self.subsystem_from.component.material.density * \
    # self.subsystem_from.soundspeed_group**2.0 *self.area * self.radiation_efficiency * \
    # self.critical_frequency / (8.0 * np.pi * self.frequency.center**3.0 * \
    # self.subsystem_to.component.mass_per_area * self.subsystem_from.component.volume)
    # except (ZeroDivisionError, FloatingPointError):
    # return np.zeros(len(self.frequency))

    @property
    def area(self):
        """
        Connecting surface.
        """
        return self.subsystem_to.component.area

    @property
    def clf(self):
        """
        Coupling loss factor for transmisson from a cavity/room to a plate/wall.
        
        .. math:: \\eta_{cavity,plate} = \\frac{5556 S_2 f_{c2} \\sigma_{2}}{V_1 \\rho{s2} f^3}
        
        See Craik, equation 1.22, page 9.
        
        """
        return (
            5556.0
            * self.area
            * self.critical_frequency
            * self.radiation_efficiency
            / (
                self.subsystem_from.component.volume
                * self.subsystem_to.component.material.density
                * self.frequency.center ** 3.0
            )
        )
