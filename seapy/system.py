"""
System
======

The System class is the main class and contains methods for solving the SEA model.

.. autoclass:: seapy.system.System

.. autoclass:: seapy.system.Frequency
.. autoclass:: seapy.system.Band

"""

import math
import cmath
import numpy as np

import warnings
import logging
from weakref import WeakSet
import weakref

from .base import Spectrum
from seapy.objects_map import objects_map

#from tabulate import tabulate
#from toolz import count
import pandas as pd
from .tools import plot, PathAnalysis


class System(object):
    """
    The System class contains methods for solving the model.
    """
    
    SORT = 'System'
    
    reference_pressure = 2.0e-5
    """Reference pressure :math:`p_{0}=2 \cdot 10^{-5}`.
    """
    
    reference_velocity = 5.0e-8
    """Reference velocity :math:`v_{0} = 5 \cdot 10^{-8}`.
    """
    
    reference_power = 1.0e-12
    """Reference power :math:`P_{0} = 1 \cdot 10^{-12}`.
    """
    
    reference_clf = 1.0e-12
    """Reference coupling loss factor :math:`\\eta_{0} = 1 \cdot 10^{-12}`.
    
    See Craik, equation 4.3, page 89.
    """
    
    reference_energy = 1.0e-12
    """Reference energy :math:`E_{0} = 1 \cdot 10^{-12}`
    """
    
    solved = False
    """
    Switch indicating whether the system (modal energies) were solved or not.
    """
    
    @property
    def objects(self):
        """All objects in the system.
        
        :returns: Generator of objects.
        :rtype: :class:`types.GeneratorType`
        """
        yield from (self.get_object(obj.name) for obj in self._objects)
        
    @property
    def components(self):
        """All components in the system.
        
        :returns: Generator of components.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Component')

    @property
    def subsystems(self):
        """All subsystems in the system.
        
        :returns: Generator of subsystems.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Subsystem')
    
    @property
    def junctions(self):
        """All junctions in the system.
        
        :returns: Generator of junctions.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Junction')
    
    @property
    def couplings(self):
        """All couplings in the system.
        
        :returns: Generator of couplings.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Coupling')
    
    @property
    def materials(self):
        """All materials in the system.
        
        :returns: Generator of materials.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Material')
    
    @property
    def excitations(self):
        """All excitations in the system.
        
        :returns: Generator of excitations.
        :rtype: :class:`python.types.GeneratorType`
        """
        yield from (obj for obj in self.objects if obj.SORT=='Excitation')

    #_frequency = None
    
    #@property
    #def frequency(self):

        #return self._frequency
        
    #@frequency.setter
    #def frequency(self, x):
        
        #try:
            #f = isinstance(f, Frequencies)
        #except AttributeError:
            #f = False
        
        #if isinstance(x, Frequency):
            #self._frequency = x
        #elif f:
            
    
    def __init__(self):
        """Constructor.
        """
        self.frequency = Frequency(weakref.proxy(self))
        """Frequency object.
        """    
            
        self._objects = list()
        """Private set of objects this SEA model consists of.
        """
        
        self.path_analysis = PathAnalysis(self)
        """Path analysis.
        
        .. seealso:: :class:`PathAnalysis`.
        
        """
        
    
    def __del__(self):
        
        for obj in self.objects:
            self.remove_object(obj.name)

    def _get_real_object(self, name):
        """
        Get real object by name.
        
        :param name: Name of `object`.
        
        :returns: Real `object`.
        """
        name = name if isinstance(name, str) else name.name
        for obj in self._objects:
            if name == obj.name:
                return obj
        else:
            raise ValueError("Unknown name. Cannot get object.")
        
    def get_object(self, name):
        """
        Get object by name.
        
        :param name: Name of `object`.
        
        :returns: Proxy to `object`.
        
        """
        name = name if isinstance(name, str) else name.name
        for obj in self._objects:
            if name == obj.name:
                return weakref.proxy(obj) 
        else:
            raise ValueError("Unknown name. Cannot get object.")
        
    
    def remove_object(self, name):
        """
        Delete object from SEA model.
        
        :param name: Name of `object`.
        
        :returns: Proxy to `object`.
        
        """
        obj = obj._get_real_object(name)
        for obj in self._objects:
            if name == obj.name:
                self._objects.remove(obj)
    
    def _add_object(self, name, model, **properties):
        """Add object to SEA model.
        
        :param name: Name of `object`.
        :param model: Model or type of `object`.
        :param properties: Other properties specific to `object`.
        
        """
        #if name not in self._objects:
        try:
            obj = model(name, weakref.proxy(self), **properties)   # Add hidden hard reference
        except KeyError:
            raise ValueError("Model does not exist. Cannot create object.")
        self._objects.append(obj)
        return self.get_object(obj.name)  
        
    def add_component(self, name, model, **properties):
        """Add component to SEA model.
        
        :param name: Name of component.
        :param model: Model or type of component. See :attr:`seapy.components.components_map`.
        :param properties: Other properties specific to the component.
        
        """
        obj = self._add_object(name, objects_map['component'][model] , **properties)
        obj._add_subsystems()
        return obj
       
    def add_junction(self, name, model, **properties):
        """Add junction to SEA model."""
        obj = self._add_object(name, objects_map['junction'][model], **properties)
        #obj._update_couplings()
        return obj
    
    def add_material(self, name, model, **properties):
        """Add material to SEA model."""
        obj = self._add_object(name, objects_map['material'][model], **properties)
        return obj
    
    def add_coupling(self, name, model, **properties):
        """Add material to SEA model."""
        obj = self._add_object(name, objects_map['coupling'][model], **properties)
        return obj
    
    def power_balance_matrix(self):
        """Power balance matrix as function of frequency.
        
        :param subsystems: is a list of subsystems. Reason to give the list as argument instead of using self.subsystems is that that list might change during execution.
        :type subsystems: list
        :param f: is the index of the center frequency of the frequency band
        :type f: int
        :rtype: :class:`numpy.ndarray`
        
        See Craik, equation 6.21, page 155.
        
        Yields power balance matrices.
        """
        #logging.info("Creating matrix for centerfrequency {}".format(self.frequency.center[f]))
        
        subsystems = [subsystem for subsystem in self.subsystems if subsystem.included is True]
        
        for f in range(self.frequency.amount):
            
            B = np.zeros((len(subsystems), len(subsystems)), dtype=float)
            for j, subsystem_j in enumerate(subsystems): # Row j 
                for i, subsystem_i in enumerate(subsystems):       # Column i
                    loss_factor = 0.0
                    if i==j:
                        loss_factor = + subsystem_i.tlf[f] # Total loss factor.
                    else:
                        
                        ####Take the coupling loss factor from subsystem i to subsystem j. Negative
                        x = list(set(subsystem_i.linked_couplings_from).intersection(set(subsystem_j.linked_couplings_to)))

                        ##if not x:
                        ## Use the relation consistency relationship?
                        ##pass
                        ##print 'error. No coupling?'
                        #print(len(x))
                        if len(x)==1:
                            #print("We have one!")
                            #print(len(x))
                            
                            loss_factor = - x[0].clf[f]
                            
                            #coupling = x[0]
                            ##loss_factor = - coupling.clf[f]
                        del x        
                    B[j,i] = loss_factor * subsystem_i.modal_density[f]
                    i+=1
                j+=1
            logging.info('Matrix created.')
            
            logging.info(B)
            yield B

    def power_vector(self):
        """Vector of input power normalized with angular frequency.
        
        See Craik, equation 6.21, page 155
        
        Yields power input vectors.
        """
        subsystems = [subsystem for subsystem in self.subsystems if subsystem.included is True]
        
        for f in range(self.frequency.amount):
            power_input = [subsystem.power_input[f] / self.frequency.angular[f] for subsystem in subsystems]
            yield np.array(power_input)
        

    def clearResults(self):
        """Clear the results. Reset modal energies. Set :attr:`solved` to False.
        
        :rtype: None
        """
        logging.info('Clearing results...')
        
        for subsystem in self.subsystems:
            del subsystem.modal_energy
    
        self.solved = False
    
        logging.info('Cleared results.')
     
    def solve_system(self):  # Put the actual solving in a separate thread?
        """Solve modal powers.
        
        :rtype: :func:`bool`
        
        This method solves the modal energies for every subsystem.
        
        .. seealso:: :meth:`power_vector` and :meth:`power_balance_matrix`
        
        """
        logging.info('Solving system...')
        
        self.clean()
        
        subsystems = [subsystem for subsystem in self.subsystems if subsystem.included is True]
        
        for f, (p, B) in enumerate(zip(self.power_vector(), self.power_balance_matrix())):
            
            if self.frequency.enabled[f]:
                #try:
                modal_energy = np.linalg.solve(B, p)    # Left division results in the modal energies.
                #except np.linalg.linalg.LinAlgError as e:   # If there is an error solving the matrix, then quit right away.
                    #warnings.warn( repr(e) )
                    #return False

                for i, subsystem in enumerate(subsystems):
                    subsystem.modal_energy[f] = modal_energy[i]                    
                #del modal_energy, power_input, LF
                
        self.solved = True  
        logging.info('System solved.')
        return True
    
    def clean(self):
        """Reset modal energy to zero in all subsystems.
        """
        
        for subsystem in self.subsystems:
            subsystem.modal_energy = np.zeros(self.frequency.amount)
    
    #def info(self, sort=None, fields=None):
        #"""Print information about objects of type sort. By default all types are returned."""

    def plot(self, objects, quantity, yscale='linear'):
        items = (getattr(obj, quantity) for obj in (self.get_object(o) for o in objects))
        return plot(self.frequency.center, items, quantity, self.frequency.enabled, yscale=yscale)
        
    def info(self, objects, attribute, tablefmt='simple'):
        """Print single attribute of objects.
        """
        objects = (self.get_object(obj) for obj in objects)
        
        data = {obj.name: getattr(obj, attribute) for obj in objects if hasattr(obj, attribute)}
        df = pd.DataFrame(data, index=self.frequency.center.astype('int')).T
        return df


    #def info_objects(self):
        #"""Print information about objects.
        #"""
        #header = ['Name', 'Included', 'Enabled', 'Class', 'Sort']
        #data = ((obj.name, obj.included, obj.enabled, obj.__class__.__name__, obj.SORT) for obj in self.objects)
        #return tabulate(data, headers=header, tablefmt=tablefmt)
        
    #def info_materials(self):
        #"""Print information about materials.
        #"""
        #header = ['Name', 'Included', 'Enabled', 'Class', 'Density', 'Components']
        #data = ((obj.name, obj.included, obj.enabled, obj.__class__.__name__, obj.density, count(obj.linked_components)) for obj in self.materials)
        #return tabulate(data, headers=header, tablefmt=tablefmt)
        
    #def components_info(self, tablefmt='simple'):
        #"""Print information about components.
        #"""
        #header = ['Name', 'Included', 'Enabled', 'Class', 'Material', 'Volume', 'Mass', 'Subsystems', 'Junctions']
        #data = ((obj.name, obj.included, obj.enabled, obj.__class__.__name__, obj.material.name, obj.volume, obj.mass, count(obj.linked_subsystems), count(obj.linked_junctions)) for obj in self.components)
        #return tabulate(data, headers=header, tablefmt=tablefmt)

    #def subsystems_info(self, tablefmt='simple'):
        #"""Print information about subsystems.
        #"""
        #header = ['Name', 'Included', 'Enabled', 'Class', 'Component', 'Couplings - From', 'Couplings - To', 'Excitations']
        #data = ((obj.name, obj.included, obj.enabled, obj.__class__.__name__, obj.component.name, count(obj.linked_couplings_from), count(obj.linked_couplings_to), count(obj.linked_excitations)) for obj in self.subsystems)
        #return tabulate(data, headers=header, tablefmt=tablefmt)

    #def excitations_info(self, tablefmt='simple'):
        #"""Print information about excitations.
        #"""
        #header = ['Name', 'Included', 'Enabled', 'Class', 'Subsystem']
        #data = ((obj.name, obj.included, obj.enabled, obj.__class__.__name__, obj.subsystem.name) for obj in self.excitations)
        #return tabulate(data, headers=header, tablefmt=tablefmt)

    #def junctions_info(self, tablefmt='simple'):
        #"""Print information about junctions.
        #"""
        #header = ['Name', 'Included', 'Enabled', 'Class', 'Shape', 'Components', 'Couplings', 'Subsystems']
        #data = ((obj.name, obj.included, obj.enabled, obj.__class__.__name__, obj.shape, count(obj.components), count(obj.linked_couplings), count(obj.subsystems)) for obj in self.junctions)
        #return tabulate(data, headers=header, tablefmt=tablefmt)
    
    #def couplings_info(self, tablefmt='simple'):
        #"""Print information about junctions.
        #"""
        #header = ['Name', 'included', 'Enabled', 'Class', 'Shape', 'Components', 'Couplings', 'Subsystems']
        #data = ((obj.name, obj.included, obj.impedance, obj.__class__.__name__, obj.shape, count(obj.components), count(obj.linked_couplings), count(obj.subsystems)) for obj in self.excitations)
        #return tabulate(data, headers=header, tablefmt=tablefmt)
    
    
    
