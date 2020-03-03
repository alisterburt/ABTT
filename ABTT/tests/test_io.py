import os
import unittest

import numpy as np
from Bio import PDB

import ABTT.io


class StarDictTest(unittest.TestCase):

    def test_headings(self):
        star_file = 'example_data/io/example.star'
        star_dict = ABTT.io.star.read(star_file)
        headings = star_dict.headings()
        self.assertTrue(isinstance(headings, list))
        self.assertTrue('#' not in headings[0])

    def test_header(self):
        star_file = 'example_data/io/example.star'
        star_dict = ABTT.io.star.read(star_file)
        header = star_dict.loopheader()
        self.assertTrue('data_\n' in header)
        self.assertTrue('loop_\n' in header)

    def test_write(self):
        star_file = 'example_data/io/example.star'
        star_dict = ABTT.io.star.read(star_file)
        out_file = 'example_data/io/example_rewrite.star'
        star_dict.write(out_file)

    def test_data_loop_start_indices(self):
        star_file = 'example_data/fsc/postprocess.star'
        loop_info = ABTT.io.star.data_loop_start_indices(star_file)
        print(loop_info)

    def test_get_data_blocks(self):
        star_file = 'example_data/fsc/postprocess.star'
        data_blocks = ABTT.io.star.get_data_blocks(star_file)

    def test_read_relion_postprocess(self):
        star_file = 'example_data/fsc/postprocess.star'
        star_dicts = ABTT.io.star.read(star_file)

class MrcTest(unittest.TestCase):

    def test_make_test_2d(self):
        file = 'example_data/io/2d.mrc'
        ABTT.io.mrc.make_test_2d(file)
        self.assertTrue(os.path.exists(file))

    def test_make_test_3d(self):
        file = 'example_data/io/3d.mrc'
        ABTT.io.mrc.make_test_3d(file)
        self.assertTrue(os.path.exists(file))

    def test_header(self):
        file = 'example_data/io/2d.mrc'
        header = ABTT.io.mrc.header(file)
        self.assertTrue(isinstance(header, np.recarray))
        self.assertTrue(header.nx == header.ny == 32)

    def test_size(self):
        file = 'example_data/io/2d.mrc'
        size = ABTT.io.mrc.size(file)
        self.assertTrue(len(size) == 3)

    def test_is_cube(self):
        file2d = 'example_data/io/2d.mrc'
        file3d = 'example_data/io/3d.mrc'
        self.assertFalse(ABTT.io.mrc.is_cube(file2d))
        self.assertTrue(ABTT.io.mrc.is_cube(file3d))

    def test_data(self):
        file = 'example_data/io/2d.mrc'
        data = ABTT.io.mrc.data(file)
        self.assertTrue(isinstance(data, np.ndarray))
        self.assertTrue(data.shape == (32, 32))

    def test_voxel_size(self):
        file = 'example_data/io/3d.mrc'
        voxel_size = ABTT.io.mrc.voxel_size(file)
        self.assertTrue(isinstance(voxel_size, np.recarray))


class PDBTest(unittest.TestCase):
    def test_get(self):
        dir = 'example_data/io'
        pdb = ABTT.io.pdb.get('1A3N', directory=dir)
        self.assertTrue(os.path.exists(f'{dir}/pdb1a3n.ent'))

    def test_read(self):
        file = 'example_data/io/pdb1a3n.ent'
        structure = ABTT.io.pdb.read(file)
        self.assertTrue(isinstance(structure, PDB.Structure.Structure))

    def test_get_atoms(self):
        file = 'example_data/io/pdb1a3n.ent'
        atoms = ABTT.io.pdb.get_atoms(file)
        atom_counter = 0
        for atom in atoms:
            atom_counter += 1
        self.assertTrue(atom_counter == 4993)

    def test_coords(self):
        file = 'example_data/io/pdb1a3n.ent'
        for coords in ABTT.io.pdb.coords(file):
            self.assertTrue(len(coords) == 3)

    def test_unique_chains(self):
        file = 'example_data/io/pdb1a3n.ent'
        chains = ABTT.io.pdb.unique_chains(file)
        self.assertTrue(isinstance(chains, list))
        self.assertTrue(all(chain in ('A', 'B', 'C', 'D') for chain in chains))

    def test_chains_coords(self):
        file = 'example_data/io/pdb1a3n.ent'
        chains = []
        coords = []
        for chain, coord in ABTT.io.pdb.chains_coords(file):
            chains.append(chain)
            coords.append(coord)
        self.assertTrue(len(chains) == len(coords) == 4993)


class DynamoTableTest(unittest.TestCase):
    def test_read(self):
        file = 'example_data/io/dynamotable.tbl'
        table = ABTT.io.dynamo_table.read(file)
        self.assertTrue(table['x'][0] == 21.17)
        self.assertTrue(table['tdrot'][0] == 62.017)
        return table

    def test_write(self):
        table = self.test_read()
        table.write('example_data/io/dynamotable_out.tbl')
