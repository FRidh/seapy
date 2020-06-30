from acoustics.signal import OctaveBand
import seapy
import numpy as np
import pytest

from .common import steel_attributes


@pytest.fixture
def system(steel_attributes):
    frequency = OctaveBand(fstart=500.0, fstop=8000.0, fraction=1)
    system = seapy.system.System(frequency)

    steel = system.add_material(**steel_attributes)

    pipe1 = system.add_component(
        "pipe1",
        "ComponentPipe",
        material="steel",
        length=2.0,
        radius=0.15,
        thickness=0.002,
    )

    return system


class TestComponentPipe:
    def test_available_subsystems(self, system):
        pipe = system.get_object("pipe1")

        subsystems = set(("subsystem_long", "subsystem_bend", "subsystem_shear"))
        assert subsystems == set(pipe.SUBSYSTEMS.keys())


class TestSubsystemBend:
    @pytest.fixture
    def subsystem(self, system):
        return system.get_object("pipe1").subsystem_bend

    def test_frequency_spacing(self, subsystem):
        subsystem.component.material.density
        subsystem.average_frequency_spacing
