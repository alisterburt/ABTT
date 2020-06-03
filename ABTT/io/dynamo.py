import logging

import numpy as np


class TableConvention(dict):
    """
    Dynamo table convention as per: https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Table_convention
    """

    def __init__(self):
        """dict {heading, column_idx (starts from 1, matlab convention)"""
        self.explanation = {}
        self['tag'] = 1
        self.explanation['tag'] = 'tag of particle file in data folder'
        self['aligned_value'] = 2
        self.explanation['aligned_value'] = 'value 1: marks the particle for alignment'
        self['averaged_value'] = 3
        self.explanation['averaged_value'] = 'value 1: the particle was included in the average'
        self['dx'] = 4
        self.explanation['dx'] = 'x shift from center (in pixels)'
        self['dy'] = 5
        self.explanation['dy'] = 'y shift from center (in pixels)'
        self['dz'] = 6
        self.explanation['dz'] = 'z shift from center (in pixels)'
        self['tdrot'] = 7
        self.explanation['tdrot'] = 'euler angle (rotation around z, in degrees)'
        self['tilt'] = 8
        self.explanation['tilt'] = 'euler angle (rotation around new x, in degrees)'
        self['narot'] = 9
        self.explanation['narot'] = 'euler angle (rotation around new z, in degrees)'
        self['cc'] = 10
        self.explanation['cc'] = 'cross correlaton coefficient'
        self['cc2'] = 11
        self.explanation['cc2'] = 'cross correlation coefficient after thresholding II'
        self['cpu'] = 12
        self.explanation['cpu'] = 'processor that aligned the particle'
        self['ftype'] = 13
        self.explanation['ftype'] = '0: full range; 1: tilt around y'
        self['ymintilt'] = 14
        self.explanation['ymintilt'] = 'minimum angle in the tilt series, usually -60'
        self['ymaxtilt'] = 15
        self.explanation['ymaxtilt'] = 'maximum angle in the tilt series, usually 60'
        self['xmintilt'] = 16
        self['xmaxtilt'] = 17
        self['fs1'] = 18
        self['fs2'] = 19
        self['tomo'] = 20
        self['reg'] = 21
        self['class'] = 22
        self['annotation'] = 23
        self['x'] = 24
        self['y'] = 25
        self['z'] = 26
        self['dshift'] = 27
        self['daxis'] = 28
        self['dnarot'] = 29
        self['dcc'] = 30
        self['otag'] = 31
        self['npar'] = 32
        self['ref'] = 34
        self['sref'] = 35
        self['apix'] = 36
        self['def'] = 37
        self['eig1'] = 41
        self['eig2'] = 42


