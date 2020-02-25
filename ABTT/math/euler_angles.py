import logging

import numpy as np

from . import rotate3d


class Conventions:
    """Known euler angle conventions for cryo-EM software"""

    def __init__(self):
        self.dynamo = self.dynamo()
        self.relion = self.relion()
        self.emclarity = self.emclarity()

    def relion(self):
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
        intrinsic = False  # heuristic, haven't looked at their code but this gives good reconstructions
        extrinsic = True
        return axes, reference_frame, intrinsic, extrinsic

    def dynamo(self):
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
        reference_frame = 'rotate_reference'
        intrinsic = True
        extrinsic = False
        return axes, reference_frame, intrinsic, extrinsic

    def emclarity(self):
        """
        The angles input to emClarity describe ZXZ active intrinsic rotations of the particles coordinate system. That is
        to say, the basis vectors describing the average particle in the microscope reference frame are rotated (positive
        anti-clockwise) around Z, the new X, and the new Z axis. The final transformation describes the coordinate system
        attached to any given particle in your data set.
        :return: axes, reference_frame
        """
        axes = 'ZXZ'
        reference_frame = 'rotate_particle'
        intrinsic = True
        extrinsic = False
        return axes, reference_frame, intrinsic, extrinsic



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

    def __init__(self, euler_angles, axes=None, reference_frame=None, intrinsic=True, extrinsic=None,
                 from_software=None,
                 target_software=None):
        """
        :param euler_angles: [N,3] numpy array of euler angles given in degrees
        :param axes: str of axes in order of application of rotation, e.g. 'XYZ' for X then Y then Z
        :param reference_frame: 'rotate_reference' or 'rotate_particle'
                                In the context of single particle analysis, euler angles define the rotation of a reference
                                volume before projection, the projection is then compared with an experimental image.

                                In the context of subtomogram averaging, euler angles can either describe the rotation of a
                                reference volume or of a 3D particle (subtomogram) before comparison of the reference volume
                                with the subtomogram.
        :param from_software: software package from which these euler angles came
        """
        logging.info('instantiated an AngleConvert object for euler angle manipulation')
        angle_conventions = Conventions()
        self.euler_angle_conventions = {'relion': angle_conventions.relion(),
                                        'dynamo': angle_conventions.dynamo(),
                                        'emclarity': angle_conventions.emclarity(),
                                        }

        if from_software is not None:
            logging.debug("using 'software' flag to set axis and reference frame conventions")
            axes, reference_frame, intrinsic, extrinsic = self.euler_angle_conventions[from_software.lower()]
            self.axes = axes
            self.reference_frame = reference_frame
            self.intrinsic = intrinsic
            self.extrinsic = extrinsic

        else:
            self.axes = axes.upper()
            self.reference_frame = reference_frame.lower()
            self.intrinsic = intrinsic
            if extrinsic is None:
                self.extrinsic = not self.intrinsic
            else:
                self.extrinsic = extrinsic
                self.intrinsic = not extrinsic

        self.euler_angles = np.asarray(euler_angles, dtype=np.float)
        self.rotation_matrices = self.calculate_rotation_matrices()

        if target_software is not None:
            logging.debug(f'trying to convert given angles to {from_software} format')
            self.to_software(target_software)

    def calculate_rotation_matrices(self):
        logging.debug('calculating rotation matrices from euler angles')
        # Set up empty array for storage of rotation matrices
        n_rows = self.euler_angles.shape[0]
        rotation_matrices = np.empty((n_rows, 3, 3), dtype=np.float)

        # Calculate rotation matrix for each euler triplet
        for idx, euler_triplet in enumerate(self.euler_angles):
            rotation_matrices[idx, :, :] = calculate_rotation_matrix(euler_triplet,
                                                                     euler_angle_axes=self.axes,
                                                                     intrinsic=self.intrinsic,
                                                                     extrinsic=self.extrinsic)

        # Store/return
        self.rotation_matrices = rotation_matrices
        return self.rotation_matrices

    def transpose_rotation_matrices(self):
        logging.debug("""transposing (N,3,3) matrix to give (N,3,3) matrix where each 3,3 matrix is the transpose of
                      the original""")
        rotation_matrices_transposed = np.transpose(self.rotation_matrices, (0, 2, 1))
        self.rotation_matrices = rotation_matrices_transposed

    def angles_from_rotation_matrices(self, target_axes_convention, intrinsic=True, extrinsic=None):
        logging.debug(f'calculating {target_axes_convention} euler angles from stored rotation matrices')
        n_rows = self.rotation_matrices.shape[0]
        euler_angles = np.empty((n_rows, 3))

        for idx, rotation_matrix in enumerate(self.rotation_matrices):
            if target_axes_convention.upper() == 'ZXZ':
                euler_angles[idx] = matrix2ZXZeuler(rotation_matrix,
                                                    intrinsic=intrinsic,
                                                    extrinsic=extrinsic)

            elif target_axes_convention.upper() == 'ZYZ':
                euler_angles[idx] = matrix2ZYZeuler(rotation_matrix,
                                                    intrinsic=intrinsic,
                                                    extrinsic=extrinsic)
            else:
                logging.warning(f'conversion for {target_axes_convention} not yet supported!')
        return euler_angles

    def change_reference_frame(self):
        logging.debug('changing reference frame of rotation matrices by transposition, also updating euler angles.')
        self.transpose_rotation_matrices()
        self.angles_from_rotation_matrices(self.axes)
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

        (target_axes,
         target_reference_frame,
         target_intrinsic,
         target_extrinsic) = self.euler_angle_conventions[software_name.lower()]
        message = f'converting euler angles from {self.axes} : {self.reference_frame} to {target_axes} : {target_reference_frame}'
        logging.info(message)
        if self.reference_frame != target_reference_frame:
            self.change_reference_frame()

        if self.intrinsic != target_intrinsic or self.extrinsic != target_extrinsic:
            self.calculate_rotation_matrices()
            self.angles_from_rotation_matrices(target_axes, target_intrinsic, target_extrinsic)

        if self.axes != target_axes:
            self.change_axes(target_axes)

        return self.euler_angles


