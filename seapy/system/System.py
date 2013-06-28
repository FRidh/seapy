"""
The System class is the main class and contains methods for solving the SEA model.
"""

import math
import cmath
import numpy as np

import warnings
import logging
import weakref


from seapy.objects_map import objects_map

from seapy.system.Frequency import Frequency


class System(object):
    """
    The System class contains methods for solving the model.
    """
    
    SORT = 'System'
    
    @property
    def objects(self):
        """Return weak list of objects."""
        return [weakref.proxy(obj) for obj in self._objects]
    
    def _weaklist(self, sort):
        """Return weak list of objects of type sort."""
        return [weakref.proxy(obj) for obj in self._objects if obj.SORT==sort]
    
    @property
    def components(self):
        """Return weak list of components."""
        return self._weaklist('Component')
    
    @property
    def connections(self):
        """Return weak list of subsystems."""
        return self._weaklist('Connection')
    
    @property
    def materials(self):
        """Return weak list of subsystems."""
        return self._weaklist('Material')
    
    @property
    def subsystems(self):
        """Return weak list of subsystems."""
        return self._weaklist('Subsystem')
    
    @property
    def couplings(self):
        """Return weak list of subsystems."""
        return self._weaklist('Couplings')
    
    @property
    def excitations(self):
        """Return weak list of subsystems."""
        return self._weaklist('Excitation')
    
    
    def __init__(self):
        """Constructor.
        """
        self.frequency = Frequency()
        """
        Frequency object
        """
        
                
        self._objects = list()
        """Private list of objects this SEA model consists of."""
    
     
    solved = False
    """
    Switch indicating whether the system (modal energies) were solved or not.
    """
    
    #_octave_true = np.array([
        #0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 
        #0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0])
    #"""
    #Which frequency bands should be used when calculating in 1/1-octave bands.
    #"""
    #_third_true = np.array([
        #1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        #1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    """
    Which frequency bands should be used when calculating in 1/3-octave bands.
    """
    
    """
    Centerfrequencies of 1/3-octave bands.
     
    """

    #frequency = np.array([
        #25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 
        #400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 
        #4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000])
    """
    Frequency is an array of centerfrequencies.
    """
 
    
    #octaves = False
    #"""
    #Switch to indicate whether 1/1-octaves (True) are used or 1/3-octaves (False).
    #"""
    
    
    #def _set_enabled_bands(self, x):
        #if len(x) == self.frequency.amount:
            #if self.octaves:
                #self._enabled_bands = np.array(x * self._octave_true) 
            #else:
                #self._enabled_bands = np.array(x)
                
    
    #def _get_enabled_bands(self):
        #return self._enabled_bands

    #_enabled_bands = np.ones(frequency.amount)
    #enabled_bands = property(fget=_get_enabled_bands, fset=_set_enabled_bands)
    """"
    Specify with booleans which :attr:`frequency` are used. 
    Checks on assignment whether 1/1-octaves should be used or 1/3-octaves.
    """

    def getObject(self, name):
        """Get object by name."""
        for obj in self._objects:
            if name == obj.name:
                #print name + obj.name
                return weakref.proxy(obj) 
        return None
    
    def removeObject(self, name):
        """Delete object from SEA model."""
        for obj in self._objects:
            if name == obj.name:
                self._objects.remove(obj)
    
    def _addObject(self, name, model, **properties):
        """Add object to SEA model."""
        #if name not in self._objects:
        obj = model(name, weakref.proxy(self), **properties)   # Add hidden hard reference
        self._objects.append(obj)
        return self.getObject(obj.name)
        #else:
            #text = 'Object with name ' + name + ' already exists'
            #warnings.warn(text)
            #logging.warn(text)
           
        
    def addComponent(self, name, model, **properties):
        """Add component to SEA model."""
        obj = self._addObject(name, objects_map['component'][model] , **properties)
        obj._addSubsystems()
        return obj
       
    def addConnection(self, name, model, **properties):
        """Add connection to SEA model."""
        return self._addObject(name, objects_map['connection'][model], **properties)
    
    def addMaterial(self, name, model, **properties):
        """Add material to SEA model."""
        return self._addObject(name, objects_map['material'][model], **properties)

    def createMatrix(self, subsystems, f):
        """Create loss factor matrix for given frequency band.
        
        :param subsystems: is a list of subsystems. Reason to give the list as argument instead of using self.subsystems is that that list might change during execution.
        :type subsystems: list
        :param f: is the index of the center frequency of the frequency band
        :type f: int
        :rtype: :class:`numpy.ndarray`
        
        """
        logging.info('Creating matrix for centerfrequency %s', str(self.frequency.center[f]))
        
        LF = np.zeros((len(subsystems), len(subsystems)), dtype=float)
        j = 0
        for subsystem_j in subsystems: # Row j 
            i = 0
            for subsystem_i in subsystems:       # Column i
                loss_factor = 0.0
                if i==j:
                    #print 'i = j'
                    ## Total loss factor: sum of damping loss factor + loss factors for power transported from i elsewhere
                    loss_factor = subsystem_i.component.material.loss_factor[f] # Damping loss factor
                    for coupling in subsystem_i.linked_couplings_from: # + all CLFs 'from' i elsewhere
                        loss_factor = loss_factor + coupling.clf[f] 
                
                else:
                    ####Take the coupling loss factor from subsystem i to subsystem j. Negative
                    x = list(set(subsystem_i.linked_couplings_from).intersection(set(subsystem_j.linked_couplings_to)))

                    ##if not x:
                    ## Use the relation consistency relationship?
                    ##pass
                    ##print 'error. No coupling?'
                    if len(x)==1:
                        coupling = x[0]
                        #loss_factor = - coupling.clf[f]
                    del x        
                LF[j,i] = loss_factor * subsystem_i.modal_density[f]
                i+=1
            j+=1
        logging.info('Matrix created.')
        
        logging.info(LF)
        return LF

    def clearResults(self):
        """Clear the results. Reset modal energies. Set :attr:`solved` to False.
        
        :rtype: None
        """
        logging.info('Clearing results...')
        
        for subsystem in self.subsystems:
            del subsystem.modal_energy
    
        self.solved = False
    
        logging.info('Cleared results.')
     
    def solveSystem(self):  # Put the actual solving in a separate thread
        """Solve modal powers.
        
        :rtype: :func:`bool`
        
        This method solves the modal energies for every subsystem.
        The method :meth:`createMatrix` is called for every frequency band to construct a matrix of :term:`loss factors` and :term:`modal densities`.
        
        """
        logging.info('Solving system...')
        

        subsystems = self.subsystems
        print self.frequency
        for f in xrange(0, self.frequency.amount, 1): # For every frequency band
            if self.frequency.enabled[f]:               # If it is enabled
                LF = self.createMatrix(subsystems, f)   # Create a loss factor matrix.
                
                input_power = np.zeros(len(subsystems))     # Create input power vector
                #print input_power    
                i=0
                for subsystem in subsystems:
                    input_power[i] = subsystem.input_power[f] / self.frequency.angular[f]   # Retrieve the power for the right frequency
                    i=i+1
                
                try:
                    modal_energy = np.linalg.solve(LF, input_power)    # Left division results in the modal energies.
                except np.linalg.linalg.LinAlgError as e:   # If there is an error solving the matrix, then quit right away.
                    warnings.warn( repr(e) )
                    return False
                # Save each modal energy to its respective Subsystem nameect
                
                
                
                i = 0
                for subsystem in subsystems:
                    subsystem.modal_energy[f] = modal_energy[i]
                    i=i+1
                    
                del modal_energy, input_power, LF
                
        self.solved = True  
        logging.info('System solved.')
        return True
    