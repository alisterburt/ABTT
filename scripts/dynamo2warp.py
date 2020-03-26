# Script for converting dynamo tables to star files for extraction in warp
# Files you need:
# 1) dynamo formatted table file (.tbl - make sure it only contains real values, no complex numbers)
# 2) dynamo tomogram table map file (.doc)

import os
import sys

import numpy as np

from ABTT.io.dynamo import table_map_read
from ABTT.io.dynamo import table_read as dynamo_table_read
from ABTT.io.star import StarDict
from ABTT.math.euler_angles import dynamo2relion as eulers_dynamo2relion

sys.path.append('/mnt/storage/documents/IBS_PhD/programming/ABTT')

DYNAMO_TABLE_FILE = '/home/aburt/Desktop/linhua/bin2_final_real.tbl'
TABLE_MAP_FILE = '/home/aburt/Desktop/linhua/tablemap_no_tomostar.doc'

OUTPUT_FILE = '/home/aburt/Desktop/linhua/table2star.star'

# Read table and table map
table = dynamo_table_read(DYNAMO_TABLE_FILE)
table_map = table_map_read(TABLE_MAP_FILE)

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
star.write(OUTPUT_FILE)
