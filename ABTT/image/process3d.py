import numpy as np


def project_z(image):
    """
    Performs a Z projection through a 3D image
    :param image: 3d numpy array of image
    :type image: np.ndarray
    :return: 2d np array of Z projection through 3d image
    """

    z_projection = np.sum(image, axis=0).reshape((image.shape[1], image.shape[2]))
    return z_projection


def project_y(image):
    """
    Performs a Y projection through a 3D image
    :param image: 3d numpy array of image
    :type image: np.ndarray
    :return: 2d np array of Y projection through 3d image
    """

    y_projection = np.sum(image, axis=1).reshape((image.shape[0], image.shape[2]))
    return y_projection


def project_x(image):
    """
    Performs an X projection through a 3D image
    :param image: 3d numpy array of image
    :type image: np.ndarray
    :return: 2d np array of X projection through 3d image
    """

    x_projection = np.sum(image, axis=2).reshape((image.shape[0], image.shape[1]))
    return x_projection
