
import numpy as np
from main import project_plane


# Create a small 3D MRI with known values
x, y, z = np.indices((8, 8, 8))
volume = (x + 10 * y + 100 * z).astype(np.int16)

print("Starting geometry tests...")


# TEST 1: Triangle
triangle = [
    [2, 1, 1],
    [0, 3, 1],
    [4, 3, 1]
]

image, valid = project_plane(volume, triangle)

assert image.shape == (3, 5)
assert image[0, 2] == 112
assert image[2, 0] == 130
assert image[2, 4] == 134
assert valid == 9

print("TEST 1 PASSED: Triangle")


# TEST 2: Trapezoid
trapezoid = [
    [1, 1, 1],
    [3, 1, 1],
    [0, 3, 1],
    [4, 3, 1]
]

image, valid = project_plane(volume, trapezoid)

assert image.shape == (3, 5)
assert image[0, 1] == 111
assert image[0, 3] == 113
assert image[2, 0] == 130
assert image[2, 4] == 134
assert valid == 11

print("TEST 2 PASSED: Trapezoid")


# TEST 3: Points outside MRI boundaries
outside_triangle = [
    [20, 1, 1],
    [18, 3, 1],
    [22, 3, 1]
]

image, valid = project_plane(volume, outside_triangle)

assert valid == 0
assert np.all(image == 0)

print("TEST 3 PASSED: Outside MRI")


# TEST 4: Triangle partially outside MRI
partial_triangle = [
    [8, 1, 1],
    [6, 3, 1],
    [10, 3, 1]
]

image, valid = project_plane(volume, partial_triangle)

assert image.shape == (3, 5)
assert image[2, 0] == 136
assert image[2, 1] == 137
assert image[2, 2] == 0
assert valid == 3

print("TEST 4 PASSED: Partial MRI boundaries")


# TEST 5: Tilted triangle in 3D
tilted_triangle = [
    [2, 1, 1],
    [0, 3, 3],
    [4, 3, 3]
]

image, valid = project_plane(volume, tilted_triangle)

assert image.shape == (4, 5)
assert image[0, 2] == 112
assert image[-1, 0] == 330
assert image[-1, 4] == 334
assert valid > 0

print("TEST 5 PASSED: Tilted Triangle")


# TEST 6: Tilted trapezoid in 3D
tilted_trapezoid = [
    [1, 1, 1],
    [3, 1, 1],
    [0, 3, 3],
    [4, 3, 3]
]

image, valid = project_plane(volume, tilted_trapezoid)

assert image.shape == (4, 5)
assert image[0, 1] == 111
assert image[0, 3] == 113
assert image[-1, 0] == 330
assert image[-1, 4] == 334
assert valid > 0

print("TEST 6 PASSED: Tilted Trapezoid")


print("ALL 6 TESTS PASSED!")
