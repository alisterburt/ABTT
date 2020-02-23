import unittest

import ABTT.fsc.relion


class RelionFSCTest(unittest.TestCase):

    def test_plot(self):
        star_file = 'example_data/fsc/postprocess.star'
        FSC_plotter = ABTT.fsc.relion.Plotter(star_file)
        FSC_plotter.plot()
        self.assertTrue(isinstance(FSC_plotter.fsc_dict, dict))

    def test_cutoff(self):
        star_file = 'example_data/fsc/postprocess.star'
        FSC_plotter = ABTT.fsc.relion.Plotter(star_file)
        FSC_plotter.find_cutoff(0.143)
