
from .components import components_map
from .junctions import junctions_map
from .couplings import couplings_map
from .excitations import excitations_map
from .materials import materials_map


objects_map = {
    'component' : components_map,
    'junction': junctions_map,
    #'subsystem' : subsystems_map,
    'coupling' : couplings_map,
    'excitation' : excitations_map,
    'material' : materials_map,
    }
    
