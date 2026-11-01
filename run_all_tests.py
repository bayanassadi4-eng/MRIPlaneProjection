
import csv
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

TEST_FILES = [
    "test_geometry.py",
    "test_reference_values.py",
    "test_tilted_reference.py",
    "test_pixel_rounding.py",
]

BENCHMARK_FILE = "benchmark.py"

REPORT_FILE = PROJECT_DIR / "test_report.txt"
HISTORY_FILE = PROJECT_DIR / "performance_history.csv"

# Baseline measured in the previous benchmark.
BASELINE_FPS = 146.86

# Warn if performance drops by more than 15%.
MAX_DROP_PERCENT = 15.0


def run_script(filename):
    start = time.perf_counter()

    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_DIR / filename)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )

        return {
            "name": filename,
            "passed": result.returncode == 0,
            "seconds": time.perf_counter() - start,
            "output": result.stdout.strip(),
            "errors": result.stderr.strip(),
        }

    except (OSError, subprocess.TimeoutExpired) as error:
        return {
            "name": filename,
            "passed": False,
            "seconds": time.perf_counter() - start,
            "output": "",
            "errors": str(error),
        }


def save_performance_history(fps, change, status):
    new_file = not HISTORY_FILE.exists()

    with open(
            HISTORY_FILE,
            "a",
            newline="",
            encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if new_file:
            writer.writerow([
                "Timestamp",
                "Processing_FPS",
                "Baseline_FPS",
                "Change_Percent",
                "Status",
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            round(fps, 2),
            BASELINE_FPS,
            round(change, 2),
            status,
        ])


def check_performance():
    print("\n" + "=" * 50)
    print("PERFORMANCE REGRESSION CHECK")
    print("=" * 50)

    result = run_script(BENCHMARK_FILE)

    if result["output"]:
        print(result["output"])

    if result["errors"]:
        print("BENCHMARK ERROR DETAILS:")
        print(result["errors"])

    if not result["passed"]:
        return {
            "status": "ERROR",
            "details": "Benchmark execution failed.",
            "fps": None,
        }

    match = re.search(
        r"Average processing FPS:\s*([0-9]+(?:\.[0-9]+)?)",
        result["output"]
    )

    if not match:
        return {
            "status": "ERROR",
            "details": "Could not find average FPS in benchmark output.",
            "fps": None,
        }

    current_fps = float(match.group(1))

    if current_fps <= 0:
        return {
            "status": "ERROR",
            "details": "Invalid benchmark FPS value.",
            "fps": None,
        }

    change_percent = (
            (current_fps - BASELINE_FPS)
            / BASELINE_FPS
            * 100
    )

    minimum_acceptable = (
            BASELINE_FPS * (1 - MAX_DROP_PERCENT / 100)
    )

    if current_fps < minimum_acceptable:
        status = "WARNING"
        details = (
            "PERFORMANCE WARNING: Processing speed "
            "dropped by more than "
            f"{MAX_DROP_PERCENT:.0f}%."
        )
    else:
        status = "OK"
        details = (
            "PERFORMANCE OK: No large regression detected."
        )

    print("\nBaseline FPS:", BASELINE_FPS)
    print("Current FPS:", current_fps)
    print("Change:", f"{change_percent:+.2f}%")
    print(
        "Warning threshold:",
        round(minimum_acceptable, 2),
        "FPS"
    )
    print(details)

    save_performance_history(
        current_fps,
        change_percent,
        status
    )

    return {
        "status": status,
        "details": details,
        "fps": current_fps,
        "change": change_percent,
    }


def main():
    print("=" * 50)
    print("MRI PROJECT - AUTOMATED TEST REPORT")
    print("=" * 50)

    results = []

    for filename in TEST_FILES:
        print(f"\nRunning {filename}...")

        result = run_script(filename)
        results.append(result)

        status = (
            "PASSED" if result["passed"]
            else "FAILED"
        )

        print(f"{filename}: {status}")
        print(f"Time: {result['seconds']:.3f} seconds")

        if result["output"]:
            print(result["output"])

        if result["errors"]:
            print("ERROR DETAILS:")
            print(result["errors"])

    passed_count = sum(
        result["passed"] for result in results
    )

    failed_count = len(results) - passed_count

    performance = check_performance()

    report = [
        "MRI PROJECT - AUTOMATED TEST REPORT",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        f"Python: {sys.version.split()[0]}",
        "",
    ]

    for result in results:
        status = (
            "PASSED" if result["passed"]
            else "FAILED"
        )

        report.extend([
            "=" * 50,
            f"Test file: {result['name']}",
            f"Status: {status}",
            f"Duration: {result['seconds']:.3f} seconds",
            "",
            "TEST OUTPUT:",
            result["output"] or "(No output)",
            "",
            "ERROR DETAILS:",
            result["errors"] or "(No errors)",
            "",
            ])

    report.extend([
        "=" * 50,
        "PERFORMANCE REGRESSION CHECK",
        f"Baseline FPS: {BASELINE_FPS}",
        f"Current FPS: {performance['fps']}",
        f"Status: {performance['status']}",
        f"Details: {performance['details']}",
        "",
        "=" * 50,
        f"Passed test files: {passed_count}",
        f"Failed test files: {failed_count}",
        f"Total test files: {len(results)}",
        ])

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\n" + "=" * 50)
    print("FINAL TEST SUMMARY")
    print("=" * 50)

    print("Passed test files:", passed_count)
    print("Failed test files:", failed_count)
    print("Total test files:", len(results))
    print("Performance status:", performance["status"])
    print("Report saved:", REPORT_FILE.name)

    if performance["fps"] is not None:
        print("History saved:", HISTORY_FILE.name)

    if failed_count or performance["status"] == "ERROR":
        print("RESULT: TEST SYSTEM REQUIRES ATTENTION")
        sys.exit(1)

    if performance["status"] == "WARNING":
        print("RESULT: TESTS PASSED, PERFORMANCE WARNING")
    else:
        print("RESULT: ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
