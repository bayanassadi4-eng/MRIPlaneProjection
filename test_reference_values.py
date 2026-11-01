
import numpy as np
from main import project_plane


# Build a small 3D MRI with predictable values.
volume = np.zeros((8, 8, 8), dtype=np.int32)

for x in range(8):
    for y in range(8):
        for z in range(8):
            volume[x, y, z] = x + 10 * y + 100 * z


# TEST 1: Triangle
triangle = [
    [2, 1, 3],
    [0, 5, 3],
    [4, 5, 3]
]

triangle_image, triangle_valid = project_plane(
    volume, triangle
)

expected_triangle = np.array([
    [0,   0, 312,   0,   0],
    [0,   0, 322,   0,   0],
    [0, 331, 332, 333,   0],
    [0, 341, 342, 343,   0],
    [350, 351, 352, 353, 354]
])

assert np.array_equal(
    triangle_image, expected_triangle
), "Triangle pixel values are incorrect"

assert triangle_valid == 13

print("TEST 1 PASSED: Triangle pixel values")


# TEST 2: Trapezoid
trapezoid = [
    [1, 1, 3],
    [3, 1, 3],
    [0, 5, 3],
    [4, 5, 3]
]

trapezoid_image, trapezoid_valid = project_plane(
    volume, trapezoid
)

expected_trapezoid = np.array([
    [0, 311, 312, 313,   0],
    [0, 321, 322, 323,   0],
    [0, 331, 332, 333,   0],
    [0, 341, 342, 343,   0],
    [350, 351, 352, 353, 354]
])

assert np.array_equal(
    trapezoid_image, expected_trapezoid
), "Trapezoid pixel values are incorrect"

assert trapezoid_valid == 17

print("TEST 2 PASSED: Trapezoid pixel values")

print("ALL REFERENCE VALUE TESTS PASSED!")
