
# Mutation Testing Report

## Objective

Verify that the automated tests can detect
an intentionally introduced bug and identify
the failing case.

## Experiment

The following line in main.py:

indices = np.rint(locations).astype(np.int64)

was temporarily changed to:

indices = np.floor(locations).astype(np.int64)

This mutation changes the sampling rule from
nearest-voxel rounding to rounding down.

## Results

The test_pixel_rounding.py script detected
the mutation.

Failing case:
- Coordinate: Z = 0.9993
- Expected pixel value: 112
- Actual pixel value: 12

The test raised an AssertionError identifying
the failed rounding case and both pixel values.

## Recovery

The original implementation was restored
using Git.

After restoration:
- All 11 pixel rounding tests passed.
- The Git working tree was clean.

## Conclusion

The experiment demonstrates that the pixel
rounding tests can detect this specific
incorrect change and identify the failing case.

It does not guarantee detection of every
possible bug.
