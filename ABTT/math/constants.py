import numpy as np

# useful physical constants
mass_of_electron = 9.1093837015e-31  # kg
rest_energy_electron = 510999  # eV
elementary_charge = 1.60217662e-19  # C
plancks_constant = 6.62607004e-34  # m2 kg s-1
speed_of_light = 299792458  # m s-1

# unit vectors as column vectors
unit_x = np.asarray([1, 0, 0], dtype=float).transpose()
unit_y = np.asarray([0, 1, 0], dtype=float).transpose()
unit_z = np.asarray([0, 0, 1], dtype=float).transpose()

unit_vectors = {}
unit_vectors['x'] = unit_x
unit_vectors['y'] = unit_y
unit_vectors['z'] = unit_z
