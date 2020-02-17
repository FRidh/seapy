"""
Other equations.
================

This module contains all kind of additional equations than can be useful.

"""
import numpy as np


def total_loss_factor(frequency, reverberation_time):
    """
    The total loss factor can be related to the reverberation time for any subsystem.
    
    :param frequency: Frequency :math:`f`.
    :param reverberation_time: Reverberation time :math:`T`.
    
    :returns: Total loss factor.
    
    .. math:: \\eta = \\frac{2.2}{f T}

    See Craik, equation 1.19, page 9.

    """
    return 2.2 / (f * T)


def total_loss_factor_masonry(frequency):
    """
    A good estimate total loss factor for masonry type structures.
    
    :param frequency: Frequency :math:`f`.
    
    :returns: Total loss factor.
    
    .. math:: \\eta_2 \\approx \\frac{1}{\\sqrt{f}} + 0.015
    
    See Craik, equation 1.21, page 9.
    
    """
    return 1.0 / np.sqrt(f) + 0.015
