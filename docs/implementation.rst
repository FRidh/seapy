.. _implementation:

SeaPy implementation
####################

.. toctree::
   :maxdepth: 2
   
The previous chapter explained what Statistical Energy Analysis is. 
In this chapter we will have a closer look on how SEA is implemented.

=========
Overview
=========

An SEA model in SeaPy is represented by the descendents of the following abstract objects:

* :class:`seapy.components.component.Component`
* :class:`seapy.subsystems.subsystem.Subsystem`
* :class:`seapy.junctions.junction.Junction`
* :class:`seapy.couplings.coupling.Coupling`
* :class:`seapy.materials.material.Material`
* :class:`seapy.excitations.excitation.Excitation`

as well as the main class representing the model

* :class:`seapy.system.System`

The following figure gives an overview on how the classes are related.

.. graphviz::

    digraph overview {
      Subsystem -> Component -> System;
      Coupling -> Junction -> System;
      Junction -> Component
      Coupling -> Subsystem
      Coupling -> Component
      Component -> Material -> System
      Excitation -> Subsystem
    }
    
Components can have multiple subsystems. Depending on the type of component these are added automatically when creating a component.
If components are connected to eachother a Junction needs to be created. The Junction will automatically create all possible couplings between the subsystems.
