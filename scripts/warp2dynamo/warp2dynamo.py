import sys

sys.path.append('/mnt/storage/documents/IBS_PhD/programming/ABTT')
import ABTT.io as io

STAR_FILE_IN = '/mnt/storage/documents/IBS_PhD/Minicells/WM5984/hex_consensus/find_c2_axes/c2_extracted_warp_nodup_8.94.star'
STAR_FILE_OUT = './dynamo_c2_nodup.star'
TABLE_FILE_OUT = './dynamo.tbl'
PREFIX_PATH = ''

# Read star file
star = io.star.read(STAR_FILE_IN)

# Store useful values
nrows = len(star['rlnCoordinateX'])
tags = star['dynParticleTag']

# Create dynamo star file
dynamo_star = io.star.StarDict()
dynamo_star['tag'] = tags
image_paths = []

for line in star['rlnImageName']:
    image_paths.append(f'{PREFIX_PATH}{line}')

dynamo_star['particleFile'] = image_paths
dynamo_star.write(STAR_FILE_OUT)
#
# # Get info for dynamo table
# # Manipulate Euler Angles
# euler_angles_relion = np.vstack((star['rlnAngleRot'],
#                                  star['rlnAngleTilt'],
#                                  star['rlnAnglePsi'])).transpose()
#
# angle_conversion = euler_angles.AngleConversion(euler_angles_relion, from_software='relion')
# euler_angles_dynamo = angle_conversion.to_software('dynamo')

# Get positions
# x = star['rlnCoordinateX']
# y = star['rlnCoordinateY']
# z = star['rlnCoordinateZ']
#
# # Make dynamo table file
# dynamo_table = io.dynamo_table.DynamoTable()
# dynamo_table['tag'] = tags
# dynamo_table['aligned_value'] = np.ones(nrows)
# dynamo_table['x'] = x
# dynamo_table['y'] = y
# dynamo_table['z'] = z
# dynamo_table['tdrot'] = euler_angles_dynamo[:, 0]
# dynamo_table['tilt'] = euler_angles_dynamo[:, 1]
# dynamo_table['narot'] = euler_angles_dynamo[:, 2]
#
# dynamo_table.write(TABLE_FILE_OUT)
