from __future__ import annotations

import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class Result:
    name: str
    returncode: int
    stdout: str
    stderr: str


CHECKS = (
    Check(
        name="Ruff lint",
        command=("ruff", "check", "."),
    ),
    Check(
        name="Ruff format",
        command=("ruff", "format", "--check", "."),
    ),
    Check(
        name="Mypy",
        command=("mypy", "src", "tests"),
    ),
    Check(
        name="Pytest",
        command=("pytest",),
    ),
)


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
    status = "PASSED" if result.returncode == 0 else "FAILED"

    print()
    print("=" * 72)
    print(f"{result.name}: {status}")
    print("=" * 72)

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)


def main() -> int:
    with ThreadPoolExecutor(max_workers=len(CHECKS)) as executor:
        results = list(executor.map(run_check, CHECKS))

    for result in results:
        print_result(result)

    failed = [result for result in results if result.returncode != 0]

    if failed:
        print()
        print("Quality checks failed: " + ", ".join(result.name for result in failed))
        return 1

    print()
    print("All quality checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
