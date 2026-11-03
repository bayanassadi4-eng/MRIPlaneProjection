
import numpy as np
from main import project_plane


volume = np.zeros((10, 10, 10), dtype=np.uint8)


def check_invalid(name, points, expected_message):
    try:
        project_plane(volume, points)
    except ValueError as error:
        if expected_message in str(error):
            print(f"PASSED: {name}")
            return
        raise AssertionError(
            f"{name}: Unexpected error: {error}"
        )

    raise AssertionError(
        f"{name}: Invalid plane was accepted"
    )


# Test 1: Triangle with unequal sides
check_invalid(
    "Invalid triangle",
    [[0, 0, 0], [0, 4, 0], [6, 4, 0]],
    "Invalid triangle: sides must be equal"
)

# Test 2: Trapezoid with unequal sides
check_invalid(
    "Unequal trapezoid sides",
    [[0, 0, 0], [4, 0, 0], [0, 4, 0], [6, 4, 0]],
    "Invalid trapezoid: sides must be equal"
)

# Test 3: Top edge longer than bottom edge
check_invalid(
    "Invalid top edge",
    [[-1, 0, 0], [5, 0, 0], [0, 4, 0], [4, 4, 0]],
    "Invalid trapezoid: top edge is longer"
)

# Test 4: Points not on the same plane
check_invalid(
    "Non-coplanar trapezoid",
    [[1, 0, 0], [3, 0, 1], [0, 4, 0], [4, 4, 1]],
    "Invalid trapezoid: points are not coplanar"
)

print("ALL 4 INVALID GEOMETRY TESTS PASSED!")
