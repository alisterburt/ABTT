def fpix2res(fourier_pixel_extent, angstroms_per_pixel, box_size):
    """
    Convert extent of signal into fourier space into a resolution value
    :param fourier_pixel_extent: the fourier pixel extent which you would like to convert into a resolution value
    :param angstroms_per_pixel: pixel size in angstroms
    :param box_size: box size of particle
    :return: resolution_angstroms
    """
    fraction_of_nyquist = float(fourier_pixel_extent) / (0.5 * box_size)
    nyquist_frequency_angstroms = 1.0 / (2.0 * float(angstroms_per_pixel))
    spatial_frequency_angstroms = fraction_of_nyquist * nyquist_frequency_angstroms
    resolution_angstroms = 1.0 / spatial_frequency_angstroms

    return resolution_angstroms


def res2fpix(resolution_angstroms, angstroms_per_pixel, box_size):
    """
    Convert a resolution in angstroms into the distance from the origin in fourier space for a given sampling rate
    and box size
    :param resolution_angstroms: resolution that you would like to convert into fpix extent
    :param angstroms_per_pixel: pixel size in angstroms
    :param box_size: box size of particle
    :return:
    """
    spatial_frequency_angstroms = 1.0 / float(resolution_angstroms)
    nyquist_frequency_angstroms = 1.0 / (2.0 * float(angstroms_per_pixel))
    fraction_of_nyquist = spatial_frequency_angstroms / nyquist_frequency_angstroms
    fourier_pixel_extent = fraction_of_nyquist * (0.5 * box_size)

    return fourier_pixel_extent


def cpix2res(cycles_per_pixel, angstroms_per_pixel):
    """
    Convert a resolution given in terms of cycles per pixel into a resolution in angstroms
    :param cycles_per_pixel: how many cycles of a signal do you represent with one pixel? max 0.5
    :param angstroms_per_pixel: pixel size in angstroms
    :return: resolution_angstroms
    """
    fraction_of_nyquist = float(cycles_per_pixel) / 0.5
    nyquist_frequency = 1.0 / float(angstroms_per_pixel)
    spatial_frequency_angstroms = fraction_of_nyquist * nyquist_frequency
    resolution_angstroms = 1.0 / spatial_frequency_angstroms

    return resolution_angstroms


def res2cpix(resolution_angstroms, angstroms_per_pixel):
    """
    Convert a given resolution in angstroms into it's cycles per pixel value at a given pixel size
    :param resolution_angstroms: resolution in angstroms
    :param angstroms_per_pixel: pixel size in angstroms
    :return: cycles_per_pixel
    """
    nyquist_frequency = 1.0 / (2.0 * float(angstroms_per_pixel))
    spatial_frequency_angstroms = 1.0 / float(resolution_angstroms)
    fraction_of_nyquist = spatial_frequency_angstroms / nyquist_frequency
    cycles_per_pixel = fraction_of_nyquist * 0.5

    return cycles_per_pixel
