import numpy as np
from ABTT.math import


class TiltScheme:
    """Generate and plot tilt schemes"""
    def __init__(self):

    def angles_continuous(self, min_angle, max_angle, angular_increment):
        angles = list(range(min_angle, max_angle+angular_increment, angular_increment))
        self.angles = angles
        self.angles_order = list(range(1, len(angles)+1, 1))
        return angles

    def angles_dose_symmetric(self, max_angle, angular_increment):
        angles = np.array(list(range(-max_angle, max_angle+angular_increment, angular_increment)))
        order_tmp = np.array(list(range(1, len(angles)+1, 1)))
        order = np.zeros_like(angles)
        middle_index = np.floor(len(angles / 2.0))
        order[middle_index:] = order_tmp[::2]
        order[:middle_index] = order_tmp[-1::2]



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
