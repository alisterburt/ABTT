import unittest
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
