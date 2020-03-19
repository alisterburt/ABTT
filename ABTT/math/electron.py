from math import sqrt

from .constants import (plancks_constant,
                        rest_energy_electron,
                        elementary_charge,
                        speed_of_light)


# Figure out why this doesn't work...
def relativistic_wavelength(accelerating_voltage_v):
    """
    Calculate electron wavelength as function of acceleration voltage
    Takes into account relativistic effects
    :param accelerating_voltage_v:
    :return:
    """
    charge_of_electron = elementary_charge
    E0 = rest_energy_electron
    c = speed_of_light
    h = plancks_constant
    v = accelerating_voltage_v

    numerator = h * c
    denominator = sqrt(((2 * E0 * v) + (v * v)) * charge_of_electron * charge_of_electron)

    electron_wavelength = numerator / denominator
    return electron_wavelength
