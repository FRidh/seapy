#! /usr/bin/env python3

import sys

import seapy
import numpy as np

def main():
    
    """First an SEA model has to be created."""
    system1 = seapy.system.System()
    
    """We're only interested in a limited frequency range."""
    system1.frequency.center = [500.0, 1000.0, 2000.0, 4000.0, 8000.0]
    system1.frequency.lower = [355.0, 710.0, 1420.0, 2840.0, 5680.0] 
    system1.frequency.upper = [710.0, 1420.0, 2840.0, 5680.0, 11360.0] 
    system1.frequency.enabled = [False, False, True, True, True]
    
    """An important parameter of a component is the type of which it is made. Let's create steel beams."""
    steel = system1.addMaterial('steel', 'MaterialSolid', young=1.0e7, poisson=0.30, loss_factor=np.ones(len(system1.frequency.center))*0.2)
    
    """Oh, we shouldn't forget to set the density"""
    steel.density = 2000.0
    
    #print (steel.__class__.__dict__)
    
    """We now create two almost similar beams."""
    beam1 = system1.addComponent('beam1', 'Component1DBeam', material='steel', volume=10.0, length=2.0, cross_section=0.30)
    #beam2 = system1.addComponent('beam2', 'Component1DBeam', material='steel', volume=40.0, length=2.0, cross_section=0.30)
    
    ##beam1.linked_subsystems = 3
    #print( beam1.__dict__['linked_subsystems'])
    #for item in beam1.linked_subsystems:
        #print (item)
    
    #for item in steel.linked_components:
        #print (item)
    #print (steel)
    
    #system1.removeObject('steel')
    #print (system1.objects)
    #print('testesddsfssdf')
    #print(item.name for item in beam1.linked_subsystems)
    #print(steel.linked_components)
    
    #print(type(steel.linked_components))
    #print( beam1.volume )
    #print( beam2.volume )
    #print( beam1.area_moment_of_inertia )
    #print( beam2.area_moment_of_inertia )
    ##"""We can have a look at for instance their bending stiffnesses"""
    #print( beam1.bending_stiffness )
    #print( beam2.bending_stiffness )
    ##"""indeed, the second beam is more stiff."""
    
    ##"""Next step is to define the subsystems. In this example we will only be including longitudinal waves."""
    ###subsystem1 = system1.addSubsystem('sub1', 'long', 'beam1')
    ###subsystem2 = system1.addSubsystem('sub2', 'long', 'beam2')
    
    ##"""Then we add the junctions. We connect the beams at their tips so it will be a 1D junction."""
    ##junction1 = system1.addjunction('junction1', 'Junction', shape='Point')
    ##junction1.addComponent(beam1, 'corner')
    ##junction1.addComponent(beam2, 'corner')


    ##"""Let's excite the system with longitudinal waves in the first beam."""
    ##subsystem1 = beam1.subsystem_long
    ##excitation1 = subsystem1.addExcitation('excitation1', 'ExcitationRain', power=[1.0, 1.0, 1.0, 1.0])

    ##"""Let's have a look at the modal densities before we start the computation."""
    ###subsystem1.plot_modal_density('modal_density_subsystem1.png')
    ###subsystem2.plot_modal_density('modal_density_subsystem2.png')
    
    ###print subsystem1.component.volume
    ###print steel.linked_components
    ###"""Finally, we solve for the modal powers"""    
    ##system1.solveSystem()
    
    ###"""And indeed, the system is solved."""
    ###print system1.solved
    
    ###"""Now we can plot for instance the velocity levels in the subsystems."""
    ###subsystem1.plot_velocity_level('velocity_level_subsystem1.png')
    ###subsystem2.plot_velocity_level('velocity_level_subsystem2.png')
       
    ###"""Or the velocity levels in the components, which is given by a summation over its related subsystems."""
    ###beam1.plot_velocity_level('velocity_level_beam1.png')
    ###beam2.plot_velocity_level('velocity_level_beam2.png')    
    ###"""Since we included only one subsystem per component, the results are the same."""
    
        
if __name__ == "__main__":
    main()
