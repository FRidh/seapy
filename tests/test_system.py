
import seapy
import numpy as np
from weakref import WeakSet

class TestSystem():
    """
    New system.
    """

    def test_new_system(self):
        """
        New System.
        """
        system1 = seapy.system.System()

    def test_frequencies(self):
        system1 = seapy.system.System()
        
        system1.frequency.center = [500.0, 1000.0, 2000.0, 4000.0, 8000.0]
        system1.frequency.lower = [355.0, 710.0, 1420.0, 2840.0, 5680.0] 
        system1.frequency.upper = [710.0, 1420.0, 2840.0, 5680.0, 11360.0] 
        system1.frequency.enabled = [False, False, True, True, True]
    
class TestNewObject():
    """Test adding a new object to the System.
    """

    def test_add_material(self):
        """
        Add material.
        """
        system1 = seapy.system.System()
        
        steel = system1.addMaterial('steel', 'MaterialSolid', young=1.0e7, poisson=0.30, loss_factor=np.ones(len(system1.frequency.center))*0.2)
        
        assert(len(list(system1.objects))==1)
        assert(len(list(system1.materials))==1)
        assert(len(list(steel.linked_components))==0)

    def test_add_component(self):
        """
        Add component.
        """
        
        system1 = seapy.system.System()
        steel = system1.addMaterial('steel', 'MaterialSolid', young=1.0e7, poisson=0.30, loss_factor=np.ones(len(system1.frequency.center))*0.2)
        beam1 = system1.addComponent('beam1', 'Component1DBeam', material='steel', volume=10.0, length=2.0, cross_section=0.30)
        
        assert(len(list(system1.objects))==5) # 1 material + 1 component + 3 subsystems = 5
        assert(len(list(system1.materials))==1)
        assert(len(list(system1.components))==1)
        assert(len(list(steel.linked_components))==1)

        #assert(steel.__dict__['linked_components'][0] == 'beam1')
        #assert(list(steel.linked_components)[0] == beam1)
        #assert(isinstance(list(steel.linked_components)[0], weakref.ProxyTypes))
        
        system1.removeObject('beam1')

    
    def test_add_junction(self):
        """
        Add junction.
        """
        system1 = seapy.system.System()
        junction1 = system1.addJunction('junction1', 'Junction', shape='Point')
        assert(len(list(system1.junctions))==1)

    def test_add_excitation(self):
        """
        Add junction.
        """
        system1 = seapy.system.System()
        
        steel = system1.addMaterial('steel', 'MaterialSolid', young=1.0e7, poisson=0.30, loss_factor=np.ones(len(system1.frequency.center))*0.2)
        beam1 = system1.addComponent('beam1', 'Component1DBeam', material='steel', volume=10.0, length=2.0, cross_section=0.30)
        
        subsystem1 = beam1.subsystem_long
        ex1 = subsystem1.addExcitation('ex1', 'ExcitationPointForce')
        assert(len(list(system1.excitations))==1)
