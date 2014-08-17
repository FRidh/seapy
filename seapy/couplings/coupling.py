"""
Coupling
--------

.. autoclass:: Coupling

"""


import abc
import math
import cmath
import numpy as np

from ..base import Base, JunctionLink, SubsystemFromLink, SubsystemToLink

class Coupling(Base):
    """
    Abstract base class for couplings.
    """
    
    SORT = 'Coupling'

    _DEPENDENCIES = ['subsystem_from', 'subsystem_to']

    junction = JunctionLink()
    """
    Junction this coupling is part of.
    """
    
    subsystem_from = SubsystemFromLink()
    """
    Type of subsystem origin for coupling
    """
    
    subsystem_to = SubsystemToLink()
    """
    Type of subsystem destination for coupling
    """
    
    #size = None
    #"""
    #Size of the coupling.
    #"""
    
    #def __init__(self, name, junction, subsystem_from, subsystem_to, **properties):
    def __init__(self, name, system, **properties):
        """
        Constructor.
        
        :param name: Identifier
        :type name: string
        :param junction: junction
        :type junction: :class:`seapy.junctions.junction`
        :param subsystem_from: subsystem from
        :type subsystem_from: :class:`seapy.subsystems.Subsystem`
        :param subsystem_to: subsystem_to
        :type subsystem_to: :class:`seapy.subsystems.Subsystem`
        
        """
        super().__init__(name, system, **properties)
        #self.junction = junction
        #self.subsystem_from = subsystem_from
        #self.subsystem_to = subsystem_to
    
    
    def _save(self):
        attrs = super()._save()
        attrs['subsystem_from'] = self.subsystem_from.name
        attrs['subsystem_to'] = self.subsystem_to.name
        attrs['junction'] = self.junction.name
        return attrs

    def disable(self, subsystems=False):
        """
        Disable this coupling. Optionally disable dependent subsystems as well.
        
        :param subsystems: Disable subsystems
        :type subsystems: bool
        """
        self.__dict__['enabled'] = False
        
        if subsystems:
            self.subsystem_from.disable()
            self.subsystem_to.disable()
    
    def enable(self, subsystems=False):
        """
        Enable this coupling. Optionally enable dependent subsystems as well.
        
        :param subsystems: Enable subsystems
        :type subsystems: bool
        """
        self.__dict__['enabled'] = True
        
        if subsystems:
            self.subsystem_from.enable()
            self.subsystem_to.enable()


    @property
    @abc.abstractmethod
    def impedance_from(self):
        """Impedance of :attr:`subsystem_from` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
    
    @property
    @abc.abstractmethod
    def impedance_to(self):
        """Impedance of :attr:`subsystem_to` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
    
    
    @property
    def reciproce(self):
        """Reciproce or inverse coupling.
        
        :returns: Reciproce coupling if it exists, else None.
        
        """
        for coupling in self.junction.linked_couplings:
            if coupling.subsystem_from == self.subsystem_to and coupling.subsystem_to == self.subsystem_from:
                return coupling
    
    @property
    def conductivity(self):
        """Conductivity of coupling.
        
        .. math:: \\omega n_i \\eta_{i,j}
        
        with:
        
        * angular frequency :math:`\\omega`
        * modal density of subsystem ``i`` :math:`n_i`
        * coupling loss factor of this coupling :math:`\\eta_{i,j}`
        
        """
        return self.frequency.angular * self.subsystem_from.modal_density * self.clf
    
    @property
    def clf(self):
        """Coupling loss factor `\\eta`.
        
        :rtype: :class:`numpy.ndarray`
        
        In case the CLF is not specified for the given coupling it is calculated using the SEA consistency relation.
        
        \\eta_{12} = \\eta_{21} \\frac{n_2}{n_1}
        
        """
        try:
            clf = self.reciproce.__class__.clf
        except AttributeError:
            raise ValueError("Cannot calculate CLF. Reciproce CLF has not been specified.")
        else:
            return clf * self.subsystem_to.modal_density / self.subsystem_from.modal_density
        
    @property
    def clf_level(self):
        """Coupling loss factor level.
        
        .. math:: \\L_{\\eta} = 10 \\log_{10}{\\left( \\frac{\\eta}{\\eta_0} \\right)}
        
        See Craik, equation 4.3, page 89.
        
        """
        return 10.0*np.log10(self.clf / self.system.ref)
    
        
    @property
    def mobility_from(self):
        """Mobility of :attr:`subsystem_from` corrected for the type of coupling.
        
        :returns: Mobility :math:`Y`
        :rtype: :class:`numpy.ndarray`
        """
        return 1.0 / self.impedance_from
        
    @property
    def mobility_to(self):
        """Mobility of :attr:`subsystem_to` corrected for the type of coupling.
        
        :returns: Mobility :math:`Y`
        :rtype: :class:`numpy.ndarray`
        """
        return 1.0 / self.impedance_to
    
    @property
    def resistance_from(self):
        """Resistance of :attr:`subsystem_from` corrected for the type of coupling.
        
        :returns: Impedance :math:`Z`
        :rtype: :class:`numpy.ndarray`
        """
        return np.real(self.impedance_from)
    
    @property
    def resistance_to(self):
        """Resistance of :attr:`subsystem_to` corrected for the type of coupling.
        
        :returns: Impedance :math:`Z`
        :rtype: :class:`numpy.ndarray`
        """
        return np.real(self.impedance_to)
    
    @property
    def power(self):
        """Amount of power flowing from subsystem 1 to subsystem 2.
        
        .. math:: P = E_{1} \\omega \\eta_{12}
        
        See Craik, equation 4.1, page 88.
    
        .. seealso:: :meth:`power_net`
    
        """
        return self.subsystem_from.energy * self.frequency.angular * self.clf
    
    @property
    def power_net(self):
        """Net amount of power from subsystem 1 to subsystem 2.
        
        .. math:: \\overline{P}_{12} = - \\overline{P}_{21} = E_1 \\omega \\eta_{12} - E_2 \\omega \\eta_{21}
        
        See Craik, equation 4.2, page 89.
        
        """
        return self.frequency.angular * (self.subsystem_from.energy * self.clf - self.subsystem_to.energy - self.reciproce.clf)
        
        
    
    
    @property
    def modal_coupling_factor(self):
        """Modal coupling factor of the coupling.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: \\beta_{ij} = \\frac{ f * \\eta_{ij} } { \\overline{\\delta f_i} }
        
        See Lyon, above equation 12.1.4
        """
        return self.frequency.center * self.clf / self.subsystem_from.average_frequency_spacing
        
