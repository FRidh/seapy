.. _quantities:

Quantities
###########

.. toctree::
   :maxdepth: 2



The following is a list of all physical quantities relevant to SEA.

.. _quantities_general:

==================
General quantities
==================

.. glossary::

    frequency
        Frequency `f` is the number of occurrences of a repeating event per unit time and has the unit hertz (Hz).
          
    
    angular frequency
        Angular frequency :math:`\omega` is the frequency of an oscillation in unit radians per second (rad/s).

        .. math::

            \omega = 2 \pi f
            
    speed of sound
        Speed of sound `c` describes the speed at which a wave passes through a medium.

            Phase speed :math:`c_{phase}`

            Group speed :math:`c_{group}` 


        
        
.. _quantities_mechanical:

=====================
Mechanical quantities
=====================

.. glossary::


    aera moment of inertia
    second moment of inertia
        Area moment of area, also known as 'second moment of inertia, 'moment of inertia of plane area, or 'second area moment', 
        is a geometrical property of an area which reflects how its points are distributed with regards to an arbitrary axis.
        It has unit (m^4).

        
    torsional moment of rigidity
        The torsional moment of rigidity `J`

        
    radius of gyration
        Radius of gyration :math:`\kappa` or gyradius is the name of several related measures of the size of an object, a surface, 
        or an ensemble of points. It is calculated as the root mean square distance of the objects' parts from either its center of gravity or a given axis.
        
        
        .. seealso:: http://en.wikipedia.org/wiki/Radius_of_gyration



.. _quantities_energy:

=================
Energy quantities
=================

.. glossary::

    velocity
        The velocity `v`


    velocity level
        The velocity level :math:`L_v` is given by
        
        .. math:: L_v = 20 \log_{10}{\frac{v}{v_0}}

        where :math:`v_0` is a reference velocity.
        
    mobility
        The mobility `Y` describes how easily a body moves when subject to a force.
            
    energy
        The energy `E`

    power dissipation
        The power dissipation `P` in a subsystem `i` is given  by
        
        .. math:: P_{dis,i} = \omega \eta n_i
    
        where :math:`\eta` is the loss factor of the subsystem.
    

    
.. _quantities_modal:

================
Modal quantities
================

.. glossary::


    conductivity
        The conductivity `C` describes the vibrational coupling.
        The coupling is however more often desribed by coupling loss factors. The conductivity and the coupling loss factor are related as
        
        .. math:: C_{i,j} = \omega n_i \eta_c^{i,j} = \omega n_j \eta_c^{j,i}

    
    coupling loss factor
        The coupling loss factors describes the losses in a coupling.
    
    mode count
        The mode count `N` is the amount of modes up to the angular frequency :math:`\omega`. 
        For a simple structure this value can be calculated, while more complex structures require :term:`FEA` or estimations.

    modal density    
        The modal density `n` is obtained by differentiating the mode count `N` with respect to the angular frequency :math:`\omega`.

        .. math::
            
            n = \frac{dN}{d \omega}

        Modal densities in SeaPy are as function of :math:`\omega`, so :math:`n(\omega)`
        
    modal overlap
        The modal overlap `M` describes the overlap of modes and thus dissipation.
        
        .. math::
        
            M = \eta \omega N
   

    modal energy
        The modal energy `e` is the energy in a band per mode.
        
        .. math::
        
            e = \frac{E}{\frac{dN}{d \omega}} = \frac{E}{N}
            
            
   


.. _quantities_material:

===================
Material quantities
===================
        
.. glossary::

    density
        The density :math:`\rho`
        
    young's modulus
        Young's modulus `E`, also known as the tensile modulus or elastic modulus, 
        is a measure of the stiffness of an elastic material, and has the unit pascal (Pa).


    bending stiffness
    flexural rigidity
        The bending stiffness or flexural rigidity `D`.


    shear modulus
        Shear modulus `G` or modulus of rigidity, is defined as the ratio of shear stress to the shear strain, and has the unit pascal (Pa).


    bulk modulus
        Bulk modulus `K` of a substance measures the substance's resistance to uniform compression. 
        It is defined as the ratio of the infinitesimal pressure increase to the resulting relative decrease 
        of the volume, and has the unit pascal (Pa).


    poisson's ratio
        Poisson's ratio :math:`\nu` is the negative ratio of transverse to axial strain. Poisson's ratio is dimensionless.

    loss factor 
    .. _lossfactor:
        Loss factor :math:`\eta` describes the amount of energy lost per cycle.
        
        .. math:: \eta = \frac{W}{E \omega}
            
            
            
            
            
