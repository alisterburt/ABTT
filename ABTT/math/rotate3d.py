import numpy as np


# These rotation matrices all define passive rotations, i.e. axes turn whilst points remain stationary

def rotate_x(theta):
    """
    calculates the rotation matrix for a passive anticlockwise rotation around the x axis
    by the angle theta
    :param theta: angle about which to rotate x axis (degrees)
    :return: rotation_matrix
    """
    theta_radians = np.deg2rad(theta)
    sin_theta = np.sin(theta_radians)
    cos_theta = np.cos(theta_radians)

    rotation_matrix = np.array([[1, 0, 0],
                                [0, cos_theta, -sin_theta],
                                [0, sin_theta, cos_theta]],
                               dtype=np.float)

    return rotation_matrix


def rotate_y(theta):
    """
    calculates the rotation matrix for a passive anticlockwise rotation around the y axis
    by the angle theta
    :param theta: angle about which to rotate y axis (degrees)
    :return: rotation_matrix
    """
    theta_radians = np.deg2rad(theta)
    sin_theta = np.sin(theta_radians)
    cos_theta = np.cos(theta_radians)

    rotation_matrix = np.array([[cos_theta, 0, sin_theta],
                                [0, 1, 0],
                                [-sin_theta, 0, cos_theta]],
                               dtype=np.float)

    return rotation_matrix


def rotate_z(theta):
    """
    calculates the rotation matrix for a passive anticlockwise rotation around the z axis
    by the angle theta
    :param theta: angle about which to rotate x axis (degrees)
    :return: rotation_matrix
    """
    theta_radians = np.deg2rad(theta)
    sin_theta = np.sin(theta_radians)
    cos_theta = np.cos(theta_radians)

    rotation_matrix = np.array([[cos_theta, -sin_theta, 0],
                                [sin_theta, cos_theta, 0],
                                [0, 0, 1]],
                               dtype=np.float)

    return rotation_matrix

