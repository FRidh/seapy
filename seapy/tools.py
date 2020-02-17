import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import networkx as nx
import itertools
import toolz

from functools import reduce
from operator import mul


def product(iterable):
    """Calculate product of items in iterable.
    """
    return reduce(mul, iterable, 1)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def plot(x, y, quantity, visible, yscale="linear"):
    """
    Plot `y` as function of `x` where `y` has quantity `quantity` and `x` is frequency :math:`f`.
    
    :param x: Array of values for the `x`-axis.
    :param y: Array of values for the `y`-axis.
    :param quantity: Quantity
    :param visible: Array of booleans.
    
    :returns: Figure.
    :type: :class:`matplotlib.figure.Figure`
    
    
    """
    mask = ~visible.astype(bool)
    x = ma.masked_array(x, mask=mask).compressed()
    y = (ma.masked_array(i, mask=mask).compressed() for i in y)

    try:
        label = ATTRIBUTES[quantity]
    except KeyError:
        label = "Unknown quantity"

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in y:
        ax.scatter(x, i)
    ax.set_xscale("log")
    ax.set_yscale(yscale)
    ax.set_xlabel("$f$ in Hz")
    ax.set_ylabel(label)
    ax.grid()
    return fig


ATTRIBUTES = {
    "pressure_level": "$L_p$ in dB",
    "velocity_level": "$L_v$ in dB",
    "power_level": "$L_P$ in dB",
    "mass": "$m$ in kg",
    "impedance": "$Z$ in ...",
    "resistance": "$R$ in ...",
    "reactance": "$X$ in ...",
    "resistance_point_average": "$R$ in ...",
    "mobility": "$Y$ in ...",
    "modal_density": "$n$ in ...",
    "average_frequency_spacing": "$\Delta f$ in Hz",
    "soundspeed_group": "$c_{g}$ in m/s",
    "soundspeed_phase": "$c_{\phi}$ in m/s",
    "clf": "$\eta$ in ...",
    "input_power": "$P$ in W",
    "loss_factor": "$\eta$ in $\mathrm{rad}^{-1}$",
    "wavenumber": "$k$ in rad/m",
    "power": "$P$ in W",
    "conductance": "$G$ in ...",
    "susceptance": "$B$ in ...",
    "sound_reduction_index": "$R$ in ...",
    "tau": "$\tau$ in ...",
}


# edges = ((obj.name, getattr(obj, b).name) for obj in getattr(system, b+'s'))
# G.add_edges_from(edges)
# except AttributeError:
# pass

# try:
# edges = ((obj.name, getattr(obj, b).name) for obj in getattr(system, b+'s'))
# G.add_edges_from(edges)
# except AttributeError:
# pass


def graph_couplings(system):
    """Graph with subsystems as nodes and couplings as edges.
    """

    G = nx.DiGraph()

    nodes = (obj.name for obj in system.subsystems)
    edges = (
        (obj.subsystem_from.name, obj.subsystem_to.name, {"name": obj.name})
        for obj in system.couplings
    )

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


