import logging

import numpy as np

from . import rotate3d


def relion():
    """
    Euler angle axes for relion
    Euler angle definitions are according to the Heymann, Chagoyen and Belnap (2005) standard:

    * The first rotation is denoted by phi or rot and is around the Z-axis.
    * The second rotation is called theta or tilt and is around the new Y-axis.
    * The third rotation is denoted by psi and is around the new Z axis

    As such, RELION uses the same Euler angles as XMIPP, SPIDER and FREALIGN.

    Positive is anti-clockwise looking at origin, clockwise looking along axis
    :return: axes, reference_frame
    """
    axes = 'ZYZ'
    reference_frame = 'rotate_reference'
    return axes, reference_frame


def dynamo():
    """
    Euler angle axes for Dynamo subtomogram averaging software. Dynamo uses a ZXZ axes to express the
    rotation in terms of Euler angles. A triplet of Euler angles is read with the colourful names [tdrot, tilt,
    narot], with the following visual depiction: imagine a particle with an axis aligned with the z direction.
    The action of the triplet of angles of this particle would be like this.

    tdrot (for tilt direction gets rotated)

    The particle rotates clockwise about its z axis.

    tilt

    the particle rotates clockwise about its new x axis.

    narot (for new azymuthal rotation)

    the particle rotates clockwise about its new z axis.

    In the context of subtomogram averaging, they are understood as the rotation that we need to operate on the
    template in order to align it with the particle. Note that the inverse rotation would be parametrized as -[
    narot, tilt, tdrot], i.e., applying the inverse of each original rotation, in reversed order.

    Positive is anti-clockwise looking at origin, clockwise looking along axis
    :return: axes, reference_frame
    """
    axes = 'ZXZ'
    reference_frame = 'rotate_particle'
    return axes, reference_frame


def emclarity():
    """
    The angles input to emClarity describe ZXZ active intrinsic rotations of the particles coordinate system. That is
    to say, the basis vectors describing the average particle in the microscope reference frame are rotated (positive
    anti-clockwise) around Z, the new X, and the new Z axis. The final transformation describes the coordinate system
    attached to any given particle in your data set.
    :return: axes, reference_frame
    """
    axes = 'ZXZ'
    reference_frame = 'rotate_particle'
    return axes, reference_frame


def xmipp():
    return relion()


def frealign():
    return relion()


