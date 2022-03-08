import math
import pint
from pint import UnitRegistry


class SupplyGraph:
    def __init__(self):
        self.ureg = UnitRegistry()
        self.nodes = {}

    def add_node(self, node_name, node):
        assert(node_name not in self.nodes)
        self.nodes[node_name] = node
        return node

    def convert_value(self, v):
        if isinstance(v, str):
            v = self.ureg.parse_expression(v)
        return v

    def to_kelvin(self, temperature):
        return temperature.to("kelvin")

    def temperature(self, temperature, unit = None):
        temperature = self.convert_value(temperature)
        if unit == None:
            unit = self.ureg.kelvin
        else:
            unit = getattr(self.ureg, unit)
        return self.to_kelvin(self.ureg.Quantity(temperature, unit))

    def to_pascal(self, pressure):
        return pressure.to("pascal")

    def pressure(self, pressure, unit = None):
        pressure = self.convert_value(pressure)
        if unit == None:
            unit = self.ureg.pascal
        else:
            unit = getattr(self.ureg, unit)
        return self.to_pascal(self.ureg.Quantity(pressure, unit))

    def to_mole(self, amount):
        return amount.to("mole")

    def amount(self, amount, unit=None):
        amount = self.convert_value(amount)
        if unit == None:
            unit = self.ureg.mol
        else:
            unit = getattr(self.ureg, unit)
        return self.to_mole(self.ureg.Quantity(amount, unit))

    def to_mol_s_m1(self, flow):
        return flow.to("mol/s")

    def flow(self, flow, unit=None):
        flow = self.convert_value(flow)
        if unit == None:
            unit = self.ureg.mol * self.ureg.s**(-1)
        else:
            unit = getattr(self.ureg, unit)
        return self.to_mol_s_m1(self.ureg.Quantity(flow, unit))

    def to_s(self, time):
        return time.to("s")

    def time(self, time, unit=None):
        time = self.convert_value(time)
        if unit == None:
            unit = self.ureg.s
        else:
            unit = getattr(self.ureg, unit)
        return self.to_s(self.ureg.Quantity(time, unit))

class SupplyVertex:
    def __init__(self, graph):
        self.graph = graph

class SupplyConnection:
    def __init__(self, dest_name, src_node, src_name):
        self.dest_name = dest_name
        self.src_node = src_node
        self.src_name = src_name

class SupplyNode:
    def __init__(self, graph):
        self.graph = graph
        self.connections = {}
        self.produced = self.graph.convert_value("0 mol")

    def update_produced(self, amount):
        self.produced += amount

    def get_produced(self):
        return self.produced

    def connect(self, src_node, src_name = "output", dest_name = "input"):
        assert(dest_name not in self.connections)
        self.connections[dest_name] = SupplyConnection(dest_name, src_node, src_name)

    def run(self, amount, dt, name = None):
        raise NotImplementedError("Implement run for class " + self.__class__.__name__)

    def register(self, name_in_graph):
        return  self.graph.add_node(name_in_graph, self)

    def consume(self, src_node, src_name = "output", dest_name = "input"):
        self.connect(src_node, src_name, dest_name)
        return self


    def parse_max_flow(self, max_flow):
        if max_flow is None:
            max_flow = None
        else:
            max_flow = self.graph.flow(max_flow)
        return max_flow

    def limit_amount(self, amount, dt):
        dt = self.graph.time(dt)
        amount = self.graph.amount(amount)
        if self.max_flow is not None:
            amount = min(amount, dt * self.max_flow)
        return amount

class ChemicalSpecies(SupplyVertex):
    def __init__(self, graph, name, temperature, pressure, amount):
        super().__init__(graph)
        self.name = name
        self.temperature = temperature
        self.pressure = pressure
        self.amount = amount

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, temperature={self.temperature}, pressure={self.pressure:e}, amount={self.amount})"

class EnergySupply(SupplyNode):
    pass

class ChemicalSpeciesSupply(SupplyNode):
    # temperature in kelvins
    # pressure in Pa
    # max_flow in mol.s-1
    def __init__(self, graph, name, temperature, pressure, max_flow = None):
        super().__init__(graph)
        self.name = name
        self.temperature = graph.temperature(temperature)
        self.pressure = graph.pressure(pressure)
        self.max_flow = self.parse_max_flow(max_flow)


    def run(self, amount, dt, name = None):
        assert(name == None or name == "main")
        amount = self.limit_amount(amount, dt)
        self.update_produced(amount)

        ret = ChemicalSpecies(self.graph, self.name, self.temperature, self.pressure, amount)
        return ret



class Heater(SupplyNode):
    def __init__(self, graph, matter_input, energy_input, temperature, pressure, max_flow = None):
        super().__init__(graph)
        self.consume(matter_input, dest_name = "matter_input")
        self.consume(energy_input, dest_name = "energy_input")

class SabatierReaction(SupplyNode):
    def __init__(self):
        super().__init__()

    def run(self):
        pass
