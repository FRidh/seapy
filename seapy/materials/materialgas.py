from ..base import Attribute
from .material import Material


class MaterialGas(Material):
    """
    Gas material.
    """

    pressure = Attribute()
    """
    Pressure :math:`p`
    """
