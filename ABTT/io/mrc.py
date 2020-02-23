import logging

import mrcfile
import numpy as np


def header(mrc_file):
    """
    Reads the header of an mrc file
    :param mrc_file: path to mrc file
    :return: header of mrc file
    """
    logging.info(f'reading mrc file header: {mrc_file}')
    with mrcfile.open(mrc_file, 'r', permissive=True, header_only=True) as mrc:
        return mrc.header


def data(mrc_file):
    """
    reads the data of an mrc file
    :param mrc_file:
    :return:
    """
    logging.info(f'reading mrc file data: {mrc_file}')
    with mrcfile.open(mrc_file, 'r', permissive=True) as mrc:
        return mrc.data


def size(mrc_file):
    """
    returns a tuple (NX, NY, NZ) for an mrc file from the header
    :param mrc_File: path to mrc file
    :return: (NX, NY, NZ)
    """
    header_object = header(mrc_file)
    size = (header_object.nx, header_object.ny, header_object.nz)

    return size


def make_test_2d(mrc_file):
    """
    creates a test mrc image 32x32
    :param mrc_file: file in which to write image
    :return: mrc file object
    """
    with mrcfile.new(mrc_file, overwrite=True) as mrc:
        mrc.set_data(np.zeros((32,32), dtype=np.int8))
        mrc.data[10:22,10:22] = 1
        return mrc


def make_test_3d(mrc_file):
    """
    creates a test mrc image 32x32x32
    :param mrc_file: file in which to write image
    :return: mrc file object
    """
    with mrcfile.new(mrc_file, overwrite=True) as mrc:
        mrc.set_data(np.zeros((32,32,32), dtype=np.int8))
        mrc.data[10:22,10:22,:] = 1
        return mrc


def is_cube(mrc_file):
    """
    checks if mrc_file is a cubic volume (header only)
    :param mrc_file: mrc file to check
    :return:
    """
    (nx, ny, nz) = size(mrc_file)
    cubic = nx == ny == nz
    return cubic


def voxel_size(mrc_file):
    """
    reads voxel size from mrc file header
    :param mrc_file: mrc file to check
    :return: np.recarray [x,y,z]
    """
    with mrcfile.open(mrc_file, 'r', permissive=True, header_only=True) as mrc:
        voxel_size = mrc.voxel_size
    return voxel_size
