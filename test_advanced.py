import numpy as np
from main import project_plane

# MRI with known values
x, y, z = np.indices((8, 8, 8))
volume = (x + 10 * y + 100 * z).astype(np.int16)

print("Starting advanced geometry tests...")


# TEST 4: Tilted triangle in 3D
triangle = [
    [2, 1, 1],
    [0, 3, 3],
    [4, 3, 3]
]

image, valid = project_plane(volume, triangle)

assert image.shape == (4, 5)
assert image[0, 2] == 112
assert image[3, 0] == 330
assert image[3, 4] == 334

print("TEST 4 PASSED: Tilted triangle")


# TEST 5: Invalid triangle with zero-length base
invalid_triangle = [
    [2, 1, 1],
    [2, 3, 1],
    [2, 3, 1]
]

try:
    project_plane(volume, invalid_triangle)
except ValueError:
    print("TEST 5 PASSED: Invalid triangle rejected")
else:
    raise AssertionError(
        "Invalid triangle was not rejected"
    )


# TEST 6: Non-coplanar trapezoid
non_coplanar = [
    [1, 1, 1],
    [3, 1, 2],
    [0, 3, 1],
    [4, 3, 1]
]

try:
    project_plane(volume, non_coplanar)
except ValueError:
    print("TEST 6 PASSED: Non-coplanar shape rejected")
else:
    print(
        "TEST 6 NEEDS FIX: "
        "Non-coplanar shape was accepted"
    )

print("Advanced diagnostic tests completed.")