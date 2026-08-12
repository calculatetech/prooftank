#!/usr/bin/env python3
"""Run generated benchmark code in a small Bubblewrap sandbox."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


SYSTEM_PATHS = (Path("/usr"), Path("/bin"), Path("/lib"), Path("/lib64"))
MAX_OUTPUT_BYTES = 1024 * 1024
PROCESS_ALLOWANCE = 64
RESOURCE_LIMITS = (
    "--as=1073741824",
    "--cpu=120",
    f"--fsize={MAX_OUTPUT_BYTES}",
    "--nofile=256",
)


def uid_thread_count() -> int:
    total = 0
    uid_line = f"Uid:\t{os.getuid()}\t"
    for status in Path("/proc").glob("[0-9]*/status"):
        try:
            lines = status.read_text().splitlines()
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        if not any(line.startswith(uid_line) for line in lines):
            continue
        threads = next((line for line in lines if line.startswith("Threads:\t")), None)
        if threads:
            total += int(threads.split()[1])
    if total < 1:
        raise RuntimeError("could not establish current user thread count")
    return total


def command_for(
    candidate: Path,
    command: list[str],
    read_only_mounts: dict[Path, str] | None = None,
) -> list[str]:
    bubblewrap = shutil.which("bwrap")
    prlimit = shutil.which("prlimit")
    if bubblewrap is None or prlimit is None:
        raise RuntimeError("bwrap and prlimit are required for generated code")
    candidate = candidate.resolve(strict=True)
    if not candidate.is_dir():
        raise ValueError(f"candidate is not a directory: {candidate}")
    wrapped = [
        prlimit,
        *RESOURCE_LIMITS,
        f"--nproc={uid_thread_count() + PROCESS_ALLOWANCE}",
        bubblewrap,
        "--die-with-parent",
        "--new-session",
        "--unshare-all",
    ]
    for path in SYSTEM_PATHS:
        if path.exists():
            wrapped.extend(("--ro-bind", str(path), str(path)))
    wrapped.extend(
        (
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--tmpfs",
            "/tmp",
            "--dir",
            "/candidate",
            "--ro-bind",
            str(candidate),
            "/candidate",
        )
    )
    for source, target in (read_only_mounts or {}).items():
        source = source.resolve(strict=True)
        if not target.startswith("/") or ".." in Path(target).parts:
            raise ValueError(f"invalid sandbox target: {target}")
        wrapped.extend(("--dir", target, "--ro-bind", str(source), target))
    wrapped.extend(
        (
            "--clearenv",
            "--setenv",
            "HOME",
            "/tmp",
            "--setenv",
            "PATH",
            "/usr/bin:/bin",
            "--setenv",
            "PYTHONDONTWRITEBYTECODE",
            "1",
            "--setenv",
            "TMPDIR",
            "/tmp",
            "--chdir",
            "/candidate",
            *command,
        )
    )
    return wrapped


def run(
    candidate: Path,
    command: list[str],
    *,
    read_only_mounts: dict[Path, str] | None = None,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    wrapped = command_for(candidate, command, read_only_mounts)
    with (
        tempfile.TemporaryFile(mode="w+") as stdout,
        tempfile.TemporaryFile(mode="w+") as stderr,
    ):
        completed = subprocess.run(
            wrapped,
            check=False,
            stdout=stdout,
            stderr=stderr,
            text=True,
            timeout=timeout,
            env={"PATH": os.environ.get("PATH", "")},
        )
        stdout.seek(0)
        stderr.seek(0)
        return subprocess.CompletedProcess(
            wrapped,
            completed.returncode,
            stdout.read(MAX_OUTPUT_BYTES),
            stderr.read(MAX_OUTPUT_BYTES),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--mount", action="append", default=[])
    args, command = parser.parse_known_args()
    command = command[1:] if command[:1] == ["--"] else command
    if not command:
        parser.error("a command is required after --")
    mounts = {}
    for value in args.mount:
        source, separator, target = value.partition("=")
        if not separator:
            parser.error("mounts use SOURCE=TARGET")
        mounts[Path(source)] = target
    completed = run(
        args.candidate,
        command,
        read_only_mounts=mounts,
        timeout=args.timeout,
    )
    print(completed.stdout, end="")
    print(completed.stderr, end="", file=__import__("sys").stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
