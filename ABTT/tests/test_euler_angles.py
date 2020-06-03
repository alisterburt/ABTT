import timeit

import numpy as np

from ABTT.io.dynamo import table_read
from ABTT.math.euler_angles import Conversion

table_file = 'example_data/io/dynamotable.tbl'

table = table_read(table_file)

# eulers = table['eulers']
# xyz = table['xyz']
n = 1000000
eulers = np.random.random((n, 3))
xyz = np.random.random((n, 3))

# n = xyz.shape[0]

ac = Conversion(eulers, axes='ZXZ', reference_frame='rotate_particle', intrinsic=True)

start_time = timeit.default_timer()
r0 = ac.calculate_rotation_matrices()
loop_time = timeit.default_timer() - start_time

start_time = timeit.default_timer()
r1 = ac.calculate_rotation_matrices_fast()
np_time = timeit.default_timer() - start_time

print(f'loop time: {loop_time}')
print(f'np time: {np_time}')
print(f'np is {loop_time / np_time} faster')
print(f'Results for loop and np are same?: {np.allclose(r0, r1)}')
