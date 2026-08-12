#!/usr/bin/env python3
"""Run generated benchmark code in a small Bubblewrap sandbox."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


SYSTEM_PATHS = (Path("/usr"), Path("/bin"), Path("/lib"), Path("/lib64"))
RESOURCE_LIMITS = (
    "--as=1073741824",
    "--cpu=120",
    "--nproc=4096",
    "--fsize=67108864",
    "--nofile=256",
)


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
    return subprocess.run(
        command_for(candidate, command, read_only_mounts),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
        env={"PATH": os.environ.get("PATH", "")},
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
