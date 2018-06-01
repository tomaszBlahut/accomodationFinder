from unittest import TestCase
from haversine_formula.haversine_formula import HaversineFormula


class TestHaversineFormula(TestCase):
    def test_calculate_distance_beetween_two_points(self):
        hav = HaversineFormula.calculate_distance_beetween_two_points(-86.67, -118.40, 36.12, 33.94)
        self.assertAlmostEqual(hav, 2887259.950607, 6)

    def test_calculate_square_bounds(self):
        results = HaversineFormula.calculate_square_bounds(-86.0, 36.0, 100000)
        self.assertAlmostEqual(results['up']['longitude'], -86.0, 6)
        self.assertAlmostEqual(results['up']['latitude'], 36.8990675, 6)
        self.assertAlmostEqual(results['right']['longitude'], -84.8887394, 6)
        self.assertAlmostEqual(results['right']['latitude'], 35.9948752, 6)
        self.assertAlmostEqual(results['down']['longitude'], -86.0, 6)
        self.assertAlmostEqual(results['down']['latitude'], 35.1009324, 6)
        self.assertAlmostEqual(results['left']['latitude'], 35.9948752, 6)
        self.assertAlmostEqual(results['left']['longitude'], -87.1112605, 6)
