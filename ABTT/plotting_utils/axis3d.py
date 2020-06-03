import logging

import matplotlib.pyplot as plt
import numpy as np

from ABTT.math.constants import unit_vectors


def set_axes_equal(ax):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    :param ax: 3D axis
    """
    x_limits, y_limits, z_limits = get_limits(ax)

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

    return None


def instantiate_figure():
    """initialises matplotlib figure and axis with 3d projection"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    return fig, ax


def get_limits(ax):
    """
    gets x, y and z limits of an axis simultaneously
    :param ax:
    :return: x_limits, y_limits, z_limits
    """
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    return x_limits, y_limits, z_limits


def pad_limits(ax, padding_factor):
    """

    :param ax: matplotlib 3d axis
    :param padding_factor: factor by which to increase overall axis size
    :return: None
    """
    x_limits, y_limits, z_limits = get_limits(ax)

    x_range = np.ptp(x_limits)
    y_range = np.ptp(y_limits)
    z_range = np.ptp(z_limits)
    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)

    x_radius = (x_range / 2.0) * padding_factor
    y_radius = (y_range / 2.0) * padding_factor
    z_radius = (z_range / 2.0) * padding_factor

    new_x_limits = (x_middle - x_radius, x_middle + x_radis)
    new_y_limits = (y_middle - y_radius, y_middle + y_radius)
    new_z_limits = (z_middle - z_radius, z_middle + z_radius)

    ax.set_xlim3d(new_x_limits)
    ax.set_ylim3d(new_y_limits)
    ax.set_zlim3d(new_z_limits)

    return None


def scatter3(x, y=None, z=None, m='o', c=None, ax=None):
    """

    :param x:
    :param y:
    :param z:
    :param m:
    :param c:
    :param ax: mpl_toolkits.mplot3d.Axes3d
    :return:
    """

    if np.asarray(x).ndim == 2:
        logging.debug('assuming xyz input given as x')
        xyz = x
        x = xyz[:, 0]
        y = xyz[:, 1]
        z = xyz[:, 2]

    if ax is None:
        fig, ax = instantiate_figure()

    if c is None:
        ax.scatter(x, y, z, marker=m)
    else:
        ax.scatter(x, y, z, c=c, marker=m)

    set_axes_equal(ax)

    return fig, ax


def quiver_em(xyz, rotation_matrices, c=None, axes='xyz', ax=None):
    """

    :param xyz:
    :param rotation_matrices:
    :param c:
    :param rotation_matrices:
    :return:
    """
    u = {}
    v = {}
    w = {}

    n_rows = xyz.shape[0]
    axes = axes.lower()

    for axis in axes:
        for component in (u, v, w):
            component[axis] = np.zeros(n_rows, dtype=float)

    for idx, rotation_matrix in enumerate(rotation_matrices):
        for axis in axes:
            uvw = rotation_matrix @ unit_vectors[axis]
            u[axis][idx] = uvw[0]
            v[axis][idx] = uvw[1]
            w[axis][idx] = uvw[2]

    if ax is None:
        fig, ax = instantiate_figure()

    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]

    arrows = {}
    for axis in axes:
        if c is None:
            p = ax.quiver(x, y, z, u[axis], v[axis], w[axis], normalize=True, length=20)
        else:
            p = ax.quiver(x, y, z, u[axis], v[axis], w[axis], c=c, normalize=True, length=20)

        arrows[axis] = p

    return ax, arrows
