
import numpy as np


#class Band(object):
    #"""Frequency band class."""
    
    #lower = 0.0
    #center = 0.0
    #upper = 0.0
    #enabled = False
    
    #@property
    #def bandwidth(self):
        #return self.upper - self.lower
    
    #@property
    #def angular(self):
        #return 2.0 * np.pi * self.center
    
#class NewFrequency(object):
    #"""New-style spectrum class."""
    
    #def __init__(self):
        #self.bands = list()
    
    #@property
    #def upper(self):
        #return np.array([band.upper for band in self._bands])
    
    #@property
    #def lower(self):
        #return np.array([band.lower for band in self._bands])
    
    #@property
    #def center(self):
        #return np.array([band.center for band in self._bands])
    
    #@property
    #def enabled(self):
        #return np.array([band.enabled for band in self._bands])
    
    #@property
    #def bandwidth(self):
        #return np.array([band.bandwidth for band in self._bands])
    
    #@property
    #def amount(self):
        #return len(self._bands)
    
class Frequency(object):
    """
    Abstract base class for handling different frequency settings.
    """
    
    
    def _set_band(self, x, sort):
        for i in ['_lower', '_center', '_upper']:
            if len(getattr(self, i)) != len(x):
                setattr(self, i, np.zeros(len(x)))
        if len(getattr(self, '_enabled')) != len(x):        
                setattr(self, '_enabled', np.zeros(len(x), dtype=bool))
        setattr(self, sort, x)
    

    
    def _get_center(self):
        return self._center
    
    def _set_center(self, x):
        self._set_band(x, '_center')
    
    _center = np.array([0.0])
    center = property(fget=_get_center, fset=_set_center)
    """
    Center frequencies of frequency bands.
    """
    
    def _get_upper(self):
        return self._upper
    
    def _set_upper(self, x):
        self._set_band(x, '_upper')
    
    _upper = np.array([0.0])
    upper = property(fget=_get_upper, fset=_set_upper)
    """
    Upper limit frequencies of frequency bands.
    """
    
    def _set_lower(self, x):
        self._set_band(x, '_lower')
    
    def _get_lower(self):
        return self._lower
    
    _lower = np.array([0.0])
    lower = property(fget=_get_lower, fset=_set_lower)
    """
    Lower limit frequencies of frequency bands.
    """
    
    def _set_enabled(self, x):
        self._set_band(x, '_enabled')
    
    def _get_enabled(self):
        return self._enabled
    
    _enabled = np.array([False]) 
    enabled = property(fget=_get_upper, fset=_set_upper)
    """
    Enabled frequency bands.
    
    Modal powers will not be solved for disabled frequency bands.
    """
    
    @property
    def bandwidth(self):
        """Bandwidth of frequency bands,
        
        :rtype: :class:`numpy.ndarray`
        """
        return self.upper - self.lower

    @property
    def angular(self):
        """Angular frequency
        
        :rtype: :class:`numpy.ndarray`
        """
        return self.center * 2.0 * np.pi 
        
    @property
    def amount(self):
        """Amount of frequency bands
        
        :rtype: :func:`int`
        """
        try:
            return len(self.center)
        except TypeError:
            return 0