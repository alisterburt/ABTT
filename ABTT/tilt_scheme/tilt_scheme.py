import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

from ABTT.math import rotate3d


class TiltScheme:
    """Generate and plot tilt schemes"""
    def __init__(self):
        return None

    def angles_continuous(self, min_angle, max_angle, angular_increment):
        angles = np.array(list(range(min_angle, max_angle + angular_increment, angular_increment)))
        self.angles = angles
        self.angles_order = np.array(list(range(len(angles))))
        return angles

    def angles_dose_symmetric(self, max_angle, angular_increment):
        angles = np.array(list(range(-max_angle, max_angle+angular_increment, angular_increment)))
        order_tmp = np.array(list(range(1, len(angles)+1, 1)))
        order = np.zeros_like(angles)
        middle_index = int(np.floor(angles.shape[0] / 2.0))

        order[middle_index + 1:] = order_tmp[:-1:2]
        order[middle_index - 1::-1] = order_tmp[1:-1:2]
        self.angles = angles
        self.angles_order = order

    def angles_bidirectional(self, max_angle, angular_increment):
        angles = np.array(list(range(-max_angle, max_angle + angular_increment, angular_increment)))
        order_tmp = np.array(list(range(1, len(angles) + 1, 1)))
        order = np.zeros_like(angles)
        middle_index = int(np.floor(angles.shape[0] / 2.0))

        order[middle_index + 1:] = order_tmp[:middle_index]
        order[middle_index - 1::-1] = order_tmp[middle_index:-1]

        self.angles = angles
        self.angles_order = order

    def sort_angles(self, reverse=False):
        idx = np.argsort(self.angles_order)
        if reverse:
            idx = idx[::-1]
        self.angles_order = self.angles_order[idx]
        self.angles = self.angles[idx]

    def lines(self):
        lines = []
        for angle in self.angles:
            lines.append(rotate_line(-angle))

        self.lines = lines

    def planes(self):
        planes = []
        for angle in self.angles:
            planes.append(rotate_plane_y(angle))

        self.planes = planes

    def plot_lines(self, ax=None, cmap='Spectral', cbar=False):
        if ax is None:
            fig, ax = plt.subplots()
            fig.set_size_inches((8, 6))
        else:
            fig = ax.get_figure()

        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)

        ax.axis('off')

        line_segments = LineCollection(self.lines,
                                       linewidths=4,
                                       linestyles='solid',
                                       array=self.angles_order,
                                       cmap=cmap,
                                       alpha=1)

        ax.add_collection(line_segments)
        ax.axis('equal')
        if cbar:
            axcb = fig.colorbar(line_segments, ticks=[0, max(self.angles_order)])
            axcb.ax.set_yticklabels(['First Tilt', 'Last Tilt'])


def rotate_line(tilt_angle):
    """
    Calculates new positions of a line from -1 to 1 on the x-axis after rotation by tilt_angle
    """
    line = np.array([[-1, 0], [1, 0]], dtype=np.float16)
    t = np.deg2rad(tilt_angle)
    rotation_matrix = np.array([[np.cos(t), -1 * np.sin(t)], [np.sin(t), np.cos(t)]])

    output_points = np.empty_like(line)
    for idx, xy in enumerate(line):
        xy = np.transpose(xy)
        output_points[idx] = np.matmul(rotation_matrix, xy)

    return output_points

def rotate_plane_y(tilt_angle):
    """
    Calculates new positions of a plane (z = 0, x and y extent -1,1) after rotation around the y-axis by tilt angle
    :param tilt_angle: angle by which to rotate plane
    :return:
    """
    plane = np.array([[-1, -1, 0],
                      [-1, 1, 0],
                      [1, -1, 0],
                      [1, 1, 0]])

    rotation_matrix = rotate3d.rotate_y(tilt_angle)

    output_plane = np.empty_like(plane)
    for idx, xyz in enumerate(plane):
        xyz = np.transpose(xyz)
        output_plane[idx] = np.matmul(rotation_matrix, xyz)

    return output_plane
