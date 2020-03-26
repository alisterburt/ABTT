import logging

import numpy as np


class StarDict(dict):
    """
    a dictionary with some methods for reading and writing of star files
    """

    def __init__(self, star_file=None, data_block=None):
        if star_file is not None:
            self.from_file(star_file)

        elif data_block is not None:
            self.from_data_block(data_block)


    def from_file(self, star_file):
        logging.info(f'reading star file: {star_file}')
        loop_info = data_loop_start_indices(star_file)

        if len(loop_info) == 1:
            logging.info(f'single block star file...')
            header = read_star_header(star_file)
            column_headings = [info[1:info.find('#')].strip() for info in header if info.startswith('_')]
            body = read_star_body(star_file)
            for idx, heading in enumerate(column_headings):
                self[heading] = np.asarray(body[idx])

        else:
            logging.info('multi block star file...')
            data_blocks = get_data_blocks(star_file)
            for data_block in data_blocks:
                try:
                    header, body = clean_data_block(data_block)
                except:
                    logging.warning('one or more data blocks in this star file are unsupported')
                    continue

                column_headings = [info[1:info.find('#')].strip() for info in header if info.startswith('_')]
                for idx, heading in enumerate(column_headings):
                    self[heading] = np.asarray(body[idx])

    def from_data_block(self, data_block):
        logging.info('making stardict from data block')
        try:
            header, body = clean_data_block(data_block)
            column_headings = [info[1:info.find('#')].strip() for info in header if info.startswith('_')]
            for idx, heading in enumerate(column_headings):
                self[heading] = np.asarray(body[idx])
        except:
            logging.warning('one or more data blocks in this star file are unsupported')
            self['data'] = data_block

    def nrows(self):
        key = self.headings()[0]
        nrows = len(self[key])
        return nrows

    def headings(self):
        headings = list(self.keys())
        return headings

    def loopheader(self):
        headings = self.headings()
        loopheader = star_loopheader(headings)
        return loopheader

    def write(self, file):
        logging.info(f'writing star file: {file}')
        header = self.loopheader()
        body = []
        nrows = self.nrows()
        for row in range(nrows):
            current_row = []
            for column_name in self.headings():
                element = self[column_name][row]

                if any(_ in column_name.lower() for _ in ('coordinate',
                                                        'angle',
                                                        'apix',
                                                        'pixel',
                                                        'magnification')):
                    element = f'{element:>12.5f}'

                elif any(_ in column_name.lower() for _ in ('tag',
                                                            'idx')):
                    element = f'{element:>.0f}'

                current_row.append(f'{element}\t')

            current_row.append('\n')
            body.append(' '.join(current_row))

        with open(file, 'w') as file:
            for line in header:
                file.write(line)
            for line in body:
                file.write(line)

    def extract_eulers_relion(self):
        """
        extracts rlnAngleRot, rlnAngleTilt & rlnAnglePsi from a StarDict into an N,3 numpy array
        :return: euler_angles_relion (N,3) numpy array
        """
        rln_rot = self['rlnAngleRot']
        rln_tilt = self['rlnAngleTilt']
        rln_psi = self['rlnAnglePsi']

        euler_angles_relion = np.vstack((rln_rot, rln_tilt, rln_psi)).transpose()
        return euler_angles_relion


def read(star_file):
    """
    reads a star file into a StarDict object { column_name : [data] }
    :param star_file:
    :return: StarDict or dict of StarDicts
    """
    logging.info(f'reading star file {star_file}')
    loop_info = data_loop_start_indices(star_file)
    if len(loop_info) == 1:
        star_dict = StarDict(star_file)
        return star_dict

    else:
        data_blocks = get_data_blocks(star_file)
        star_dicts = {}
        for data_block in data_blocks:
            data_loop_name = data_block[0]
            star_dict = StarDict(data_block=data_block)
            star_dicts[data_loop_name] = star_dict
        return star_dicts





