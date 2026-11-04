# Software Requirements Specification (SRS)

## Project: 3D MRI Image Projection

### 1. Introduction

The purpose of this project is to develop a Python application that extracts two-dimensional image slices from a three-dimensional MRI volume.

The application receives an MRI file in NRRD format and a CSV file containing coordinates that define triangular or trapezoidal regions.

The generated slices are exported as an MP4 video at a fixed playback rate of 30 FPS.

### 2. Functional Requirements

**FR1 – MRI Input**

The system shall read a three-dimensional MRI volume stored in NRRD format.

**FR2 – CSV Input**

The system shall read a CSV file containing three or four 3D points for each requested projection.

Input points shall be read from the supplied CSV file rather than hard-coded into the application.

**FR3 – Geometric Projection**

The system shall calculate two-dimensional images from triangular and trapezoidal regions defined by the input coordinates.

The implementation shall support tilted regions in three-dimensional space.

**FR4 – Pixel Sampling**

The system shall sample MRI voxel intensities using nearest-neighbor sampling.

**FR5 – Boundary Handling**

Pixels corresponding to locations outside the MRI volume shall be assigned zero intensity.

**FR6 – Video Output**

The system shall save the generated images as frames in an MP4 video.

Valid projections shall appear in the same relative order as their corresponding CSV rows.

**FR7 – Video Frame Rate**

The generated MP4 video shall have a fixed playback rate of 30 frames per second.

The playback rate shall not depend on the number of input projections.

**FR8 – Input Validation**

The system shall detect supported types of invalid input, including:

- Missing coordinates.
- Unsupported numbers of points.
- Non-finite coordinate values.
- Degenerate regions with invalid dimensions.
- Projection dimensions exceeding the implemented safety limit.

**FR9 – Error Handling**

The system shall report understandable warnings for invalid CSV rows and continue processing subsequent valid rows when possible.

If all CSV planes are invalid, the system shall generate a video containing an error frame for each row. An empty CSV does not produce a video.

**FR10 – Processing Information**

The system shall display processing information, including:

- MRI volume dimensions.
- Processed projection dimensions.
- Number of sampled pixels.
- Number of valid projections.
- Number of skipped projections.
- Projection processing rate.
- Configured video FPS.

**FR11 – Preview Image**

The system shall save a PNG preview of the first output frame, which may be an error frame.

### 3. Non-Functional Requirements

**NFR1 – Programming Language**

The application shall be implemented in Python 3.

**NFR2 – Portability**

The application should be runnable on compatible computers with Python and the required libraries installed.

Dependencies shall be listed in `requirements.txt`.

**NFR3 – Performance**

The application should process projections efficiently.

Processing speed shall be measurable and reported.

Performance may vary depending on the computer, image dimensions, and input data.

**NFR4 – Reliability**

The application should handle supported invalid-input cases without an unhandled exception.

**NFR5 – Maintainability**

The code should be readable, organized, and documented.

**NFR6 – Reusability**

The program shall accept different input files through command-line arguments without requiring modifications to the source code.

### 4. Testing Requirements

The implementation shall be tested for:

- Triangle projection.
- Trapezoid projection.
- Tilted triangle projection.
- Tilted trapezoid projection.
- Coordinates outside MRI boundaries.
- Partially out-of-bounds regions.
- Correct reference pixel values.
- Missing or invalid CSV coordinates.
- Unsupported numbers of points.
- Continuing after invalid CSV rows.
- CSV files containing no valid projections.
- Multiple input projections.
- Correct MP4 frame rate and frame count.
- Processing performance.

### 5. Testing Results

**5.1 Geometry Tests**

The six geometry tests in `test_geometry.py` passed.

**5.2 Reference Pixel Tests**

The two reference tests in `test_reference_values.py` passed.

**5.3 Tilted Reference Tests**

The two tests in `test_tilted_reference.py` passed.

**5.4 Invalid Input Tests**

The program successfully skipped invalid CSV rows and continued processing subsequent valid rows.

A CSV file containing no valid projections was handled without an unhandled exception.

**5.5 Stress Test**

The application successfully processed 60 input regions.

The generated MP4 was independently checked and confirmed to contain 60 frames at 30 FPS.

**5.6 Performance Benchmark**

The benchmark processed 200 projections across five rounds.

Measured processing rates:

- Average: 149.65 projections/second.
- Minimum: 143.85 projections/second.
- Maximum: 153.86 projections/second.

The benchmark measures projection computation only, excluding MRI loading and MP4 encoding.

### 6. Current Implementation Status

The MRI input, CSV processing, geometric projection, pixel sampling, MP4 output, 30 FPS configuration, preview generation, and basic error handling have been implemented.

The recorded geometry, reference-value, invalid-input, and 60-frame tests passed.

The implementation has been tested in a new Python environment on Windows.

Successful tests do not guarantee correct behavior for every possible geometric configuration or malformed input.

### 7. Known Limitations

- The implementation uses nearest-neighbor sampling.
- Input coordinates are interpreted as MRI array indices.
- The program relies on the expected coordinate ordering and CSV structure.
- Invalid CSV rows are skipped rather than repaired.
- Invalid triangle or trapezoid geometry raises ValueError. The demo handles these exceptions by generating marked error frames.
- All valid projection images are stored in memory before video encoding.
- Performance depends on input size and computer resources.
- Cross-platform execution has not been independently tested on every operating system.
- Additional verification is needed for unusual geometric configurations and exact compliance with the assignment's coordinate conventions.
-
## 8. Final Validation and Performance Results

### Automated Testing

The project includes 25 automated checks across five test files:

- 6 geometry tests
- 2 reference pixel value tests
- 2 tilted reference tests
- 11 pixel rounding tests
- 4 invalid geometry tests

All 25 tests passed in the latest test run.

### Invalid Plane Handling

Invalid triangle and trapezoid definitions raise ValueError.

During video generation, invalid CSV rows produce
marked error frames instead of being removed.

The original CSV row order is preserved.

### Large Volume Benchmark

A synthetic 500x500x500 uint8 volume was tested.

- Average processing rate: 67.11 projections/second
- Minimum: 65.02 projections/second
- Maximum: 68.69 projections/second

The benchmark measures projection computation,
excluding MRI loading and video encoding.

The processing rate exceeded 30 projections/second
but did not reach the approximately 100
projections/second performance expectation.

### Validation Status

The application passed the recorded automated tests
and invalid-input video checks.

Further testing may be needed for unusual input
geometries and different computer environments.
