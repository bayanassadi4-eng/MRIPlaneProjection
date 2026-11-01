
import numpy as np
from main import project_plane


# Create an MRI with predictable voxel values.
volume = np.zeros((8, 8, 8), dtype=np.int32)

for x in range(8):
    for y in range(8):
        for z in range(8):
            volume[x, y, z] = x + 10 * y + 100 * z


def check_pixel(test_name, points, expected_value):
    image, valid = project_plane(volume, points)

    actual_value = int(image[0, 2])

    assert valid > 0, (
        f"{test_name} FAILED: No valid pixels"
    )

    assert actual_value == expected_value, (
        f"{test_name} FAILED\n"
        f"Expected pixel value: {expected_value}\n"
        f"Actual pixel value: {actual_value}"
    )

    print(f"PASSED: {test_name}")


print("Starting pixel rounding tests...")


# Test fractional Z coordinates.
z_cases = [
    (0.4, 0),
    (0.9993, 1),
    (1.0007, 1),
    (1.5, 2),
    (2.5, 2),
    (2.5001, 3),
    (3.5, 4),
]

for z_value, expected_z in z_cases:

    points = [
        [1, 1, z_value],
        [3, 1, z_value],
        [0, 5, z_value],
        [4, 5, z_value],
    ]

    expected_pixel = 12 + 100 * expected_z

    check_pixel(
        f"Z rounding {z_value} -> {expected_z}",
        points,
        expected_pixel
    )


# Test fractional X coordinates.
x_cases = [
    (0.4, 2),
    (0.5, 2),
    (0.5001, 3),
    (1.5, 4),
]

for offset, expected_x in x_cases:

    points = [
        [1 + offset, 1, 3],
        [3 + offset, 1, 3],
        [0 + offset, 5, 3],
        [4 + offset, 5, 3],
    ]

    expected_pixel = expected_x + 10 + 300

    check_pixel(
        f"X rounding with offset {offset}",
        points,
        expected_pixel
    )


print("------------------------------")
print("ALL 11 PIXEL ROUNDING TESTS PASSED!")
