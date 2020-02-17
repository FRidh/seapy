import math
import cmath

import warnings


# import scipy.constants as physical_constants  # Container of physical constants which might be of use
import numpy as np
from .material import Material

from ..base import Base, Attribute, LinkedList


class MaterialSolid(Material):
    """
    Solid material class
    """

    description = "A material in solid state."

    young = Attribute()
    shear = Attribute()
    poisson = Attribute()


def modulus(out, young=None, bulk=None, shear=None, poisson=None):
    """Calculate `out` using `given`.
    
    :param out: Desired elastic modulus.
    :param young: Young's modulus.
    :param bulk: Bulk modulus.
    :param shear: Shear modulus.
    :param poisson: Poisson ration.
    
    This function determines the desired elastic modulus using the given moduli.
    """

    if out == "bulk":
        if young and shear:
            return (young * shear) / (9.0 * shear - 3.0 * young)
        elif young and poisson:
            return (young) / (3.0 - 6.0 * poisson)
        elif shear and poisson:
            return 2.0 * shear * (1.0 + poisson) / (3.0 - 6.0 * poisson)
    elif out == "young":
        if bulk and shear:
            return 9.0 * bulk * shear / (3.0 * bulk + shear)
        elif young and poisson:
            return 3.0 * bulk * (1.0 - 2.0 * poisson)
        elif shear and poisson:
            return 2.0 * shear * (1.0 + poisson)
    elif out == "shear":
        if bulk and young:
            return 3.0 * bulk * young / (9.0 * bulk - young)
        elif bulk and poisson:
            return 3.0 * bulk * (1.0 - 2.0 * poisson) / (2.0 + 2.0 * poisson)
        elif young and poisson:
            return young / (2.0 + 2.0 * poisson)
    elif out == "poisson":
        if bulk and young:
            return (3.0 * bulk - young) / (6.0 * bulk)
        elif bulk and shear:
            return (3.0 * bulk - 2.0 * shear) / (6.0 * bulk + 2.0 * shear)
        elif young and shear:
            return (young) / (2.0 * shear) - 1.0

    raise ValueError("Cannot determine {} with the given moduli.".format(out))
