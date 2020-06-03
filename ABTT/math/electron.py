from math import sqrt


def relativistic_wavelength(accelerating_voltage_v):
    """
    Calculate electron wavelength as function of acceleration voltage
    Takes into account relativistic effects
    Equation taken from "High Resolution Electron Microscopy (2012) J. Spence"
    :param accelerating_voltage_v:
    :return:
    """
    v = accelerating_voltage_v
    electron_wavelength_nm = 1.22639 / sqrt(v + 0.97845e-6 * v ** 2)
    electron_wavelength_m = electron_wavelength_nm / 1e9
    return electron_wavelength_m
