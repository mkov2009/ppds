from __future__ import division
from numba import cuda
import numpy


@cuda.jit
def subtraction(arr_1, arr_2):
    pass


array_1 = numpy.ones(128) * 8
array_2 = numpy.random.randint(1, 10, 128)


