# -*- coding: utf-8 -*-
"""Tests for multiset methods in module pymsetmath

    Test specification
    ------------------
    - test internal methods
    - test i/o arguments
    - test math
    - test functionality

:Author: Hy Carrinski

"""

from decimal import Decimal
import math
import random
import unittest

#from pymsetmath.pymsetmath import Multiset, is_nonneg_int
#from pymsetmath.examples import prob_of_missing as mset_prob
from pymsetmath import is_nonneg_int, Multiset, examples

class TestMultisetMath(unittest.TestCase):

    """Test Multiset calculations."""

    def setUp(self):
        self.mset = Multiset()

    def tearDown(self):
        self.mset.clear()
        self.mset = None

    def test_factorial_random_inputs(self):
        """Test factorial random inputs."""
        for val in random.sample(xrange(300), 5):
            result = self.mset.factorial(val)
            expected = math.factorial(val)
            self.assertEqual(result, expected)

    def test_factorial_bad_inputs(self):
        """Test factorial bad inputs."""
        inputs = (-1, None)
        for value in inputs:
            self.assertRaises(ValueError, self.mset.factorial, value)

    def test_factorial_small_inputs(self):
        """Test factorial small inputs."""
        pairs = ((0, 1), (1, 1), (2, 2), (3, 6))
        for (value, expected) in pairs:
            self.assertEqual(self.mset.factorial(value), expected)

    def test_clear_method(self):
        """Test clear method."""
        self.mset.factorial(10)
        self.assertTrue(len(self.mset._data) > 10)
        self.mset.clear()
        self.assertTrue(len(self.mset._data) == 1)

    def test_is_nonneg_int_on_several_inputs(self):
        """Test is_nonneg_int on several inputs."""
        pairs = ((None, False), (-1, False),
            (0, True), (1, True), (5.0, True))
        for (value, expected) in pairs:
            self.assertEqual(is_nonneg_int(value), expected)

    def test_uniq_msets_on_bad_input(self):
        """Test uniq_msets on on bad input."""
        f = lambda total, length: list(self.mset.uniq_msets(total, length))
        self.assertRaises(TypeError, f, 10, None)
        self.assertRaises(ValueError, f, -3, 2)

    def test_uniq_msets_on_several_inputs(self):
        """Test uniq_msets on on several inputs."""
        pairs = {(10, 0): [()], (10, 1): [(10,)]}
        for (value, expected) in pairs.items():
            result = list(self.mset.uniq_msets(*value))
            self.assertEqual(result, expected)

    def test_uniq_msets_contains_unique_elements(self):
        """Test uniq_msets contains unique elements."""
        expected = set([(3, 2), (4, 1), (5, 0)])
        result = set(self.mset.uniq_msets(5, 2))
        self.assertEqual(result, expected)

    def test_uniq_msets_contains_correct_number_of_elements(self):
        """Test uniq_msets contains correct number of elements."""
        result = list(self.mset.uniq_msets(5, 2))
        self.assertEqual(len(result), len(set(result)))

    def test_num_ways_n_tuple_key(self):
        """Test num_ways n tuple key."""
        expected = (4, 5, 5)
        num_ways = self.mset.num_ways
        result = tuple(len(list(num_ways(4, 4, x))) for x in xrange(1,4))
        self.assertEqual(result, expected)

    def test_number_of_arrangements_bad_input(self):
        """Test number_of_arrangements bad input."""
        num_arrange = self.mset.number_of_arrangements
        self.assertRaises(TypeError, num_arrange, 5)
        self.assertRaises(TypeError, num_arrange, None)
        self.assertRaises(ValueError, num_arrange, ())

    def test_number_of_arrangements_good_input(self):
        """Test number_of_arrangements good input."""
        pairs = (((3,), 1), ((2, 3), 2), ((1, 2, 3), 6))
        num_arrange = self.mset.number_of_arrangements
        for (value, expected) in pairs:
            self.assertEqual(num_arrange(value), expected)

    def test_iterate_through_number_of_arrangements_list_input(self):
        """Test iterate through number_of_arrangements list input."""
        groups = [(0, 5), (1, 4), (2, 3)]
        result = dict((grp, self.mset.number_of_arrangements(grp))
                    for grp in groups)
        expected = {(0, 5): 2, (1, 4): 2, (2, 3): 2}
        self.assertEqual(result, expected)

    def test_iterate_through_number_of_arrangements_by_uniq_msets(self):
        """Test iterate through number_of_arrangements by uniq_msets."""
        result = dict((grp, self.mset.number_of_arrangements(grp))
                    for grp in self.mset.uniq_msets(5, 2))
        expected = {(5, 0): 2, (4, 1): 2, (3, 2): 2}
        self.assertEqual(result, expected)

    def test_multinomial_coeff_bad_inputs(self):
        """Test multinomial_coeff bad inputs."""
        m_coeff = self.mset.multinomial_coeff
        self.assertRaises(TypeError, m_coeff, None)
        self.assertRaises(ValueError, m_coeff, ())

    def test_multinomial_coeff_good_inputs(self):
        """Test multinomial_coeff good inputs."""
        pairs = (((0,), 1), ((3,), 1), ((2, 3), 10), ((1, 2, 3), 60))
        m_coeff = self.mset.multinomial_coeff
        for (value, expected) in pairs:
            self.assertEqual(m_coeff(value), expected)

    def test_number_arrangements_of_uniq_msets_is_mset_number(self):
        """Test number_arrangements of uniq_msets is mset number."""
        for n in (5, 15, 30):
            for m in (3, 6):
                l1 = self.mset.multiset_number(n, m)
                l2 = sum(self.mset.number_of_arrangements(ms)
                    for ms in self.mset.uniq_msets(n, m))
                self.assertEqual(l1, l2)

    def test_num_uniq_msets_is_equal_to_calculated_number(self):
        """Test num_uniq_msets is equal to calculated number."""
        for n in (5, 15, 30):
            for m in (3, 6):
                l1 = self.mset.num_uniq_msets(n, m)
                l2 = sum(1 for ms in self.mset.uniq_msets(n, m))
                self.assertEqual(l1, l2)