def star_loopheader(*args):
    """
    Generates a star file header for a given number of column headings
    :param *args: column headings for star file
    :return: list of strings, each string is a line of the star file
    """
    star_loopheader = ['data_\n',
                       'loop_\n']

    n_args = 0
    for arg in args:
        n_args += 1

    if n_args == 1 and isinstance(arg, list):
        for idx, heading in enumerate(arg):
            star_loopheader.append(f'_{heading} #{idx+1}\n')

    else:
        for idx, heading in enumerate(args):
            star_loopheader.append(f'_{heading} #{idx+1}\n')

    return star_loopheader


def read_star_header(star_file):
    """
    reads the header of a star file into a list
    :param star_file: star file
    :return: header
    """
    with open(star_file, 'r') as file:
        lines = file.readlines()

        header = []
        for line in lines:
            line = line.strip()
            if line.startswith('_') or line.endswith('_'):
                header.append(line)

    return header

def read_star_body(star_file):
    """
    reads the body of a star file into a list of lists, one list for each column
    :param star_file:
    :return:
    """
    with open(star_file, 'r') as file:
        lines = file.readlines()

        body_lines = []
        for line in lines:
            line = line.strip()
            if not (line.startswith('_') or
                    line.startswith('data_') or
                    line.startswith('loop_') or
                    line == '' or
                    line == ' ' or
                    line.startswith('#')):
                body_lines.append(line)

        n_cols = len(body_lines[0].split())
        body = [[] for _ in range(n_cols)]

        for line in body_lines:
            data = line.split()
            for idx, col in enumerate(data):
                try:
                    body[idx].append(float(col))
                except:
                    body[idx].append(col)
    return body


def data_loop_start_indices(star_file):
    """
    Checks how many data loops there are in a star file.
    :param star_file: star file
    :return: dict {'data_fsc' : start index}
    """
    with open(star_file, 'r') as file:
        lines = file.readlines()

        data_loops = {}
        for idx, line in enumerate(lines):
            line = line.strip()
            if line.startswith('data_'):
                data_loops[line] = idx

    return data_loops


def get_data_blocks(star_file):
    """
    Gets multiple data blocks, headings and data, from a star file
    :param star_file:
    :return: list of data blocks
    """
    loop_indices = data_loop_start_indices(star_file)
    with open(star_file, 'r') as file:
        lines = file.readlines()
        blocks = []

        for data_loop in loop_indices:
            block = []
            start_index = loop_indices[data_loop]
            seen_data_loop_name = False

            for line in lines[start_index:]:
                line = line.strip()

                if line.startswith('data_') and seen_data_loop_name is True:
                    break

                block.append(line)

                if line == data_loop:
                    seen_data_loop_name = True
            blocks.append(block)

        return blocks


def clean_data_block(star_data_block):
    """
    converts a list of strings corresponding to a data block from a star file into a StarDict
    :param star_data_block: list of strings
    :return: StarDict
    """
    logging.info('Cleaning data blocks from multi block star file')
    known_data_blocks = ['data_', 'data_fsc', 'data_guinier']

    if star_data_block[0] in known_data_blocks:
        header = []
        for line in star_data_block:
            line = line.strip()
            if line.startswith('_') or line.endswith('_'):
                header.append(line)

        body_lines = []
        for line in star_data_block:
            line = line.strip()
            if not (line.startswith('_') or
                    line.startswith('data_') or
                    line.startswith('loop_') or
                    line == '' or
                    line == ' ' or
                    line.startswith('#')):
                body_lines.append(line)

        n_cols = len(body_lines[0].split())
        body = [[] for _ in range(n_cols)]

        for line in body_lines:
            data = line.split()
            for idx, col in enumerate(data):
                try:
                    body[idx].append(float(col))
                except:
                    body[idx].append(col)

        return header, body

    else:
        logging.info(f'star data loop header not recognised: {star_data_block[0]}')
        return star_data_block
