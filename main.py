
import csv
import sys
import time
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
import nrrd


EPS = 1e-8
VIDEO_FPS = 30
MAX_PLANE_PIXELS = 4_000_000


def project_plane(volume, points):
    """Sample a 3D MRI on a triangular or trapezoid-shaped plane."""

    points = np.asarray(points, dtype=np.float64)

    if len(points) not in (3, 4):
        raise ValueError("Each plane must have 3 or 4 points")

    if points.shape != (len(points), 3):
        raise ValueError("Each point must contain x, y, z")

    if not np.all(np.isfinite(points)):
        raise ValueError("Coordinates must be finite numbers")

    if len(points) == 3:
        top_left = top_right = points[0]
        bottom_left = points[1]
        bottom_right = points[2]
    else:
        top_left = points[0]
        top_right = points[1]
        bottom_left = points[2]
        bottom_right = points[3]

    bottom_vector = bottom_right - bottom_left
    bottom_width = np.linalg.norm(bottom_vector)

    if not np.isfinite(bottom_width) or bottom_width < EPS:
        raise ValueError("The bottom edge must have positive length")

    x_axis = bottom_vector / bottom_width

    top_middle = (top_left + top_right) / 2.0
    bottom_middle = (bottom_left + bottom_right) / 2.0

    center_vector = bottom_middle - top_middle

    height_vector = (
            center_vector
            - np.dot(center_vector, x_axis) * x_axis
    )

    height_length = np.linalg.norm(height_vector)

    if not np.isfinite(height_length) or height_length < EPS:
        raise ValueError("Plane height must be positive")
    # Validate an isosceles triangle
    if len(points) == 3:
        side1 = np.linalg.norm(bottom_left - top_left)
        side2 = np.linalg.norm(bottom_right - top_left)

        if abs(side1 - side2) >= 0.001:
            raise ValueError(
                "Invalid triangle: sides must be equal"
            )
    if len(points) == 4:
        side1 = np.linalg.norm(bottom_left - top_left)
        side2 = np.linalg.norm(bottom_right - top_right)
        top_width = np.linalg.norm(
            top_right - top_left
        )

        if top_width > bottom_width:
            raise ValueError(
                "Invalid trapezoid: top edge is longer than bottom edge"
            )
        if abs(side1 - side2) >= 0.001:
           raise ValueError(
            "Invalid trapezoid: sides must be equal"
        )

        normal = np.cross(bottom_vector, height_vector)
        normal_length = np.linalg.norm(normal)

        if normal_length < EPS:
            raise ValueError("Cannot calculate plane normal")

        normal = normal / normal_length

        out_of_plane = abs(
            np.dot(top_right - top_left, normal)
        )

        if out_of_plane >= 0.001:
         raise ValueError(
        "Invalid trapezoid: points are not coplanar"
    )

    top_left_x = np.dot(
        top_left - bottom_left,
        x_axis
    )

    top_right_x = np.dot(
        top_right - bottom_left,
        x_axis
    )

    min_x = np.floor(
        min(0.0, bottom_width, top_left_x, top_right_x)
    )

    max_x = np.ceil(
        max(0.0, bottom_width, top_left_x, top_right_x)
    )

    width = max(1, int(max_x - min_x) + 1)
    height = max(1, int(np.ceil(height_length)) + 1)

    if width * height > MAX_PLANE_PIXELS:
        raise ValueError(
            "Plane is too large to process safely"
        )

    t = np.linspace(
        0.0,
        1.0,
        height
    )[:, None]

    left = (
            top_left
            + t * (bottom_left - top_left)
    )

    right = (
            top_right
            + t * (bottom_right - top_right)
    )

    left_x = (left - bottom_left) @ x_axis
    right_x = (right - bottom_left) @ x_axis

    x = (
            np.arange(width, dtype=np.float64)[None, :]
            + min_x
    )

    span_x = (right_x - left_x)[:, None]
    numerator = x - left_x[:, None]

    fraction = np.zeros(
        (height, width),
        dtype=np.float64
    )

    np.divide(
        numerator,
        span_x,
        out=fraction,
        where=np.abs(span_x) > EPS
    )

    inside = (
            (fraction >= -EPS)
            & (fraction <= 1 + EPS)
    )

    zero_width_rows = (
            np.abs(span_x[:, 0]) <= EPS
    )

    if np.any(zero_width_rows):
        inside[zero_width_rows] = (
                np.abs(numerator[zero_width_rows]) <= 0.5
        )
        fraction[zero_width_rows] = 0.0

    fraction = np.clip(
        fraction,
        0.0,
        1.0
    )

    locations = (
            left[:, None, :]
            + fraction[:, :, None]
            * (right - left)[:, None, :]
    )

    indices = np.rint(locations).astype(np.int64)

    volume_shape = np.array(volume.shape)

    valid = (
            inside
            & np.all(
        (indices >= 0)
        & (indices < volume_shape),
        axis=2
    )
    )

    image = np.zeros(
        (height, width),
        dtype=volume.dtype
    )

    positions = indices[valid]

    if len(positions):
        image[valid] = volume[
            positions[:, 0],
            positions[:, 1],
            positions[:, 2]
        ]

    return image, int(valid.sum())


