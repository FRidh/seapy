from seapy.base.base import UniqueName, NameWarning


class UniqueNameHolder:

    name = UniqueName()

    def __init__(self, system, name):
        self.system = system
        self.name = name


class UniqueNameSystem:
    def __init__(self):
        self._objects = list()

    def objects(self):
        return self._objects


def test_UniqueName(recwarn):
    """
    Test descriptor whether unique names are assigned.
    """

    s = UniqueNameSystem()
    s._objects.append(UniqueNameHolder(s, "a"))
    s._objects.append(UniqueNameHolder(s, "b"))
    s._objects.append(UniqueNameHolder(s, "b"))

    names = [i.name for i in s.objects()]
    assert len(names) == len(set(names))

    w = recwarn.pop(NameWarning)
    assert issubclass(w.category, NameWarning)
