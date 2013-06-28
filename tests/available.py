import seapy
import unittest

class TestAvailabilityObjects(unittest.TestCase):
    
    
    def setUp(self):
        """Code run before each unit test."""
        self.system1 = seapy.system.System()
        self.material = self.system1.addMaterial('steel', 'MaterialSolid')
        self.beam1 = self.system1.addComponent('beam1', 'Component1DBeam', material=self.material)
        self.beam2 = self.system1.addComponent('beam2', 'Component1DBeam', material=self.material)
        self.junction = self.system1.addjunction('junction1', 'Junction', shape='Point')
        self.junction.addComponent(self.beam1, 'corner')
        self.junction.addComponent(self.beam2, 'corner')
        
    
    def tearDown(self):
        """Code run after each test."""
        self.system1 = None
        self.material = None
        self.beam1 = None
        self.beam2 = None
        self.junction = None
        
    
    def test_disabling_material(self):
        """Test disabling material."""
        self.material.disable() # Cause
        
        self.assertFalse(self.material.enabled)
        
        self.assertFalse(self.material.included)
        self.assertFalse(self.beam1.included)
        self.assertFalse(self.beam2.included)
        self.assertFalse(self.junction.included)
    
    def test_disabling_subsystem(self):
        """Testing disabling a subsystem."""
        sub = self.beam1.linked_subsystems[0]
        
        sub.disable() # Cause
        
        self.assertFalse(sub.enabled)
        self.assertFalse(sub.included)
        self.assertFalse(sub.linked_couplings_from(included=True))
        self.assertFalse(sub.linked_couplings_from(included=False))
        
    
if __name__ == '__main__':
    unittest.main()
