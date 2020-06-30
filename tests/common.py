from typing import Dict

import pytest
import numpy as np
from acoustics.signal import OctaveBand

import seapy
from seapy.materials.materialsolid import modulus


@pytest.fixture
def steel_attributes() -> Dict:
    """Attributes of a steel material."""
    young=1.0e7
    poisson=0.30
    attributes = {
        "name": "steel",
        "model": "MaterialSolid",
        "young": young,
        "poisson": poisson,
        "loss_factor": 0.002,
        "density": 8000.,
        "temperature": 293.,
        "bulk": modulus("bulk", young=young, poisson=poisson),
        "shear": modulus("shear", young=young, poisson=poisson),
    }
    return attributes


@pytest.fixture
def system():
    """System with frequencies."""
    frequency = OctaveBand(fstart=500.0, fstop=8000.0, fraction=1)
    system = seapy.system.System(frequency)
    return system