class Path(object):
    """Path between two subsystems.
    
    .. warning:: If changes are made in the actual paths in the system, then this object will yield invalid results! 
    
    """

    def __init__(self, system, path):

        self._path = path
        """The path is a list of names of subsystems and couplings.
        """

        self._system = system
        """Reference to system.
        """

    def __repr__(self):
        return "Path({})".format(self._path)

    def __str__(self):
        return str(self._path)

    def __iter__(self):
        yield from self._path

    @property
    def subsystems(self):
        """Subsystems in path.
        """
        for name in self._path:
            obj = self._system.get_object(name)
            if obj.SORT == "Subsystem":
                yield obj

    @property
    def couplings(self):
        """Couplings in path.
        """
        for name in self._path:
            obj = self._system.get_object(name)
            if obj.SORT == "Coupling":
                yield obj

    @property
    def energy_ratio(self):
        """Energy ratio :math:`\\frac{E_n}{_{1}}`.
        
        See Craik, equation 6.43.
        """
        clf = (obj.clf for obj in self.couplings)
        tlf = (obj.tlf for obj in self.subsystems)
        return product(clf) / product(tlf)

    @property
    def level_difference(self):
        """Attenuation along path.
        
        .. math:: 10 \\log_{10}{\\frac{E_1}{E_n}}
        
        See Craik,  equation 6.44
        """
        return -10.0 * np.log10(self.energy_ratio)  # Note the minus sign!

    def energy_due_to_excitation(self, excitation=None):
        """Energy in subsystem due to excitation.
        
        :param excitation: Excitation. Valid arguments are:
        * 'None', in which case the total power input to the first subsystem is considered;
        * an iterable with names or excitation objects;
        * a name of the excitation;
        * an excitation object.
        
        :returns: Energy in a subsystem.
        
        """
        angular = self._system.frequency.angular
        subsystem = toolz.first(self.subsystems)

        if excitation is None:
            power = subsystem.power_input
        elif toolz.isiterable(excitation):
            excitations = excitation
            power = np.zeros(len(self._system.frequency))
            for excitation in excitations:
                excitation = self._system.get_object(excitation)
                if excitation.subsystem == subsystem:
                    power += excitation.power
                else:
                    raise ValueError(
                        "Invalid excitation. The excitation {} is not connected to the first subsystem of this path, {}.".format(
                            excitation.name, subsystem.name
                        )
                    )
        else:
            excitation = self._system.get_object(excitation)
            if excitation.subsystem == subsystem:
                power = excitation.power
            else:
                raise ValueError(
                    "Invalid excitation. The excitation {} is not connected to the first subsystem of this path, {}.".format(
                        excitation.name, subsystem.name
                    )
                )

        return power / angular * self.energy_ratio


class PathAnalysis(object):
    """Path analysis.
    """

    def __init__(self, system):

        self._system = system

    def graph(self, objects=None):
        """Draw a graph of types specified in `objects`.
        
        .. note:: All objects are treated as nodes.
        
        """
        system = self._system
        G = nx.DiGraph()

        for sort in objects:
            nodes = (obj.name for obj in getattr(system, sort))  # +'s'))
            G.add_nodes_from(nodes)

        if "components" in objects and "subsystems" in objects:
            edges = ((obj.name, obj.component.name) for obj in system.subsystems)
            G.add_edges_from(edges)

        if "components" in objects and "materials" in objects:
            edges = ((obj.name, obj.component.name) for obj in system.materials)
            G.add_edges_from(edges)

        if "components" in objects and "junctions" in objects:
            edges = ((obj.name, obj.component.name) for obj in system.junctions)
            G.add_edges_from(edges)

        if "subsystems" in objects and "excitations" in objects:
            edges = ((obj.name, obj.subsystem.name) for obj in system.excitations)
            G.add_edges_from(edges)

        if "junctions" in objects and "couplings" in objects:
            edges = ((obj.name, obj.junction.name) for obj in system.couplings)
            G.add_edges_from(edges)

        if "subsystems" in objects and "couplings" in objects:
            for coupling in system.couplings:
                G.add_path(
                    (
                        coupling.subsystem_from.name,
                        coupling.name,
                        coupling.subsystem_to.name,
                    )
                )

            # edges = ((obj.subsystem_from.name, obj.subsystem_to.name) for obj in system.couplings)
            # G.add_edges_from(edges)

            # edges = ((obj.name, obj.subsystem_from.name) for obj in system.couplings)
            # G.add_edges_from(edges)
            # edges = ((obj.name, obj.subsystem_to.name) for obj in system.couplings)
            # G.add_edges_from(edges)
        return G

    def paths(self, subsystem_from, subsystem_to):
        """Determine all paths between specified subsystems.
        """
        subsystem_from = self._system.get_object(subsystem_from)
        subsystem_to = self._system.get_object(subsystem_to)
        G = self.graph(objects=["subsystems", "couplings"])

        yield from (
            Path(self._system, path)
            for path in nx.all_simple_paths(G, subsystem_from.name, subsystem_to.name)
        )

    def has_path(self, subsystem_from, subsystem_to):
        """Determine whether there is a connection between two subsystems.
        """
        subsystem_from = self._system.get_object(subsystem_from)
        subsystem_to = self._system.get_object(subsystem_to)
        G = self.graph(objects=["subsystems", "couplings"])

        return nx.has_path(G, subsystem_from.name, subsystem_to.name)

    # def energy_due_to_excitation(self, subsystem, excitation):
    # """Energy in `subsystem` due to `excitation`

    # See Craik, equation 6.47, page 163.
    # """
    # angular = self._system.frequency.angular
    # power = self._system.get_object(excitation).power

    # energy = power / angular *
