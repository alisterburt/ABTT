import logging
import numpy as np

class StarDict(dict):
    """
    a dictionary with some methods for reading and writing of star files
    """
    def __init__(self, star_file=None):
        if star_file is not None:
            self.from_file(star_file)

    def from_file(self, star_file):
        logging.info(f'reading star file: {star_file}')
        header = read_star_header(star_file)
        column_headings = [info[1:info.find('#')].strip() for info in header if info.startswith('_')]

        body = read_star_body(star_file)
        for idx, heading in enumerate(column_headings):
            self[heading] = np.asarray(body[idx])

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



def read(star_file):
    """
    reads a star file into a StarDict object { column_name : [data] }
    :param star_file:
    :return: StarDict
    """
    star_dict = StarDict(star_file)
    return star_dict


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
            line = line.strip('\n')
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
            line = line.strip('\n')
            if not (line.startswith('_') or line.endswith('_') or line == ''):
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