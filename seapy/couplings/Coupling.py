
import abc
import math
import cmath
import numpy as np

from ..base import Base

class Coupling(Base):
    """
    Abstract base class for couplings.
    """
    __metaclass__ = abc.ABCMeta
    
    
    SORT = 'Coupling'
    
    def _get_connection(self):
        return self._connection
    
    def _set_connection(self, x):
        self._set_link('connection', 'linked_couplings', x)
        
    _connection = None
    connection = property(fget=_get_connection, fset=_set_connection)
    """
    Connection this coupling is part of.
    """
    
    
    def __init__(self, name, connection, **properties):
        """Constructor.
        
        :param name: Identifier
        :type name: string
        :param connection: Connection
        :type connection: :class:`SeaPy.connections.Connection`
        
        """
        Base.__init__(self, name, connection.system, **properties)
        
        self.connection = connection
    
    
    
    def _get_subsystem_from(self):
        return self._subsystem_from
    
    def _set_subsystem_from(self, x):
        self._set_link('subsystem_from', 'linked_couplings_from', x)
    
    _subsystem_from = None
    subsystem_from = property(fget=_get_subsystem_from, fset=_set_subsystem_from)
    """
    Type of subsystem origin for coupling
    """
    
    def _get_subsystem_to(self):
        return self._subsystem_to
    
    def _set_subsystem_to(self, x):
        self._set_link('subsystem_to', 'linked_couplings_to', x)
    
    
    _subsystem_to = None
    subsystem_to = property(fget=_get_subsystem_to, fset=_set_subsystem_to)
    """
    Type of subsystem destination for coupling
    """
    
    
    
    
    size = None
    """
    Size of the coupling.
    """
    
    @abc.abstractproperty
    def impedance_from(self):
        """Impedance of :attr:`subsystem_from` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
    
    @abc.abstractproperty
    def impedance_to(self):
        """Impedance of :attr:`subsystem_to` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
     
    @abc.abstractproperty
    def clf(self):
        """Coupling loss factor `\\eta`.
        
        :rtype: :class:`numpy.ndarray`
        """
        return
        
    @property
    def mobility_from(self):
        """Mobility of :attr:`subsystem_from` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return 1.0 / self.impedance_from
        
    @property
    def mobility_to(self):
        """Mobility of :attr:`subsystem_to` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return 1.0 / self.impedance_to
    
    @property
    def resistance_from(self):
        """Resistance of :attr:`subsystem_from` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return np.real(self.impedance_from)
    
    @property
    def resistance_to(self):
        """Resistance of :attr:`subsystem_to` corrected for the type of coupling.
        
        :rtype: :class:`numpy.ndarray`
        """
        return np.real(self.impedance_to)
    
    
    @property
    def modal_coupling_factor(self):
        """Modal coupling factor of the coupling.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: \\beta_{ij} = \\frac{ f * \\eta_{ij} } { \\overline{\\delta f_i} }
        
        See Lyon, above equation 12.1.4
        """
        return self.frequency.center * self.clf / self.subsystem_from.average_frequency_spacing
        
