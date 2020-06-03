#!/usr/bin/env python
# Import modules and put ABTT on path until it's available in environment
import os
import pathlib
import sys

sys.path.append('/mnt/storage/documents/IBS_PhD/programming/ABTT')
import numpy as np
import click

from ABTT.io.dynamo import table_map_read
from ABTT.io.dynamo import table_read as dynamo_table_read
from ABTT.io.star import StarDict
from ABTT.math.euler_angles import dynamo2relion as eulers_dynamo2relion


# Set up parser and command line interface
@click.command()
@click.argument('dynamo_table_file', required=False)
@click.argument('table_map_file', required=False)
@click.argument('output_star_file', required=False)
@click.option('-i',
              '--dynamo_table_file',
              help='Dynamo format table file, can only contain real values',
              prompt='Dynamo table file',
              type=str)
@click.option('-tm',
              '--table_map_file',
              help='Dynamo table map file, usually found in data folder',
              prompt='Table map file',
              type=str)
@click.option('-o',
              '--output_star_file',
              help='Star file for extraction in WARP or subtomogram averaging in RELION',
              prompt='Output star file',
              type=str)
def main(dynamo_table_file, table_map_file, output_star_file):
    message = f'Converting dynamo table file {dynamo_table_file} into a Warp/RELION format star file ({output_star_file})... '
    click.echo(message)

    # Check input files exist
    for item in dynamo_table_file, table_map_file:
        file = pathlib.Path(item)
        if not file.exists():
            raise Exception(f'File {file.absolute()} does not exist...')

    # Read table and table map
    table = dynamo_table_read(dynamo_table_file)
    table_map = table_map_read(table_map_file)

    # get number of rows
    n_rows = table['x'].shape[0]

    # Initialise StarDict for writing out star file
    star = StarDict()

    # Convert euler angles
    euler_angles_dynamo = table['eulers']
    euler_angles_relion = eulers_dynamo2relion(euler_angles_dynamo)
    rln_rot = euler_angles_relion[:, 0]
    rln_tilt = euler_angles_relion[:, 1]
    rln_psi = euler_angles_relion[:, 2]

    # Collect micrograph basenames
    for tomo_idx in table_map:
        path = table_map[tomo_idx]
        basename = os.path.basename(path)
        table_map[tomo_idx] = basename

    # Make list of basenames matching tomogram index from table
    basenames = np.empty(n_rows, dtype=object)

    for idx, tomo_idx in enumerate(table['tomo']):
        basenames[idx] = table_map[tomo_idx]

    # Add necessary info under proper headings to star file
    star['rlnCoordinateX'] = table['xyz'][:, 0]
    star['rlnCoordinateY'] = table['xyz'][:, 1]
    star['rlnCoordinateZ'] = table['xyz'][:, 2]

    star['rlnAngleRot'] = rln_rot
    star['rlnAngleTilt'] = rln_tilt
    star['rlnAnglePsi'] = rln_psi

    star['rlnMicrographName'] = basenames

    # Write out star file
    star.write(output_star_file)
    click.echo('Done!')


if __name__ == '__main__':
    main()