# General functions
def calculate_rotation_matrix(euler_triplet, euler_angle_axes, intrinsic=True, extrinsic=None):
    """
    :param euler_triplet: 3 element vector defining three euler angles, in degrees
    :param euler_angle_axes: str of format 'XYZ' or similar for rotation about X, Y, then Z
    :return: [3,3] rotation matrix for rotation given by R=RZ*RY*RX
    """
    logging.debug('calculating rotation matrix from euler triplet')
    # Check that intrinsic and extrinsic are not the same
    if extrinsic and intrinsic:
        intrinsic = False
        logging.debug('extrinsic rotation was explicitly set to True so performing extrinsic rotations')

    elif extrinsic == None and intrinsic:
        extrinsic = False
        logging.debug('defaulting to intrinsic rotations')

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
        else:
            logging.debug(f'axis {axis} not XYZ so not supported')

        if rotation_matrix is not None:
            rotation_matrices.append(rotation_matrix)

    if intrinsic and not extrinsic:
        rotation_matrix_final = rotation_matrices[2] @ rotation_matrices[1] @ rotation_matrices[0]

    if extrinsic and not intrinsic:
        rotation_matrix_final = rotation_matrices[0] @ rotation_matrices[1] @ rotation_matrices[2]

    return rotation_matrix_final


def matrix2ZXZeuler(rotation_matrix, intrinsic=True, extrinsic=None):
    """
    Converts rotation matrix ([3,3] numpy array) into ZXZ euler angles (in degrees)
    :param rotation_matrix: [3,3] numpy array
    :return: [3] element vector containing euler angles in degrees
    """
    logging.debug('calculating ZXZ euler angles from rotation matrix')
    if intrinsic and extrinsic is None:
        extrinsic = False
        logging.debug('ZXZ euler angles output will be intrinsic, i.e. rotations of axes not points')

    if extrinsic and intrinsic:
        intrinsic = False
        logging.debug('ZXZ euler angles output will be extrinsic, i.e. rotations of points not axes')

    # Set a tolerance because of indetermination in defining narot and tdrot
    tolerance = 1e-4

    # Check special cases
    # rm(3,3) = +1
    if np.absolute(rotation_matrix[2, 2] - 1) < tolerance:
        tdrot = 0
        tilt = 0
        narot = np.rad2deg(np.arctan2(rotation_matrix[1, 0], rotation_matrix[2, 2]))

    # rm(3,3) = -1
    elif np.absolute(rotation_matrix[2, 2] + 1) < tolerance:
        tdrot = 0
        tilt = 180
        narot = np.rad2deg(np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0]))

    # general case
    else:
        tdrot = np.rad2deg(np.arctan2(rotation_matrix[2, 0], rotation_matrix[2, 1]))
        tilt = np.rad2deg(np.arccos(rotation_matrix[2, 2]))
        narot = np.rad2deg(np.arctan2(rotation_matrix[0, 2], -rotation_matrix[1, 2]))

    if intrinsic and not extrinsic:
        ZXZeuler = np.array([tdrot, tilt, narot], dtype=np.float)

    elif extrinsic and not intrinsic:
        ZXZeuler = np.array([narot, tilt, tdrot], dtype=np.float)

    return ZXZeuler


def matrix2ZYZeuler(rotation_matrix, intrinsic=True, extrinsic=None):
    logging.debug('calculating ZYZ euler angles from ZYZ euler angles')
    if intrinsic and extrinsic is None:
        extrinsic = False
        logging.debug('ZYZ euler angles output will be intrinsic, i.e. rotations of axes not points')

    if extrinsic and intrinsic:
        intrinsic = False
        logging.debug('ZYZ euler angles output will be extrinsic, i.e. rotations of points not axes')


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

    if intrinsic and not extrinsic:
        ZYZeuler = np.array([tdrot, tilt, narot], dtype=np.float)

    elif extrinsic and not intrinsic:
        ZYZeuler = np.array([narot, tilt, tdrot], dtype=np.float)

    return ZYZeuler

# def matrix2XYZeuler(rotation_matrix):
#
# def matrix2

