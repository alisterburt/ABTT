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

    def test_roty_z(self):
        initial_point = np.array([0, 0, 1])
        rotation_matrix = ABTT.math.rotate3d.rotate_y(90)
        final_point = np.matmul(rotation_matrix, initial_point)
        np.testing.assert_array_almost_equal([1, 0, 0], final_point)

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


class EulerAnglesTest(unittest.TestCase):
    def test_calculate_rotation_matrix_ZXZ(self):
        euler_triplet = [-156, 64, 198]
        dynamo_euler2matrix_results = [[0.8137, -0.5106, -0.2777],
                                       [0.4519, 0.2552, 0.8548],
                                       [-0.3656, -0.8211, 0.4384]]

        rotation_matrix = ABTT.math.euler_angles.calculate_rotation_matrix(euler_triplet, 'ZXZ')

        np.testing.assert_array_almost_equal(dynamo_euler2matrix_results, rotation_matrix, decimal=4)

    def test_calculate_rotation_matrix_ZYZ(self):
        euler_triplet = [107.81, 63.924, -65.55]
        # This should in theory, verified by relion reconstruct vs dynamo_average, yield the same rotation as
        # [-156, 64, 198] or the transpose (I think it should be the transpose... lol)
        rotation_matrix = ABTT.math.euler_angles.calculate_rotation_matrix(euler_triplet, 'ZYZ')
        # NAN cest pas pareil merde
