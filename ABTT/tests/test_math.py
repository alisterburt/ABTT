import unittest

import numpy as np

import ABTT.math


class Rotate3DTest(unittest.TestCase):
    """All rotation matrices describe passive rotations"""
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
        euler_triplet = [-155.55, 63.924, 197.81]  # euler angles are intrinsic
        dynamo_euler2matrix_results = [[0.8110, -0.5165, -0.2747],
                                       [0.4516, 0.2544, 0.8552],
                                       [-0.3718, -0.8177, 0.4396]]

        rotation_matrix = ABTT.math.euler_angles.calculate_rotation_matrix(euler_triplet, 'ZXZ', intrinsic=True)

        np.testing.assert_array_almost_equal(dynamo_euler2matrix_results, rotation_matrix, decimal=4)
        return rotation_matrix

    def test_calculate_rotation_matrix_ZYZ(self):
        euler_triplet = [107.81, 63.924,
                         -65.55]  # should give the same as matrix from test_calculate_rotation_matrix_ZXZ
        # This is verified by relion_reconstruct and dynamo_average giving the same result
        # I know dynamo euler angles are intrinsic because I programmed intrinsic rotations and got the same result
        # Should look at RELION code to see where their matrices/matrix multiplication is defined
        rotation_matrix = ABTT.math.euler_angles.calculate_rotation_matrix(euler_triplet, 'ZYZ', extrinsic=True)
        rotation_matrix_ref = self.test_calculate_rotation_matrix_ZXZ()
        np.testing.assert_array_almost_equal(rotation_matrix, rotation_matrix_ref, decimal=4)
        return rotation_matrix

    def test_matrix2ZYZeuler(self):
        euler_triplet_ref = [107.81, 63.924, -65.55]  # Extrinsic euler angles
        rotation_matrix = self.test_calculate_rotation_matrix_ZYZ()
        euler_triplet = ABTT.euler_angles.matrix2ZYZeuler(rotation_matrix, extrinsic=True)
        # euler_triplet may not be exactly the same because degenerate representations exist, compare rotation_matrices
        recalculated_rotation_matrix = ABTT.euler_angles.calculate_rotation_matrix(euler_triplet, 'ZYZ', extrinsic=True)
        np.testing.assert_array_almost_equal(rotation_matrix, recalculated_rotation_matrix)

    def test_matrix2ZXZeuler(self):
        euler_triplet_ref = [-155.55, 63.924, 197.81]  # Intrinsic euler angles
        rotation_matrix = self.test_calculate_rotation_matrix_ZXZ()
        euler_triplet = ABTT.euler_angles.matrix2ZXZeuler(rotation_matrix)
        # euler triplet may not be exactly the same because degenerate representations exist, compare rotation matrices
        recalculated_rotation_matrix = ABTT.euler_angles.calculate_rotation_matrix(euler_triplet, 'ZXZ', intrinsic=True)
        np.testing.assert_array_almost_equal(rotation_matrix, recalculated_rotation_matrix)

    def test_AngleConversion(self):
        euler_triplet_ZXZ_intrinsic = [-155.55, 63.924, 197.81]  # rotates_reference
        euler_triplet_ZYZ_extrinsic = [107.81, 63.924, -65.55]  # rotates reference

        conversion_object = ABTT.euler_angles.AngleConversion(euler_triplet_ZXZ_intrinsic, 'ZXZ', intrinsic=True)
        conversion_object.angles_from_rotation_matrices('ZYZ', extrinsic=True)
        np.testing.assert_array_almost_equal(np.asarray(euler_triplet_ZYZ_extrinsic).reshape((-1, 3)),
                                             conversion_object.euler_angles)

    def test_AngleConversion_software(self):
        euler_triplet_dynamo = [-155.55, 63.924, 197.81]  # ZXZ intrinsic rotates reference
        euler_triplet_relion = [107.81, 63.924, -65.55]  # ZYZ extrinsic rotates particle

        conversion_object = ABTT.euler_angles.AngleConversion(euler_triplet_dynamo,
                                                              from_software='dynamo',
                                                              target_software='relion')

        np.testing.assert_array_almost_equal(np.asarray(euler_triplet_relion).reshape((-1, 3)),
                                             conversion_object.euler_angles)


class CTFTest(unittest.TestCase):
    def test_electron_wavelength(self):
        electron_wavelength = ABTT.math.electron.wavelength(300000)
        reference_value_300keV = 1.97e-12
        # doesn't work...

    def test_ctf_calculator(self):
        spatial_frequency = np.linspace(0.001, 0.5, 1000)
        ctf = []
        for value in spatial_frequency:
            ctf.append(ABTT.math.ctf.ctf(2.7e-3, 1.97e-12, value, -3e-6))

        print(ctf)
