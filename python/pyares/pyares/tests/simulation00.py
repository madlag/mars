import unittest
from unittest import TestCase
import pyares.chemistry as chemistry

class TestFun(TestCase):
    def test_units(self):
        g = chemistry.SupplyGraph()
        t = g.temperature(20, "degC")
        self.assertEqual(str(t), "293.15 kelvin")

        t = g.pressure(20, "bar")
        self.assertEqual(str(t), "2000000.0 pascal")

        t = g.amount(20, "mole")
        t = g.to_mole(t)
        self.assertEqual(str(t), "20 mole")

    def test_basic_graph00(self):
        g = chemistry.SupplyGraph()
        co2 = chemistry.ChemicalSpeciesSupply(g, "CO2", 273, "10 bars").register("co2")
        o = co2.run("1 mole", 1)
        self.assertEqual(str(o), "ChemicalSpecies(name=CO2, temperature=273 kelvin, pressure=1.000000e+06 pascal, amount=1 mole)")
        c = co2.get_produced()
        self.assertEqual(str(c), "1 mole")

    def test_basic_graph01(self):
        g = chemistry.SupplyGraph()
        co2 = chemistry.ChemicalSpeciesSupply(g, "CO2", 273, "10 bars", "1 mole/s").register("co2")
        o = co2.run("10 mole", 1)
        self.assertEqual(str(o), "ChemicalSpecies(name=CO2, temperature=273 kelvin, pressure=1.000000e+06 pascal, amount=1.0 mole)")
        c = co2.get_produced()
        self.assertEqual(str(c), "1.0 mole")

    def test_basic_graph02(self):
        g = chemistry.SupplyGraph()
        energy = chemistry.EnergySupply(g)
        co2 = chemistry.ChemicalSpeciesSupply(g, "CO2", 273, 10e5).register("co2")
        co2heater = chemistry.Heater(g, co2, energy, 673 , 30e5)
        h2 = chemistry.ChemicalSpeciesSupply(g, "H2", 273, 10e5).register("h2")
        h2heater = chemistry.Heater(g, h2, energy, 673, 30e5)


if __name__ == '__main__':
    unittest.main()