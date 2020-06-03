import numpy as np


def ctf1d(spherical_abberation, amplitude_contrast, relativistic_lambda, spatial_frequency, defocus, B_factor=None):
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
    ctf = - (np.sqrt(1 - np.power(amplitude_contrast, 2)) * np.sin(gamma)) - (amplitude_contrast * np.cos(gamma))

    if B_factor is not None:
        envelope = envelope_function(B_factor, spatial_frequency)
        ctf *= envelope
    return ctf


def envelope_function(B_factor, spatial_frequency):
    """
    Generalised B-factor from J. Frank, 2006
    :param B-factor: units: squared distance
    :param spatial_frequency: spatial frequency
    :return: envelope function
    """
    envelope = np.exp(-1 * B_factor * np.power(spatial_frequency, 2))
    return envelope
