import numpy as np


def ctf(spherical_abberation, amplitude_contrast, relativistic_lambda, spatial_frequency, defocus):
    """
    Gets 1D ctf using equation from Zhang et al. GCTF paper
    :param spherical_abberation:
    :param amplitude_contrast:
    :param relativistic_lambda:
    :param spatial_frequency:
    :param defocus:
    :return:
    """
    gamma = (((-np.pi / 2) * spherical_abberation * np.power(relativistic_lambda, 3) * np.power(spatial_frequency, 4))
             + (np.pi * relativistic_lambda * defocus * np.power(spatial_frequency, 2)))
    CTF = - np.sqrt(1 - np.power(amplitude_contrast, 2))
