from __future__ import annotations

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    id: str
    name: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class Result:
    name: str
    returncode: int
    stdout: str
    stderr: str


class Color:
    GREEN = "\033[32m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


CHECKS = (
    Check(
        id="ruff-lint",
        name="Ruff lint",
        command=("ruff", "check", "."),
    ),
    Check(
        id="ruff-format",
        name="Ruff format",
        command=("ruff", "format", "--check", "."),
    ),
    Check(
        id="mypy",
        name="Mypy",
        command=("mypy", "src", "tests"),
    ),
    Check(
        id="pytest",
        name="Pytest",
        command=("pytest",),
    ),
)


def _color(text: str, color: str) -> str:
    if not sys.stdout.isatty() or "NO_COLOR" in os.environ:
        return text

    return f"{color}{text}{Color.RESET}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TrabeculAI quality checks.")

    parser.add_argument(
        "checks",
        nargs="*",
        choices=["all", *(check.id for check in CHECKS)],
        help="Checks to run. Defaults to all.",
    )

    return parser.parse_args()


def select_checks(requested: list[str]) -> tuple[Check, ...]:
    if not requested or "all" in requested:
        return CHECKS

    requested_ids = set(requested)

    return tuple(check for check in CHECKS if check.id in requested_ids)


def run_check(check: Check) -> Result:
    process = subprocess.run(
        check.command,
        capture_output=True,
        text=True,
        check=False,
    )

    return Result(
        name=check.name,
        returncode=process.returncode,
        stdout=process.stdout.strip(),
        stderr=process.stderr.strip(),
    )


def print_result(result: Result) -> None:
    passed = result.returncode == 0

    status = _color(
        "PASSED" if passed else "FAILED",
        Color.GREEN if passed else Color.RED,
    )

    name = _color(result.name, Color.CYAN)

    print()
    print(_color("=" * 72, Color.YELLOW))
    print(f"{name}: {status}")
    print(_color("=" * 72, Color.YELLOW))

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)


def main() -> int:
    args = parse_args()
    checks_to_run = select_checks(args.checks)
    with ThreadPoolExecutor(max_workers=len(checks_to_run)) as executor:
        results = list(executor.map(run_check, checks_to_run))

    for result in results:
        print_result(result)

    failed = [result for result in results if result.returncode != 0]

    if failed:
        print()

        failed_names = ", ".join(_color(result.name, Color.RED) for result in failed)
        print(_color("Quality checks failed: ", Color.RED) + failed_names)

        return 1

    print()
    print(_color("✓ All quality checks passed.", Color.GREEN + Color.BOLD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
