# 3D MRI Image Projection

## Project Description

This project reads a three-dimensional MRI scan in NRRD format and generates two-dimensional MRI slices based on coordinates provided in a CSV file.

The program supports triangular and trapezoidal regions, including tilted planes in 3D space.

The resulting slices are exported as an MP4 video at **30 FPS**.

## Programming Language

Python 3

Tested on Windows using Python 3.13.

## Required Libraries

- numpy
- pynrrd
- imageio
- imageio-ffmpeg

## Installation

Install Python 3, then open a terminal in the project directory.

Install all required dependencies using:

```bash
python -m pip install -r requirements.txt
```

On Windows, `py` may be used instead of `python`.

## Input Files

The program requires three command-line arguments:

## MRI Dataset

The MRI dataset used for this assignment is available
through the link provided in the original assignment:

[Download MRI Dataset](https://drive.google.com/file/d/1cqqOgSf8k4e14K5CBs-V_EvMmATX1K-J/view?usp=sharing)

The project was tested using the file:
`MRHead_1 (1).nrrd`

Place the NRRD file in the project directory before
running the application.

If the downloaded filename is different, use its
actual filename in the command-line arguments.

1. **NRRD file:** A three-dimensional MRI volume.
2. **CSV file:** A list of triangular or trapezoidal regions defined by 3D coordinates.
3. **Output file:** The name or path of the generated MP4 video.

Each CSV row defines one region containing either three or four points.

The CSV must include the expected coordinate columns and point-count header.

## How to Run

Open a terminal in the project directory and run:

```bash
python main.py "MRHead_1 (1).nrrd" MRI_test.csv result.mp4
```

General command format:

```bash
python main.py input.nrrd input.csv output.mp4
```

The MRI and CSV file paths can be changed without modifying the source code.


## How It Works

### Detailed Projection Algorithm

The implementation uses NumPy to compute 2D
projections from a 3D MRI volume.

1. Load the NRRD file as a three-dimensional
   NumPy array and read the input CSV file.

2. For each CSV row, read three points for a
   triangle or four points for a trapezoid.

3. Validate the geometry:
    - An isosceles triangle must have equal sides
      within a tolerance of 0.001.
    - A trapezoid must have equal side lengths.
    - Its top edge cannot exceed its bottom edge.
    - All four trapezoid points must be coplanar.
    - Degenerate or non-finite coordinates are rejected.

4. Define the horizontal sampling direction
   using the normalized bottom-edge vector:

   x_axis = (bottom_right - bottom_left) /
   length(bottom_right - bottom_left)

5. Calculate the midpoint of the top edge
   and the midpoint of the bottom edge.

6. Subtract the horizontal component from
   the vector connecting these midpoints.
   The resulting perpendicular component
   determines the projection height.

7. Determine the output image dimensions
   using the projected horizontal coordinates
   and the calculated height.

8. Generate sampling rows between the top
   and bottom edges using linear interpolation.

9. For each output row, calculate the left
   and right boundary positions.

10. Calculate sampling positions between
    these boundaries using NumPy arrays.

11. Convert the calculated 3D coordinates
    to voxel indices using nearest-neighbor
    sampling with np.rint().

12. Check whether each sampling position
    belongs to the geometric region and
    lies within the MRI volume boundaries.

13. Copy valid MRI voxel intensities into
    the output 2D image. Invalid or
    out-of-bounds pixels remain zero.

14. Return the projected image together
    with the number of valid sampled pixels.

### Video Generation

1. Process the input planes in CSV order.

2. Catch validation exceptions for invalid
   planes and preserve their frame positions.

3. Represent invalid planes with black
   frames containing a red X.

4. Normalize grayscale intensities and
   center the images on a common canvas.

5. Encode all frames into an MP4 video
   at a playback rate of 30 FPS.

6. Save a PNG preview of the first frame.

The implementation uses vectorized NumPy
operations to reduce Python-level loops
and improve projection processing speed.

Projection processing FPS and video
playback FPS are measured separately.

## Error Handling

The program includes basic input validation and error handling.

- Missing input files produce an error message.
- Rows with missing coordinates are skipped.
- Rows specifying an unsupported number of points are skipped.
- Degenerate regions with invalid dimensions are rejected.
- Non-finite coordinate values are rejected.
- Excessively large projection images are rejected.
- Coordinates outside the MRI volume produce black pixels where sampling is invalid.
- The program reports the number of valid and skipped regions.
- If the CSV contains rows but all planes are invalid, the program generates error frames. An empty CSV does not produce a video.

Invalid CSV rows do not prevent subsequent valid rows from being processed.

For invalid input, the program reports a warning rather than silently treating the data as valid.

## Output

The program generates:

- An MP4 video containing the valid MRI projections.
- A `first_plane.png` preview image showing the first valid projection.
- Terminal output showing processed regions, skipped regions, processing speed, and video FPS.

The video playback rate is fixed at **30 FPS**, independently of the number of valid input regions.

## Testing

The project includes several Python testing scripts.

### Geometry Tests

Run:

```bash
python test_geometry.py
```

The six geometry tests cover:

1. Triangle projection
2. Trapezoid projection
3. Regions outside the MRI
4. Partially out-of-bounds regions
5. Tilted triangle
6. Tilted trapezoid

**Result: All 6 tests passed.**

### Reference Pixel Value Tests

Run:

```bash
python test_reference_values.py
```

These tests compare the computed pixel values with expected values for a triangle and trapezoid.

**Result: Both tests passed.**

### Tilted Reference Tests

Run:

```bash
python test_tilted_reference.py
```

These tests compare computed values with expected values for tilted triangular and trapezoidal regions.

**Result: Both tests passed.**

### Additional Integration Tests

Additional tests were performed using:

- `MRI_test.csv` — sample triangular and trapezoidal regions.
- `MRI_tilted_test.csv` — tilted regions.
- `MRI_rotated_test.csv` — alternative 3D orientations.
- `MRI_invalid_test.csv` — valid and invalid rows mixed together.
- `MRI_all_invalid.csv` — input containing no valid regions.
- `MRI_stress_test.csv` — 60 input regions.

The 60-frame video was independently checked and confirmed to contain 60 frames at 30 FPS.

These tests demonstrate successful operation for the tested cases; they do not guarantee correctness for every possible input.

## Performance Benchmark

A performance benchmark was performed using a 3D MRI volume with dimensions:

**256 × 256 × 130**

Benchmark configuration:

- Test regions: 4
- Total processed projections: 200
- Benchmark rounds: 5

Results:

- Average processing rate: **149.65 projections/second**
- Minimum processing rate: **143.85 projections/second**
- Maximum processing rate: **153.86 projections/second**

The benchmark measures projection processing only.

It excludes MRI file loading and MP4 video encoding.

Actual performance depends on the computer, input dimensions, region sizes, and workload.
### Large Volume Performance Test (500x500x500)

A synthetic 3D volume of size 500x500x500
was used to evaluate projection performance.

- Volume data type: uint8
- Number of test planes: 4
- Benchmark rounds: 5
- Projections per round: 20
- Average processing rate: 67.11 projections/second
- Median processing rate: 66.89 projections/second
- Minimum processing rate: 65.02 projections/second
- Maximum processing rate: 68.69 projections/second

The measured processing rate exceeded 30
projections per second but did not reach
the expected rate of approximately 100.

The benchmark measures projection computation only.
It excludes NRRD loading and video encoding.

Profiling identified project_plane as the main
computational bottleneck.

The benchmark used synthetic volume data rather
than a real MRI scan.
## Current Limitations

- MRI projection uses nearest-neighbor sampling rather than interpolation between neighboring voxels.
- Input coordinates are interpreted as MRI array indices.
- The program assumes the expected point ordering and CSV structure.
- Invalid rows produce marked error frames instead of being automatically repaired.
- The video contains one frame for each CSV data row, including error frames for invalid planes.
- Large numbers of projections may increase memory usage because generated images are stored before video encoding.
- Testing on Windows does not guarantee identical behavior on every operating system.
- Additional testing may be needed for unusual or geometrically inconsistent input regions.

## Notes

The project does not depend on fixed coordinates from `Ex0.csv` or `MRI_test.csv`.

The CSV file is supplied as a command-line argument, allowing the program to process different input datasets that follow the expected format.

The video playback setting remains fixed at 30 FPS.

## Demo Video

The final MRI projection demo is available
in GitHub Releases:

[Download MRI Final Demo](https://github.com/bayanassadi4-eng/MRIPlaneProjection/releases/download/v1.0.0/MRI_final_demo.mp4)

Demo details:
- 60 frames
- 30 FPS
- MP4 video format
- Triangle and trapezoid projections

## Design Decisions and Justification

### 1. Pixel Sampling

The project uses nearest-neighbor sampling.

Each calculated 3D position is rounded to the
nearest voxel using NumPy's np.rint function.

This method was selected because it is simple,
efficient, and consistent with the assignment's
guidance regarding voxel selection.

Pixel rounding tests verify several boundary
and fractional-coordinate cases.

### 2. Invalid Plane Handling

Invalid geometric definitions raise ValueError.

During video generation, these exceptions are
handled without stopping the remaining projections.

Each invalid CSV row produces a black frame
with a red X.

This preserves the original CSV row order
and makes invalid projections visible.

### 3. Automated Testing

The project uses automated tests for geometry,
reference pixel values, tilted planes, rounding,
and invalid geometric definitions.

The test runner reports failing test files
and includes individual test output.

A mutation testing experiment demonstrated that
the tests detect an intentional rounding bug
and identify the failing case.

### 4. Performance Monitoring

Performance benchmarks measure the number of
projections processed per second.

The automated test runner compares performance
against a recorded baseline and reports
significant regressions.

A separate benchmark evaluates projection
performance using a synthetic 500x500x500 volume.

The measured average was 67.11 projections/second.

### 5. Limitations and Trade-offs

Nearest-neighbor sampling does not interpolate
between neighboring voxels.

The current implementation stores projection
images in memory before video encoding.

Coordinates are interpreted as MRI array indices.

The tests cover defined scenarios but cannot
guarantee correctness for every possible input.

### Additional Performance Measurements

The 500x500x500 benchmark was repeated twice
without modifying the projection algorithm.

First repeated benchmark:
- Average: 117.07 projections/second
- Minimum: 109.75 projections/second
- Maximum: 128.90 projections/second

Second repeated benchmark:
- Average: 129.78 projections/second
- Minimum: 121.49 projections/second
- Maximum: 136.09 projections/second

Both repeated measurements exceeded the
approximately 100 projections/second expectation.

The variation between runs may be related to
system load, CPU scheduling, or other runtime
conditions.

These measurements cover projection computation
only and exclude NRRD loading and MP4 encoding.

No code optimization was applied between
these benchmark runs.
