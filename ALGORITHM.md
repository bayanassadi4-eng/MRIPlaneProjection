# MRI Plane Projection — Algorithm Documentation

## 1. Overview

The algorithm generates two-dimensional projections from a three-dimensional MRI volume stored in NRRD format.

Each row in the input CSV defines a geometric plane using three points (an isosceles triangle) or four points (an isosceles trapezoid).

The algorithm supports planes with different orientations in 3D space, including tilted planes.

## 2. Input and Output

**Inputs:**
- A three-dimensional MRI volume represented as a NumPy array.
- Three or four points defining the requested geometric region.

**Output:**
- A two-dimensional NumPy array containing the sampled MRI intensities.
- The number of valid sampled pixels.

## 3. Geometry Validation

Before generating a projection, the algorithm validates the input coordinates.

For triangular regions:
- The triangle must be isosceles.
- Its two equal sides are compared using a tolerance of 0.001.

For trapezoidal regions:
- The two side lengths must be equal within the specified tolerance.
- The top edge cannot be longer than the bottom edge.
- All four points must be coplanar.

Degenerate geometric regions and non-finite coordinates are rejected.

Invalid geometric definitions raise `ValueError`.

## 4. Constructing the Projection Plane

First, the algorithm computes a horizontal direction from the bottom edge:

`x_axis = (bottom_right - bottom_left) / bottom_edge_length`

Next, it calculates the midpoint of the bottom edge and the midpoint of the top edge.

The vector connecting these midpoints is separated into horizontal and perpendicular components.

The perpendicular component determines the vertical direction and height of the projection.

This construction allows the algorithm to process planes that are tilted in three-dimensional space.

## 5. Output Image Dimensions

The algorithm determines the width and height of the projected region from its geometric dimensions.

It then creates a two-dimensional output image initialized with zero values.

The algorithm also validates the image dimensions to prevent invalid or excessively large allocations.

## 6. Sampling the Geometric Region

The algorithm processes the region row by row.

For each output row:

1. Calculate its relative position between the top and bottom of the region.
2. Determine the corresponding left and right boundaries by linear interpolation.
3. Generate sampling positions between those boundaries.
4. Map the sampling positions into the three-dimensional MRI coordinate system.

NumPy vectorized operations are used to calculate many sampling positions efficiently instead of processing every pixel in a separate Python loop.

## 7. Nearest-Neighbor Voxel Sampling

The calculated sampling coordinates may contain fractional values.

The implementation selects the nearest voxel using:

`indices = np.rint(locations).astype(np.int64)`

The algorithm checks whether each sampled position is inside the MRI volume.

- Valid positions receive the corresponding MRI voxel intensity.
- Out-of-bounds positions remain zero.
- Pixels outside the defined geometric region remain zero.

Nearest-neighbor sampling was selected for its simplicity and computational efficiency.

## 8. Invalid Plane Handling

During video generation, invalid geometric definitions are handled without terminating the entire process.

For an invalid plane, the application generates a black frame with a red X.

This preserves the original order of the CSV rows while clearly indicating failed projections.

## 9. Video Generation

After processing the requested regions, the application:

1. Normalizes grayscale intensities for video display.
2. Places the generated projections on a common canvas.
3. Includes marked error frames for invalid regions.
4. Encodes the frames into an MP4 video at 30 FPS.

The MP4 playback frame rate is separate from the algorithm's projection processing speed.

## 10. Computational Complexity

Let W and H represent the dimensions of one generated two-dimensional projection.

The algorithm calculates sampling positions for approximately W × H output pixels.

Its time complexity per projection is therefore approximately:

**O(W × H)**

The output image and temporary sampling arrays also require memory proportional to the number of generated pixels.

Vectorization reduces Python-level overhead but does not eliminate the underlying pixel-processing work.

## 11. Design Limitations

- The implementation uses nearest-neighbor sampling rather than interpolating between adjacent MRI voxels.
- Coordinates are interpreted as MRI array indices.
- The input must follow the expected CSV format and point ordering.
- Correctness and performance depend on the tested geometric regions and execution environment.

## 12. Related Documentation

- `SRS.md` — Software requirements.
- `TESTING_STRATEGY.md` — Correctness, mutation, performance, and continuous integration testing.
- `MUTATION_TEST_REPORT.md` — Experimental verification of rounding-error detection.