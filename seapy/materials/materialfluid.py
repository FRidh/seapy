from .material import Material


class MaterialFluid(Material):
    """
    Fluid material.
    """

    pressure = Attribute()
    """
    Pressure :math:`p`
    """
