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

1. Load the 3D MRI volume from the NRRD file.
2. Read the coordinate information from the CSV file.
3. Identify whether each region is a triangle or trapezoid.
4. Calculate sampling positions inside the region.
5. Sample MRI voxel intensities using nearest-neighbor sampling.
6. Set positions outside the MRI volume to zero.
7. Convert valid projections into video frames.
8. Export the frames as an MP4 video at 30 FPS.
9. Save a preview image of the first valid projection.

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