class Band(object):
    """Frequency band class."""
    
    def __init__(self, lower=0.0, center=0.0,  upper=0.0, enabled=False):
        
        self.lower = lower
        self.center = center
        self.upper = upper
        self.enabled = enabled
    
    @property
    def bandwidth(self):
        return self.upper - self.lower
    
    @property
    def angular(self):
        return 2.0 * np.pi * self.center
   
   
   
   
#class SpectrumDescriptorFrequency(object):
    #"""
    #"""
    
    #def __get__(self):
        #pass
    
    #def __set__(self):
        #pass
   
class Frequency(object):
    """New-style spectrum class."""
    
    def __init__(self, system):
        self._system = system
        self._bands = list()
    
    
    #@classmethod
    #def from_frequencies(cls, system, f):
        #"""Create object from :class:`acoustics.signal.Frequencies`.""" 
        #obj = cls(system)
        #obj.center = f.center
        #obj.lower = f.lower
        #obj.upper = f.upper
        
        #return obj
    
    def _spectrum(name):
        """Property to access the frequency bands as/using arrays."""

        @property
        def prop(self):
            return np.array([getattr(band, name) for band in self._bands])
        
        @prop.setter
        def prop(self, x):
            if len(x) == len(self._bands):
                """
                When the given array has the same amount of items as there are 
                frequency bands, we will fit them one on one.
                """
                for new, band in zip(x, self._bands):
                    setattr(band, name, new)
            else:
                """
                If not, we will delete the old frequency bands, and create new ones."""
                self._bands = list()
                for i in x:
                    band = Band()
                    setattr(band, name, i)
                    self._bands.append(band) # Use self.addBand() instead!!
        return prop
    
    lower = _spectrum('lower')
    center = _spectrum('center')
    upper = _spectrum('upper')
    enabled = _spectrum('enabled')
    
    @property
    def bandwidth(self):
        return np.array([band.bandwidth for band in self._bands])
        
    @property
    def angular(self):
        return np.array([band.angular for band in self._bands])
    
    @property
    def amount(self):
        return len(self._bands)
    
    @property
    def spectra(self):
        """Generator to obtain all spectra in use in the SEA model."""
        for obj in self._system.objects:
            for cls in obj.__class__.__mro__:
                for key, value in cls.__dict__.items():
                    if isinstance(value, Spectrum):
                        yield (obj, key)
    
    def appendBand(self, **kwargs):
        """
        Append frequency band.
        """
        self.addBand(len(self._bands), **kwargs)
    
    def addBand(self, pos, **kwargs):
        """
        Add frequency band.
        
        
        Inform all spectra of the change!!
        """
        
        self._bands.insert(pos, Band(**kwargs))  # Create a new frequency band
        
        default = 0.0 # default value of array cells
        
        for obj, attr in self.spectra():    # Add a band to all spectra
            setattr(obj, attr, np.insert(getattr(obj, attr), pos, default))
            
    
    def removeBand(self, pos):
        """
        Remove frequency band.
        
        Inform all spectra of the change!!
        """
        self._bands.pop(pos) # Remove the frequency band
        
        for obj, attr in self.iterspectra():     # Remove a band from all spectra
            setattr(obj, attr, np.delete(getattr(obj, attr), pos))
            
            
        
    #@property
    #def upper(self):
        #return np.array([band.upper for band in self._bands])
    
    #@property
    #def lower(self):
        #return np.array([band.lower for band in self._bands])
    
    #@property
    #def center(self):
        #return np.array([band.center for band in self._bands])
    
    #@center.setter
    #def center(self, x):
        #if len(x) == len(self.bands):
            #for new, band in zip(x, self.bands):
                #band.center = new
        ##else:
            #"""Add the required amount of bands."""

    #@property
    #def enabled(self):
        #return np.array([band.enabled for band in self._bands])
    

    
