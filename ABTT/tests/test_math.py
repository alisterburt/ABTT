import unittest

import numpy as np

import ABTT.math


class Rotate3DTest(unittest.TestCase):
    def test_rotx_x(self):
        initial_point = np.array([1, 0, 0])
        rotation_matrix = ABTT.math.rotate3d.rotate_x(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_equal(initial_point, final_point)

    def test_rotx_y(self):
        initial_point = np.array([0, 1, 0])
        rotation_matrix = ABTT.math.rotate3d.rotate_x(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_almost_equal([0, 0, 1], final_point)

    def test_roty_y(selfs):
        initial_point = np.array([0, 1, 0])
        rotation_matrix = ABTT.math.rotate3d.rotate_y(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_equal(initial_point, final_point)

    def test_roty_x(self):
        initial_point = np.array([1, 0, 0])
        rotation_matrix = ABTT.math.rotate3d.rotate_y(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_almost_equal([0, 0, -1], final_point)

    def test_rotz_z(self):
        initial_point = np.array([0, 0, 1])
        rotation_matrix = ABTT.math.rotate3d.rotate_z(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_equal(initial_point, final_point)

    def test_rotz_x(self):
        initial_point = np.array([1, 0, 0])
        rotation_matrix = ABTT.math.rotate3d.rotate_z(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_almost_equal([0, 1, 0], final_point)
