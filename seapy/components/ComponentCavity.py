
from Component import Component

class ComponentCavity(Component):
    """
    Abstract base class for fluid components.
    """
    
    def __init__(self):
        Component.__init__(self)
    
    
    availableSubsystems = ['Long']

    
    @property
    def pressure(self):
        """Pressure within the component :math:`p_{component}`. 
        
        :rtype: :class:`numpy.ndarray`
        
        This is the sum of all subsystems velocities.       
        """
        
        pressure = np.zeros(self.frequency.amount)
        for subsystem in self.linked_subsystems:
            pressure = pressure + subsystem.pressure
        return pressure      
    
    @property
    def pressure_level(self):
        """
        Sound pressure level :math:`L_p`.
        
        :rtype: :class:`numpy.ndarray`
        
        .. math:: L_p = 20 \\log_{10}{\\frac{p}{p_0}}
        """
        try:
            return 20.0 * np.log10(self.pressure / (2.0 * 10**(-5.0)) ) 
        except FloatingPointError:
            return np.zeros(self.frequency.amount)
    