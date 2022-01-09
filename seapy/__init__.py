"""


The model contains classes describing the physics of all the SEA objects.

Each sort of component, subsystem, coupling, excitation and material has a class of its own.
Every type has a baseclass describing properties that are common.
Ultimately, every object in this module except for System is derived from :class:`seapy.base.Base.Base`.

The :class:`seapy.system.System` class contains methods for solving the SEA model.


.. automodule:: seapy.base
    :no-members:
.. automodule:: seapy.tools
    :no-members:
.. automodule:: seapy.system
    :no-members:
.. automodule:: seapy.materials
    :no-members:
.. automodule:: seapy.components
    :no-members:
.. automodule:: seapy.subsystems
    :no-members:
.. automodule:: seapy.junctions
    :no-members:
.. automodule:: seapy.couplings
    :no-members:
.. automodule:: seapy.excitations
    :no-members:


"""

__version__ = "0.0.0"

from . import system
from . import junctions
from . import components
from . import subsystems
from . import couplings
from . import excitations
from . import materials

from . import objects_map


from .system import System