class TestProbabilities(unittest.TestCase):

    """Test probability calculation examples."""

    def test_ex_compute_prob_top_100_from_10_return_15(self):
        """Test ex compute prob top 100 from 10 return 15."""
        for stats in examples.compute_probabilities(100, 10):
            if stats['count'] == 15:
                print stats
                result = stats['p']
                break
        expected = 0.5929
        self.assertAlmostEqual(result, expected, 3)


    def test_ex_compute_prob_and_use_threshold(self):
        """Test ex compute prob and use threshold."""
        for stats in examples.compute_probabilities(5, 2, 4):
            result = stats
        self.assertEqual(result['count'], 4)
        self.assertAlmostEqual(result['p'], 0.375, 3)

    def test_ex_compute_prob_with_boundary_threshold(self):
        """Test ex compute prob with boundary threshold."""
        result = None
        for stats in examples.compute_probabilities(5, 2, 1):
            result = stats
        self.assertTrue(result is None)

    def test_ex_compute_all_probabilities_for_5_and_2(self):
        """Test ex compute all prob for 5 and 2."""
        result = list(examples.compute_all_probabilities(5, 2))
        expected = [{'n': 5, 'm': 2, 'count': 3, 'p': Decimal('1')},
                    {'n': 5, 'm': 2, 'count': 4, 'p': Decimal('0.375')},
                    {'n': 5, 'm': 2, 'count': 5, 'p': Decimal('0.0625')}]
        for stats in result:
            stats['p'] = Decimal('%g' % stats['p'])
        self.assertEqual(result, expected)

    def test_ex_compute_all_probabilities_for_3_real_cases(self):
        """Test ex compute all prob for 3 real cases."""
        pairs = [({'n': 40, 'm': 4, 'count': 20}, float('2.2897244280e-03')),
                 ({'n': 40, 'm': 8, 'count': 10}, float('1.7789512134e-01')),
                 ({'n': 80, 'm': 4, 'count': 35}, float('7.8544408865e-04'))]
        for (param, expected) in pairs:
            n, m = param['n'], param['m']
            for stats in examples.compute_all_probabilities(n, m):
                if stats['count'] == param['count']:
                    break
            self.assertAlmostEqual(stats['p'], expected, 10)