#class Frequency(object):
    #"""
    #Abstract base class for handling different frequency settings.
    #"""
    
    #def __init__(self, system):
        #self._system = system
    
    #def _set_band(self, x, sort):
        #for i in ['_lower', '_center', '_upper']:
            #if len(getattr(self, i)) != len(x):
                #setattr(self, i, np.zeros(len(x)))
        #if len(getattr(self, '_enabled')) != len(x):        
                #setattr(self, '_enabled', np.zeros(len(x), dtype=bool))
        #setattr(self, sort, np.array(x))
    

    
    #def _get_center(self):
        #return self._center
    
    #def _set_center(self, x):
        #self._set_band(x, '_center')
    
    #_center = np.array([0.0])
    #center = property(fget=_get_center, fset=_set_center)
    #"""
    #Center frequencies of frequency bands.
    #"""
    
    
    #def _get_upper(self):
        #return self._upper
    
    #def _set_upper(self, x):
        #self._set_band(x, '_upper')
    
    #_upper = np.array([0.0])
    #upper = property(fget=_get_upper, fset=_set_upper)
    #"""
    #Upper limit frequencies of frequency bands.
    #"""
    
    #def _set_lower(self, x):
        #self._set_band(x, '_lower')
    
    #def _get_lower(self):
        #return self._lower
    
    #_lower = np.array([0.0])
    #lower = property(fget=_get_lower, fset=_set_lower)
    #"""
    #Lower limit frequencies of frequency bands.
    #"""
    
    #def _set_enabled(self, x):
        #self._set_band(x, '_enabled')
    
    #def _get_enabled(self):
        #return self._enabled
    
    #_enabled = np.array([False]) 
    #enabled = property(fget=_get_upper, fset=_set_upper)
    #"""
    #Enabled frequency bands.
    
    #Modal powers will not be solved for disabled frequency bands.
    #"""
    
    #@property
    #def bandwidth(self):
        #"""Bandwidth of frequency bands,
        
        #:rtype: :class:`numpy.ndarray`
        #"""
        #return self.upper - self.lower

    #@property
    #def angular(self):
        #"""Angular frequency
        
        #:rtype: :class:`numpy.ndarray`
        #"""
        #return self.center * 2.0 * np.pi 
    
    
    
    #@property
    #def amount(self):
        #"""Amount of frequency bands
        
        #:rtype: :func:`int`
        #"""
        #try:
            #return len(self.center)
        #except TypeError:
            #return 0