class DynamoTable(dict):
    """
    A dictionary with some methods for reading and writing of dynamo table files
    """

    def __init__(self, table_file=None):
        self.convention = TableConvention()

        if table_file is not None:
            self.from_file(table_file)

    def from_file(self, table_file):
        logging.debug(f'reading table file: {table_file}')
        # try:
        data = np.loadtxt(table_file)
        # except:
        #     logging.debug(f'failed to read table, attempting to read as complex numbers...')
        #     data_complex = np.genfromtxt(table_file, dtype=np.complex128)
        #     data = data_complex.view(float)

        for key, column_idx in self.convention.items():
            try:
                logging.debug(f'loaded data for {key} into DynamoTable')
                zero_indexed_index = column_idx - 1
                self[key] = data[:, zero_indexed_index]
            except:
                logging.debug(f'failed to access data for {key}')

        self['eulers'] = self.get_eulers()
        self['xyz'] = self.get_xyz()

    def write(self, file):
        logging.info(f'writing table file from DynamoTable object: {file}')
        # Check all dict items have same length, if so set empty array
        if all([array.shape[0] for array in self.values()]):
            array = self[list(self.keys())[0]]
            data = np.zeros((array.shape[0], 41))

        else:
            logging.warning('not all elements in dictionary have the same length')

        for key, value in self.items():
            column_idx_zero_index = self.convention[key] - 1
            data[:, column_idx_zero_index] = value

        # Specify format
        format = ['%.4f' for _ in range(41)]
        for i in range(1):
            format[i] = '%d'

        # save file
        np.savetxt(file, data, delimiter=' \t', fmt=format)
        return file

    def get_eulers(self):
        """
        extracts euler angles from table as (N,3) numpy array
        :return: (N,3) numpy array of euler angles
        """
        return np.vstack((self['tdrot'], self['tilt'], self['narot'])).transpose()

    def get_xyz(self):
        """
        extracts xyz coordinates from table as (N,3) numpy array
        :return: (N,3) numpy array of xyz positions
        """
        x = self['x'] + self['dx']
        y = self['y'] + self['dy']
        z = self['z'] + self['dz']
        return np.vstack((x, y, z)).transpose()

    def averaged(self):
        """
        extracts only particles which contributed to an average for a given table
        :return: subtable
        """
        idx = self['averaged_value'] == 1
        subtable = self.subtable(idx)
        return subtable

    def subtable(self, selection_indices):
        """
        extracts selected indices into a subtable and returns that
        :param selection_indices:
        :return: subtable
        """
        subtable = DynamoTable()
        for key in self:
            subtable[key] = self[key][selection_indices]

        return subtable

    def number_of_particles(self):
        """
        calculates number of particles in table
        :return: number_of_particles
        """
        number_of_particles = self['x'].shape[0]
        return number_of_particles

    def particles_per_class(self):
        """
        calculates the number of particles contributing to each unique class in a DynamoTable object
        :param self: DynamoTable object
        :type self: dynamo_table
        :return: class_particles: { class_index : n_particles }
        """
        class_indices = np.unique(self['ref'])
        class_particles = StarDict

        for idx in class_indices:
            class_particles[idx] = np.sum(self['ref'] == idx)

        return class_particles

    def unique_tomograms(self):
        """
        extracts unique tomogram identifiers from a DynamoTable
        :param self: DynamoTable object
        :return: tomo_indices
        """
        tomo_indices = np.unique(self['tomo'])
        return tomo_indices

    def unique_classes(self):
        """
        extracts unique class identifiers from a DynamoTable
        :param self: DynamoTable object
        :return: class_indices
        """
        class_indices = np.unique(self['ref'])
        return class_indices

    def class_distribution(self):
        """
        calculates the class distribution
        :param self: DynamoTable object
        :return: particles_per_class { class_idx : n_particles }, percentage_per_class { class_idx : n_particles }
        """
        total_particles = self.number_of_particles()
        unique_classes = self.unique_classes()

        particles_per_class = {}
        percentage_per_class = {}

        for class_idx in unique_classes:
            particles_per_class[class_idx] = np.sum(self['ref'] == class_idx)
            percentage_per_class[class_idx] = 100 * (particles_per_class[class_idx] / total_particles)

        return particles_per_class, percentage_per_class

    def table_per_tomogram(self):
        """
        separates a table into dictionary of tables, one per tomogram, accessed by the tomogram index from the original table
        :param self: DynamoTable object
        :type self: DynamoTable
        :return: dict of DynamoTable objects { tomo_idx : DynamoTable }
        """
        tomo_indices = np.unique(self['tomo'])
        dict_of_dynamo_tables = {}

        for tomo_idx in tomo_indices:
            row_idx_for_current_tomogram = self['tomo'] == tomo_idx
            table_for_current_tomogram = DynamoTable()
            for key in self:
                table_for_current_tomogram[key] = self[key][row_idx_for_current_tomogram]
            dict_of_dynamo_tables[tomo_idx] = table_for_current_tomogram

        return dict_of_dynamo_tables

    def pairwise_distances(self):
        """
        returns a squareform pairwise distance matrix for the xyz positions in a DynamoTable object
        :param self: DynamoTable object
        :type DynamoTable: DynamoTable
        :return: pairwise_distance_matrix
        """
        xyz = self['xyz']
        pairwise_distance_matrix = squareform(pdist(xyz, 'euclidean'))

        return pairwise_distance_matrix

    def neighbours_in_range(self, min_distance, max_distance):
        """
        computes the number of neighbours within a minimum and maximum distance per particle for a DynamoTable object
        :param self: DynamoTable object
        :type self: DynamoTable
        :param min_distance: minimum distance above which particles are considered neighbours
        :param max_distance: maximum distance below which particles are considered neighbours
        :return: neighbours_in_range_per_particle : m-element numpy array if xyz in dynamo table is mx3
        """
        pairwise_distance_matrix = self.pairwise_distances()
        items_in_range = min_distance <= pairwise_distance_matrix < max_distance
        neighbours_in_range_per_particle = np.sum(items_in_range, 0)

        return neighbours_in_range_per_particle

    def neighbourhood_analysis(self, min_distance, max_distance, number_of_bins):
        """
        computes a per-particle neighbourhood analysis for a DynamoTable object
        neighbourhood analysis will be performed in equally sized, non-overlapping bins between the minimum and maximum distance
        :param self: DynamoTable object
        :type self: DynamoTable
        :param min_distance: minimum distance above which particles are considered neighbours
        :param max_distance: maximum distance below which particles are considered neighbours
        :param number_of_bins: number of equally spaced bins in which to measure number of neighbouring particles
        :return: neighbourhood_analysis_result, bin_centres, bin_minmax
        """

        bin_centres = np.linspace(min_distance, max_distance, number_of_bins)
        bin_width = np.abs(bin_centres[1] - bin_centres[0])
        minimum_values = bin_centres - (bin_width / 2.0)
        maximum_values = bin_centres + (bin_width / 2.0)

        bin_minmax = np.vstack((minimum_values, maximum_values)).transpose()

        pairwise_distance_matrix = self.pairwise_distances()
        n_rows = pairwise_distance_matrix.shape[0]
        neighbourhood_analysis_result = np.zeros((n_rows, number_of_bins))

        for idx, bin in enumerate(bin_minmax):
            bin_minimum = bin[0]
            bin_maximum = bin[1]
            items_in_range = bin_minimum <= pairwise_distance_matrix < bin_maximum
            neighbours_in_range_per_particle = np.sum(items_in_range, 0)
            neighbourhood_analysis_result[:, idx] = neighbours_in_range_per_particle

        return neighbourhood_analysis_result, bin_centres, bin_minmax


def table_read(table_file):
    dynamo_table = DynamoTable(table_file)
    return dynamo_table


def table_map_read(file):
    """
    Reads dynamo table map file
    :param file: table map file from dynamo
    :return: dict of form {idx : '/path/to/tomogram'}
    """
    table_map = open(file, 'r')
    lines = table_map.readlines()

    out_dict = {}
    for line in lines:
        idx, path = line.strip().split()
        out_dict[int(idx)] = path

    return out_dict
