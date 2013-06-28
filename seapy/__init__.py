"""
The model contains classes describing the physics of all the SEA objects.

Each sort of component, subsystem, coupling, excitation and material has a class of its own.
Every type has a baseclass describing properties that are common.
Ultimately, every object in this module except for System is derived from :class:`Sea.model.base.BaseClass`.

The :class:`Sea.model.system.System` class contains methods for solving the SEA model.


"""

import system
import connections
import components
import subsystems
import couplings
import excitations
import materials

import objects_map