def to_video_frame(image, height, width, max_intensity):
    """Convert an MRI image or an error into a video frame."""

    # Invalid plane: create a black frame with a red X.
    if image is None:
        frame = np.zeros(
            (height, width, 3),
            dtype=np.uint8
        )

        rows = np.arange(height)

        cols = np.rint(
            rows * (width - 1) / max(height - 1, 1)
        ).astype(int)

        for offset in range(-2, 3):
            left = np.clip(cols + offset, 0, width - 1)
            right = np.clip(
                width - 1 - cols + offset,
                0,
                width - 1
            )

            frame[rows, left, 0] = 255
            frame[rows, right, 0] = 255

        return frame

    # Valid plane: convert the MRI image as before.
    gray = np.clip(
        image.astype(np.float32)
        * (255.0 / max_intensity),
        0,
        255
    ).astype(np.uint8)

    canvas = np.zeros(
        (height, width),
        dtype=np.uint8
    )

    h, w = gray.shape

    y = (height - h) // 2
    x = (width - w) // 2

    canvas[y:y + h, x:x + w] = gray

    return np.repeat(
        canvas[:, :, None],
        3,
        axis=2
    )

def main():
    if len(sys.argv) != 4:
        print(
            'Usage: python main.py "MRI.nrrd" planes.csv output.mp4'
        )
        return

    nrrd_file, csv_file, mp4_file = sys.argv[1:]

    if not Path(nrrd_file).is_file():
        print("Error: MRI file not found:", nrrd_file)
        return

    if not Path(csv_file).is_file():
        print("Error: CSV file not found:", csv_file)
        return

    try:
        volume, _header = nrrd.read(nrrd_file)
    except (OSError, ValueError) as error:
        print("Error reading MRI:", error)
        return

    if volume.ndim != 3:
        print("Error: Expected a 3D MRI volume")
        return

    print("MRI dimensions:", volume.shape)

    all_images = []
    skipped_planes = 0

    started = time.perf_counter()

    try:
        with open(
                csv_file,
                newline="",
                encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for number, row in enumerate(reader, start=1):

                try:
                    count = int(
                        row["Number of Points (3 or 4)"]
                    )

                    if count not in (3, 4):
                        raise ValueError(
                            "Expected 3 or 4 points"
                        )

                    points = []

                    for i in range(1, count + 1):
                        point = [
                            float(row[f"x{i}"]),
                            float(row[f"y{i}"]),
                            float(row[f"z{i}"])
                        ]
                        points.append(point)

                    image, valid = project_plane(
                        volume,
                        points
                    )

                except (
                        ValueError,
                        KeyError,
                        TypeError,
                        OverflowError
                ) as error:

                    skipped_planes += 1

                    print(
                         f"Warning: Invalid plane "
                         f"{number}: {error}"
                    )

                    all_images.append(None)
                    continue

                all_images.append(image)

                print(
                    f"Plane {number}: "
                    f"{image.shape}, "
                    f"sampled pixels: {valid}"
                )

    except (OSError, UnicodeError, csv.Error) as error:
        print("Error reading CSV:", error)
        return

    elapsed = time.perf_counter() - started

    if not all_images:
        print("The CSV contains no planes")
        return

    valid_images = [
        image for image in all_images
        if image is not None
    ]

    if valid_images:
        max_h = max(
            image.shape[0]
            for image in valid_images
        )

        max_w = max(
            image.shape[1]
            for image in valid_images
        )
    else:
        max_h = 256
        max_w = 256
    canvas_h = (max_h + 15) // 16 * 16
    canvas_w = (max_w + 15) // 16 * 16

    maximum = max(
        float(np.max(volume)),
        1.0
    )

    try:
        with imageio.get_writer(
                mp4_file,
                fps=VIDEO_FPS,
                codec="libx264",
                macro_block_size=16
        ) as writer:

            for image in all_images:
                frame = to_video_frame(
                    image,
                    canvas_h,
                    canvas_w,
                    maximum
                )

                writer.append_data(frame)

    except (OSError, ValueError, RuntimeError) as error:
        print("Error creating video:", error)
        return

    preview_file = Path(mp4_file).with_name(
        "first_plane.png"
    )

    try:
        imageio.imwrite(
            str(preview_file),
            to_video_frame(
                all_images[0],
                canvas_h,
                canvas_w,
                maximum
            )
        )
        print("First image saved:", preview_file)

    except (OSError, ValueError) as error:
        print("Warning: Could not save preview:", error)

    print("Total planes:", len(all_images))
    print("Skipped planes:", skipped_planes)

    print(
        "Plane processing FPS:",
        round(len(all_images) / elapsed, 2)
        if elapsed > 0
        else "N/A"
    )

    print("Video FPS:", VIDEO_FPS)
    print("Video saved:", mp4_file)


if __name__ == "__main__":
    main()