class AngleConvert:
    """
    An object for conversion of euler angles between different conventions of different software packages
    Explanations and notation will be in the context of cryo-electron microscopy software
    Conventions are defined by two parameters:
    :param axes: str 'ZYZ' or similar
    :param reference_frame: 'rotate_reference' or 'rotate_particle'
                            In the context of single particle analysis, euler angles define the rotation of a reference
                            volume before projection, the projection is then compared with an experimental image.

                            In the context of subtomogram averaging, euler angles can either describe the rotation of a
                            reference volume or of a 3D particle (subtomogram) before comparison of the reference volume
                            with the subtomogram.
    """

    def __init__(self, euler_angles, axes=None, reference_frame=None, software=None):
        """

        :param euler_angles: [N,3] numpy array of euler angles given in degrees
        :param axes: str of axes in order of application of rotation, e.g. 'XYZ' for X then Y then Z
        :param reference_frame: 'rotate_reference' or 'rotate_particle'
                                In the context of single particle analysis, euler angles define the rotation of a reference
                                volume before projection, the projection is then compared with an experimental image.

                                In the context of subtomogram averaging, euler angles can either describe the rotation of a
                                reference volume or of a 3D particle (subtomogram) before comparison of the reference volume
                                with the subtomogram.
        :param software: software package from which these euler angles came
        """
        logging.info('instantiated an AngleConvert object for euler angle manipulation')

        self.euler_angle_conventions = {'relion': relion(),
                                        'dynamo': dynamo(),
                                        'emclarity': emclarity(),
                                        'xmipp': xmipp(),
                                        'frealign': frealign()}
        if software is not None:
            logging.debug("using 'software' flag to set axis and reference frame conventions")
            axes, reference_frame = euler_angle_conventions[software.lower]
            self.axes = axes
            self.reference_frame = reference_frame
        else:
            self.axes = axes.upper()
            self.reference_frame = reference_frame.lower()

        self.euler_angles = np.asarray(euler_angles, dtype=np.float)
        self.rotation_matrices = self.calculate_rotation_matrices()

    def calculate_rotation_matrices(self):
        logging.debug('calculating rotation matrices from euler angles')
        # Set up empty array for storage of rotation matrices
        n_rows = self.data.shape[0]
        rotation_matrices = np.empty((n_rows, 3, 3), dtype=np.float)

        # Calculate rotation matrix for each euler triplet
        for idx, euler_triplet in enumerate(self.euler_angles):
            rotation_matrices[idx, :, :] = calculate_rotation_matrix(euler_triplet, euler_angle_axes=self.axes)

        # Store/return
        self.rotation_matrices = rotation_matrices
        return self.rotation_matrices

    def transpose_rotation_matrices(self):
        logging.debug("""transposing (N,3,3) matrix to give (N,3,3) matrix where each 3,3 matrix is the transpose of
                      the original""")
        rotation_matrices_transposed = np.transpose(self.rotation_matrices, (0, 2, 1))
        self.rotation_matrices = rotation_matrices_transposed

    def angles_from_rotation_matrices(self, target_axes_convention):
        logging.debug(f'calculating {target_axes_convention} euler angles from stored rotation matrices')
        n_rows = self.rotation_matrices.shape[0]
        euler_angles = np.empty((n_rows, 3))

        for idx, rotation_matrix in self.rotation_matrices:
            if target_axes_convention.upper() = 'ZXZ':
                euler_angles[idx] = matrix2ZXZeuler(rotation_matrix)
            elif target_axes_convention.upper() = 'ZYZ':
                euler_angles[idx] = matrix2ZYZeuler(rotation_matrix)
            else:
                logging.warning(f'conversion for {target_axes_convention} not yet supported!')
        return euler_angles

    def change_reference_frame(self):
        logging.debug('changing reference frame of rotation matrices by transposition, also updating euler angles.')
        self.transpose_rotation_matrices()
        self.angles_from_rotation_matrices()
        if self.reference_frame.lower() == 'rotate_particle':
            self.reference_frame = 'rotate_reference'

        elif self.reference_frame.lower() == 'rotate_reference':
            self.reference_frame = 'rotate_particle'

    def change_axes(self, target_axes_convention):
        """

        :param target_axes_convention:
        :return:
        """
        logging.debug(f'changing axis convention from {self.axes} to {target_axes_convention}')
        euler_angles = self.angles_from_rotation_matrices(target_axes_convention)
        self.euler_angles = euler_angles
        self.axes = target_axes_convention.upper()

    def to_software(self, software_name):

        target_axes, target_reference_frame = self.euler_angle_conventions[software_name.lower()]
        message = f'converting euler angles from {self.axes} : {self.reference_frame} to {target_axes} : {target_reference_frame}'
        logging.info(message)
        if self.reference_frame == target_reference_frame:
            self.change_reference_frame()

        if self.axes == target_axes:
            self.change_axes(target_axes)

        return self.euler_angles


# General functions
def calculate_rotation_matrix(euler_triplet, euler_angle_axes):
    """
    :param euler_triplet: 3 element vector defining three euler angles, in degrees
    :param euler_angle_axes: str of format 'XYZ' or similar for rotation about X, Y, then Z
    :return: [3,3] rotation matrix for rotation given by R=RZ*RY*RX
    """
    # Store rotation matrices, first matrix is first rotation (e.g. X for 'XYZ')
    rotation_matrices = []
    for idx, axis in enumerate(euler_angle_axes.upper()):
        euler_angle = euler_triplet[idx]
        if axis == 'X':
            rotation_matrix = rotate3d.rotate_x(euler_angle)
        elif axis == 'Y':
            rotation_matrix = rotate3d.rotate_y(euler_angle)
        elif axis == 'Z':
            rotation_matrix = rotate3d.rotate_z(euler_angle)
        rotation_matrices.append(rotation_matrix)

    rotation_matrix_final = np.matmul(np.matmul(rotation_matrices[2], rotation_matrices[1]), rotation_matrices[0])

    return rotation_matrix_final


