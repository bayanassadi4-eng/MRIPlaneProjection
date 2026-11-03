
import time
import statistics
import numpy as np

from main import project_plane


print("Starting 500x500x500 performance benchmark...")

# Synthetic 3D MRI: approximately 125 MB
try:
    volume = np.full(
        (500, 500, 500),
        128,
        dtype=np.uint8
    )
except MemoryError:
    raise SystemExit(
        "Not enough memory for the benchmark"
    )

print("MRI dimensions:", volume.shape)

# Valid isosceles triangles and trapezoids
planes = [
    [
        [250, 100, 250],
        [100, 350, 250],
        [400, 350, 250],
    ],
    [
        [180, 100, 250],
        [320, 100, 250],
        [100, 350, 250],
        [400, 350, 250],
    ],
    [
        [250, 100, 100],
        [100, 350, 300],
        [400, 350, 300],
    ],
    [
        [180, 100, 100],
        [320, 100, 100],
        [100, 350, 300],
        [400, 350, 300],
    ],
]

print("Number of test planes:", len(planes))

# Warm-up before measuring
for points in planes:
    project_plane(volume, points)

rounds = 5
repetitions = 5
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

average = statistics.mean(results)

print("Average processing FPS:", round(average, 2))
print(
    "Median processing FPS:",
    round(statistics.median(results), 2)
)
print("Minimum processing FPS:", round(min(results), 2))
print("Maximum processing FPS:", round(max(results), 2))

if average > 30:
    print("Processing rate above 30 FPS: YES")
else:
    print("Processing rate above 30 FPS: NO")

print("500x500x500 BENCHMARK COMPLETED")
