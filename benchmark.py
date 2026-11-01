
import csv
import time
import statistics
from pathlib import Path

import nrrd
from main import project_plane


# Find files in the project folder
folder = Path(__file__).resolve().parent

mri_path = folder / "MRHead_1 (1).nrrd"
csv_path = folder / "MRI_test.csv"

print("Starting performance benchmark...")

# Read the real MRI file
volume, header = nrrd.read(str(mri_path))

print("MRI dimensions:", volume.shape)

# Read the test planes
planes = []

with open(csv_path, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        count = int(row["Number of Points (3 or 4)"])

        points = []

        for i in range(1, count + 1):
            points.append([
                float(row[f"x{i}"]),
                float(row[f"y{i}"]),
                float(row[f"z{i}"])
            ])

        planes.append(points)

print("Number of test planes:", len(planes))

if not planes:
    raise ValueError("No planes found in CSV")

# Warm up the algorithm
for points in planes:
    project_plane(volume, points)

# Repeat the test to get more reliable results
rounds = 5
repetitions = 10
results = []

for run in range(rounds):
    start = time.perf_counter()

    for _ in range(repetitions):
        for points in planes:
            project_plane(volume, points)

    elapsed = time.perf_counter() - start

    total = repetitions * len(planes)
    fps = total / elapsed

    results.append(fps)

    print(
        f"Run {run + 1}: "
        f"{fps:.2f} projections/second"
    )

print("------------------------------")

print(
    "Average processing FPS:",
    round(statistics.mean(results), 2)
)

print(
    "Median processing FPS:",
    round(statistics.median(results), 2)
)

print(
    "Minimum processing FPS:",
    round(min(results), 2)
)

print(
    "Maximum processing FPS:",
    round(max(results), 2)
)

print("PERFORMANCE TEST COMPLETED")
