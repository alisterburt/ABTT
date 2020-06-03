#!/usr/bin/env python
# import modules and put ABTT on path until available as part of environment
import sys

sys.path.append('/mnt/storage/documents/IBS_PhD/programming/ABTT')
import pathlib
import numpy as np
import click

from ABTT.io.dynamo import DynamoTable
from ABTT.io.star import read as star_read
from ABTT.math.euler_angles import relion2dynamo as eulers_relion2dynamo


# Setup parser and command line interface
@click.command()
@click.argument('warp_star_file', required=False)
@click.argument('output_dynamo_table', required=False)
@click.argument('data_box_size', required=False)
@click.option('-i',
              '--warp_star_file',
              help='Star file output by warp upon particle extraction',
              prompt='Star file output by warp upon particle extraction',
              type=str)
@click.option('-o',
              '--output_dynamo_table',
              help='Output dynamo table file to be used in subsequent subtomogram averaging',
              prompt='Output dynamo table file',
              type=str)
@click.option('-s',
              '--data_box_size',
              help='Box size of extracted particles in pixels',
              prompt='Box size of data (px)',
              type=int)
def main(warp_star_file, output_dynamo_table, data_box_size):
    message = f'Converting warp output {warp_star_file} into a dynamo table ({output_dynamo_table})...'
    click.echo(message)

    # Check warp star file exists
    warp_star_file = pathlib.Path(warp_star_file)
    if not warp_star_file.exists():
        raise Exception(f'File {warp_star_file.absolute()} does not exist...')

    # Read star file
    star = star_read(warp_star_file)

    # Convert euler angles
    euler_angles_relion = star.extract_eulers_relion()
    euler_angles_dynamo = eulers_relion2dynamo(euler_angles_relion)
    dyn_tdrot = euler_angles_dynamo[:, 0]
    dyn_tilt = euler_angles_dynamo[:, 1]
    dyn_narot = euler_angles_dynamo[:, 2]

    # Generate tags
    n_rows = star['rlnCoordinateX'].shape[0]
    tags = np.arange(n_rows) + 1

    # Generate tomogram indices for table from paths
    tomogram_index_from_tomogram = {}
    unique_tomos = np.unique(star['rlnMicrographName'])

    for idx, tomogram_path in enumerate(unique_tomos):
        tomogram_index_from_tomogram[tomogram_path] = idx + 1

    tomogram_indices = np.empty_like(star['rlnMicrographName'], dtype=int)

    for idx, tomogram_name in enumerate(star['rlnMicrographName']):
        tomogram_indices[idx] = tomogram_index_from_tomogram[tomogram_name]

    # Initialise DynamoTable
    table = DynamoTable()
    table['tag'] = tags
    table['aligned_value'] = np.ones_like(tags)
    table['averaged_value'] = np.ones_like(tags)
    table['x'] = star['rlnCoordinateX']
    table['y'] = star['rlnCoordinateY']
    table['z'] = star['rlnCoordinateZ']
    table['tdrot'] = dyn_tdrot
    table['tilt'] = dyn_tilt
    table['narot'] = dyn_narot
    table['tomo'] = tomogram_indices

    # Write out table
    table.write(output_dynamo_table)

    # Write out table map file
    table_map_file = output_dynamo_table.replace('.tbl', '.doc')

    with open(table_map_file, 'w') as table_map:
        for tomogram in tomogram_index_from_tomogram:
            tomogram_index = tomogram_index_from_tomogram[tomogram]
            table_map.write(f'{tomogram_index}\t{tomogram}\n')

    # Modify table for reextraction of dynamo data folder
    # reposition center to middle of box,
    # change tomogram id to particle tag
    reextraction_table = output_dynamo_table.replace('.tbl', '_reextract.tbl')
    reextract_centre = data_box_size / 2

    for axis in ['x', 'y', 'z']:
        table[axis] = np.ones_like(table[axis]) * reextract_centre

    table['tomo'] = table['tag']
    table.write(reextraction_table)

    # Make and save reextraction tomogram table map
    reextraction_table_map_file = output_dynamo_table.replace('.tbl', '_reextract.doc')

    with open(reextraction_table_map_file, 'w') as table_map:
        for idx, particle in enumerate(star['rlnImageName']):
            current_tag = tags[idx]
            table_map.write(f'{current_tag}\t{particle}\n')

    click.echo('Done! You can reextract this as a dynamo formatted data folder using a command such as...')
    click.echo('dtcrop <tomogram_table_map.doc> <tableForAllTomograms>  <outputfolder> <sidelength>')


# Run CLI
if __name__ == '__main__':
    main()
