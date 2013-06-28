# Introduction

SeaPy is a Python module to assist in performing a Statistical Energy Analysis, or SEA.
SEA is used within vibroacoustics to model the flow of acoustic power through a vibrating system. 
An example is modeling the vibrations in cars due to the engine. 
SEA is generally used in the high-frequency region whereas finite-element analysis is used in the low-frequency region. 

First step in performing an SEA is creating the geometry. 
Then, the relevant components are modeled as subsystems, where each subsystem represents one wave type.
The subsystems are then connected through couplings. 
Power is added into the system through excitation of one or more subsystems. 
Power dissipation in subsystems and couplings are modeled using loss factors. 
Finally, a single matrix composed of loss factors, modal densities and input powers, are solved resulting in the modal energies of each subsystem, from which their vibration or noise levels can be calculated.

# SeaPy

This module provides several classes and functions to perform an SEA. First, an object of the main class System() has to be created.
Then, components, subsystems, couplings and excitations can be added to the System() instance.
Finally, when all properties have been set, the modal energies can be solved by executing the solve_system() method of the System() instance.



# Prerequisites

Required are:

- Python 3.4 or higher
- NumPy
- matplotlib
- pandas
- toolz


# Installing

Via pip:

    pip install seapy

Via conda:

    conda install -c ...
    
Or clone this repository:


## Documentation

Documentation can be viewed at [Python Hosted(https://pythonhosted.org/seapy/) and also [here](http://www.fridh.nl/seapy/).


## To do

There's still plenty to be done. Some of the most important things to do are, in order of importance:

1. Implement several junctions. E.g., one that allows calculating the coupling loss factors between multiple plates.
2. Improve handling of spectral values.
2. Adjust impedance based on position of excitation
3. Enable and disable objects per band. This would allow for frequency-dependent models without having to make entirely new or separate models.
4. Path analysis


## Reporting bugs
