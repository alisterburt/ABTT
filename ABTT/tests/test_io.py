import unittest
import os

import numpy as np

import ABTT.io


class StarDictTest(unittest.TestCase):

    def test_headings(self):
        star_file = 'example_data/example.star'
        star_dict = ABTT.io.star.read(star_file)
        headings = star_dict.headings()
        self.assertTrue(isinstance(headings, list))
        self.assertTrue('#' not in headings[0])

    def test_header(self):
        star_file = 'example_data/example.star'
        star_dict = ABTT.io.star.read(star_file)
        header = star_dict.loopheader()
        self.assertTrue('data_\n' in header)
        self.assertTrue('loop_\n' in header)

    def test_write(self):
        star_file = 'example_data/example.star'
        star_dict = ABTT.io.star.read(star_file)
        out_file = 'example_data/example_rewrite.star'
        star_dict.write(out_file)


class MrcTest(unittest.TestCase):

    def test_make_test_2d(self):
        file = 'example_data/2d.mrc'
        ABTT.io.mrc.make_test_2d(file)
        self.assertTrue(os.path.exists(file))

    def test_make_test_3d(self):
        file = 'example_data/3d.mrc'
        ABTT.io.mrc.make_test_3d(file)
        self.assertTrue(os.path.exists(file))

    def test_header(self):
        file = 'example_data/2d.mrc'
        header = ABTT.io.mrc.header(file)
        self.assertTrue(isinstance(header, np.recarray))
        self.assertTrue(header.nx == header.ny == 32)

    def test_size(self):
        file = 'example_data/2d.mrc'
        size = ABTT.io.mrc.size(file)
        self.assertTrue(len(size) == 3)

    def test_is_cube(self):
        file2d = 'example_data/2d.mrc'
        file3d = 'example_data/3d.mrc'
        self.assertFalse(ABTT.io.mrc.is_cube(file2d))
        self.assertTrue(ABTT.io.mrc.is_cube(file3d))
