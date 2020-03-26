import logging

import numpy as np


class Convention(dict):
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
        self.convention = Convention()

        if table_file is not None:
            self.from_file(table_file)

    def from_file(self, table_file):
        logging.info(f'reading table file: {table_file}')
        data = np.loadtxt(table_file)
        for key, column_idx in self.convention.items():
            try:
                logging.debug(f'loaded data for {key} into DynamoTable')
                zero_indexed_index = column_idx - 1
                self[key] = data[:, zero_indexed_index]
            except:
                logging.debug(f'failed to access data for {key}')

        self['eulers'] = self.eulers()
        self['xyz'] = self.xyz()

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

    def eulers(self):
        """
        extracts euler angles from table as (N,3) numpy array
        :return: (N,3) numpy array of euler angles
        """
        return np.vstack((self['tdrot'], self['tilt'], self['narot'])).transpose()

    def xyz(self):
        """
        extracts xyz coordinates from table as (N,3) numpy array
        :return: (N,3) numpy array of xyz positions
        """
        x = self['x'] + self['dx']
        y = self['y'] + self['dy']
        z = self['z'] + self['dz']
        return np.vstack((x, y, z)).transpose()


def read(table_file):
    table = DynamoTable(table_file)
    return table
