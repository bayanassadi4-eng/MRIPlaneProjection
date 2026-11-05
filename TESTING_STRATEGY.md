# MRI Plane Projection — Testing Strategy

## 1. Objective

The testing strategy verifies the correctness, stability, and performance of the MRI plane projection algorithm.

Tests are designed to detect errors after code changes and identify failing scenarios.

## 2. Correctness Testing

The project includes 25 automated checks across five Python test files:

| Test File | Tests | Purpose |
|---|---:|---|
| test_geometry.py | 6 | Valid triangles, trapezoids, tilted planes, and MRI boundaries |
| test_reference_values.py | 2 | Verify output pixel values |
| test_tilted_reference.py | 2 | Verify pixel values for tilted projections |
| test_pixel_rounding.py | 11 | Verify nearest-voxel rounding |
| test_invalid_geometry.py | 4 | Verify rejection of invalid geometric definitions |

All 25 checks passed in the recorded local test run.

## 3. Invalid Input Testing

Invalid geometric definitions must raise `ValueError`.

During demo execution, invalid CSV rows produce marked error frames without stopping the processing of subsequent valid rows.

The frame order is preserved.

## 4. Mutation Testing

An intentional bug was introduced by replacing `np.rint()` with `np.floor()`.

The pixel rounding tests detected the mutation:

- Test case: Z = 0.9993
- Expected pixel value: 112
- Actual pixel value: 12

The original code was restored, and all 11 pixel rounding checks passed again.

This demonstrates detection of the tested mutation, not every possible bug.

## 5. Performance Testing

The project includes two performance benchmarks:

- `benchmark.py`: evaluates projection processing using the real MRI dataset.
- `benchmark_500.py`: evaluates projection processing using a synthetic 500×500×500 volume.

Recorded averages for the synthetic volume were:

- Initial run: 67.11 projections/second
- Repeated run: 117.07 projections/second
- Additional run: 129.78 projections/second

Performance depends on the execution environment. These benchmarks measure projection computation, excluding NRRD loading and video encoding.

## 6. Continuous Integration

GitHub Actions runs automatically on pushes and pull requests targeting `main`.

The workflow `.github/workflows/mri-tests.yml` installs Python dependencies, executes the five correctness test files, and runs the synthetic-volume benchmark.

A failed correctness test causes the workflow to fail. The synthetic benchmark reports performance but does not enforce a minimum FPS threshold.

## 7. Limitations

The tests cover selected valid and invalid cases, but do not guarantee correctness for every possible input.

The real MRI benchmark requires a locally available NRRD dataset and is not part of the current GitHub Actions workflow.

Performance measurements on GitHub-hosted runners are not directly comparable to local computer measurements.