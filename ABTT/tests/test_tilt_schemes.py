import unittest

import ABTT.tilt_scheme


class TiltSchemeTest(unittest.TestCase):

    def test_tilt_scheme_dose_symmetric(self):
        tilt_scheme = ABTT.tilt_scheme.tilt_scheme.TiltScheme()
        tilt_scheme.angles_dose_symmetric(60, 3)
        tilt_scheme.sort_angles()
        tilt_scheme.lines()
        tilt_scheme.plot_lines(cmap='Blues_r')

    def test_tilt_scheme_continuous(self):
        tilt_scheme = ABTT.tilt_scheme.tilt_scheme.TiltScheme()
        tilt_scheme.angles_continuous(-60, 60, 3)
        tilt_scheme.sort_angles()
        tilt_scheme.lines()
        tilt_scheme.plot_lines(cmap='Blues_r')

    def test_tilt_scheme_bidirectional(self):
        tilt_scheme = ABTT.tilt_scheme.tilt_scheme.TiltScheme()
        tilt_scheme.angles_bidirectional(60, 3)
        tilt_scheme.sort_angles()
        tilt_scheme.lines()
        tilt_scheme.plot_lines(cmap='Blues_r')
