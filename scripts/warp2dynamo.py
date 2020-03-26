# Script for converting dynamo tables to star files for extraction in warp
# Files you need:
# 1) warp output particle star file (.star)

import sys

import numpy as np

from ABTT.io.dynamo import DynamoTable
from ABTT.io.star import read as star_read
from ABTT.math.euler_angles import relion2dynamo as eulers_relion2dynamo

sys.path.append('/mnt/storage/documents/IBS_PhD/programming/ABTT')

# Set variables here
WARP_STAR_FILE = '/mnt/storage/documents/IBS_PhD/programming/ABTT/scripts/warp2dynamo/warp.star'
OUTPUT_DYNAMO_TABLE = '/home/aburt/Desktop/linhua/warp2dynamo.tbl'
DATA_BOX_SIZE_PX = 128

# Read star file
star = star_read(WARP_STAR_FILE)

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
table.write(OUTPUT_DYNAMO_TABLE)

# Write out table map file
table_map_file = OUTPUT_DYNAMO_TABLE.replace('.tbl', '.doc')

with open(table_map_file, 'w') as table_map:
    for tomogram in tomogram_index_from_tomogram:
        tomogram_index = tomogram_index_from_tomogram[tomogram]
        table_map.write(f'{tomogram_index}\t{tomogram}\n')

# Modify table for reextraction
# reposition center to middle of box,
# change tomogram id to particle tag
reextraction_table = OUTPUT_DYNAMO_TABLE.replace('.tbl', '_reextract.tbl')
reextract_centre = DATA_BOX_SIZE_PX / 2

for axis in ['x', 'y', 'z']:
    table[axis] = np.ones_like(table[axis]) * reextract_centre

table['tomo'] = table['tag']
table.write(reextraction_table)

# Make and save reextraction tomogram table map
reextraction_table_map_file = OUTPUT_DYNAMO_TABLE.replace('.tbl', '_reextract.doc')

with open(reextraction_table_map_file, 'w') as table_map:
    for idx, particle in enumerate(star['rlnImageName']):
        current_tag = tags[idx]
        table_map.write(f'{current_tag}\t{particle}\n')
