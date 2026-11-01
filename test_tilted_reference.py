
import numpy as np
from main import project_plane


# Create a small MRI with known voxel values.
volume = np.zeros((8, 8, 8), dtype=np.int32)

for x in range(8):
    for y in range(8):
        for z in range(8):
            volume[x, y, z] = x + 10 * y + 100 * z


# TEST 1: Tilted triangle
triangle = [
    [2, 1, 1],
    [0, 5, 4],
    [4, 5, 4]
]

image, valid = project_plane(volume, triangle)

expected_triangle = np.array([
    [0,   0, 112,   0,   0],
    [0,   0, 222,   0,   0],
    [0,   0, 232,   0,   0],
    [0, 331, 332, 333,   0],
    [0, 341, 342, 343,   0],
    [450, 451, 452, 453, 454]
])

assert np.array_equal(image, expected_triangle), (
    f"Tilted triangle values incorrect:\n{image}"
)

assert valid == 14, (
    f"Expected 14 valid pixels, got {valid}"
)

print("TEST 1 PASSED: Tilted triangle values")


# TEST 2: Tilted trapezoid
trapezoid = [
    [1, 1, 1],
    [3, 1, 1],
    [0, 5, 4],
    [4, 5, 4]
]

image, valid = project_plane(volume, trapezoid)

expected_trapezoid = np.array([
    [0, 111, 112, 113,   0],
    [0, 221, 222, 223,   0],
    [0, 231, 232, 233,   0],
    [0, 331, 332, 333,   0],
    [0, 341, 342, 343,   0],
    [450, 451, 452, 453, 454]
])

assert np.array_equal(image, expected_trapezoid), (
    f"Tilted trapezoid values incorrect:\n{image}"
)

assert valid == 20, (
    f"Expected 20 valid pixels, got {valid}"
)

print("TEST 2 PASSED: Tilted trapezoid values")

print("ALL TILTED REFERENCE TESTS PASSED!")
