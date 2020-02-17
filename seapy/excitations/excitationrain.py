from .excitation import Excitation


class ExcitationRain(Excitation):
    """
    Rain on the roof excitation
    """

    @property
    def power(self):
        raise NotImplementedError
