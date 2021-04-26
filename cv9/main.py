from __future__ import division
from numba import cuda
import numpy
import math


@cuda.jit
def subtraction(arr_1, arr_2):
    pos = cuda.grid(1)
    if pos < array_1.size:
        arr_1[pos] -= arr_2[pos]


array_1 = numpy.ones(128) * 8
array_2 = numpy.random.randint(1, 10, 128)
threadsperblock = 128
blockspergrid = math.ceil(array_1.shape[0] / threadsperblock)
subtraction[blockspergrid, threadsperblock](array_1, array_2)
print(array_1)