def matrix2ZXZeuler(rotation_matrix):
    """
    Converts rotation matrix ([3,3] numpy array) into ZXZ euler angles (in degrees)
    :param rotation_matrix: [3,3] numpy array
    :return: [3] element vector containing euler angles in degrees
    """
    # Set a tolerance because of indetermination in defining narot and tdrot
    tolerance = 1e-4

    # Check special cases
    # rm(3,3) = +1
    if np.absolute(rotation_matrix[2, 2] - 1) < tolerance:
        tdrot = 0
        tilt = 0
        narot = np.rad2deg(np.arctan2(rotation_matrix[1, 0], rotation_matrix[2, 2]))

        ZXZeuler = np.array([tdrot, tilt, narot])
        return ZXZeuler


    # rm(3,3) = -1
    elif np.absolute(rotation_matrix[2, 2] + 1) < tolerance:
        tdrot = 0
        tilt = 180
        narot = np.rad2deg(np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0]))

        ZXZeuler = np.array([tdrot, tilt, narot])
        return ZXZeuler

    # general case
    else:
        tdrot = np.rad2deg(np.arctan2(rotation_matrix[2, 0], rotation_matrix[2, 1]))
        tilt = np.rad2deg(np.arccos(rotation_matrix[2, 2]))
        narot = np.rad2deg(np.arctan2(rotation_matrix[0, 2], -rotation_matrix[1, 2]))

        ZXZeuler = np.array([tdrot, tilt, narot], dtype=np.float)
        return ZXZeuler


def matrix2ZYZeuler(rotation_matrix):
    # Set a tolerance because of indetermination in defining narot and tdrot
    tolerance = 1e-4

    # Check special cases
    # rm(3,3) = -1
    # rm(3,3) = cos(b) = -1
    # cos-1(rm(3,3)) = b = pi/2
    # sin(b) = sin(pi/2) = 1

    # [-cos(c)cos(a)-sin(a)    cos(c)sin(a)-sin(c)cos(a) cos(c)]
    # [-sin(c)cos(a)+cos(c)sin(a)    sin(c)sin(a)+cos(c)cos(a) sin(c)]
    # [-sin(b)cos(a)                      sin(a)             -1      ]

    # R(1,1) = -cos(c)cos(a)-1*(sin(a)
    # R(1,2) = sin(a)cos(c)-cos(a)sin(c) = sin(a-c)
    # R(2,1) = sin(a)cos(c)-cos(a)sin(c) = sin(a-c)
    # R(2,2) = sin(c)sin(a)+cos(c)cos(a) = cos(c-a)
    if np.absolute(rotation_matrix[2, 2] + 1) < tolerance:
        tdrot = -np.arctan2(rotation_matrix[1, 0], rotation_matrix[1, 1])
        tilt = 180
        narot = 0


    elif np.absolute(rotation_matrix[2, 2] - 1) < tolerance:
        tdrot = np.arctan2(rotation_matrix[1, 0], rotation_matrix[1, 1])
        tilt = 0
        narot = 0


    # general case
    else:
        tdrot = np.rad2deg(np.arctan2(rotation_matrix[2, 1], -rotation_matrix[2, 0]))
        tilt = np.rad2deg(np.arccos(rotation_matrix[2, 2]))
        narot = np.rad2deg(np.arctan2(rotation_matrix[1, 2], rotation_matrix[0, 2]))

    ZYZeuler = np.array([tdrot, tilt, narot], dtype=np.float)

    return ZYZeuler

# def matrix2XYZeuler(rotation_matrix):
#
# def matrix2
