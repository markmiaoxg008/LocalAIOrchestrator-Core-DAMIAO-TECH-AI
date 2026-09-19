#!/usr/bin/env python3
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Mapping, Sequence


MACOS_GUI_EXECUTABLE_DIRS = (
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/usr/bin",
    "/bin",
    "/usr/sbin",
    "/sbin",
)


def resolve_executable(
    executable: str,
    *,
    path: str | None = None,
    system: str | None = None,
    macos_directories: Sequence[str] = MACOS_GUI_EXECUTABLE_DIRS,
) -> str | None:
    """Resolve a command without invoking a shell or reading shell profiles."""
    candidate = Path(executable).expanduser()
    if candidate.is_absolute():
        return str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None

    resolved = shutil.which(executable, path=path)
    if resolved:
        return str(Path(resolved).absolute())

    if (system or platform.system()) != "Darwin":
        return None

    for directory in macos_directories:
        fallback = Path(directory) / executable
        if fallback.is_file() and os.access(fallback, os.X_OK):
            return str(fallback.absolute())
    return None


def run_resolved_command(
    command: Sequence[str],
    *,
    timeout: float = 5,
    env: Mapping[str, str] | None = None,
    path: str | None = None,
    system: str | None = None,
    macos_directories: Sequence[str] = MACOS_GUI_EXECUTABLE_DIRS,
) -> dict[str, Any]:
    started = time.monotonic()
    requested = [str(item) for item in command]
    if not requested:
        return {
            "status": "BLOCKED",
            "command": requested,
            "reason": "COMMAND_NOT_FOUND",
            "resolved_executable": None,
            "duration_ms": 0,
        }

    process_env = dict(os.environ if env is None else env)
    search_path = path if path is not None else process_env.get("PATH")
    resolved = resolve_executable(
        requested[0],
        path=search_path,
        system=system,
        macos_directories=macos_directories,
    )
    if not resolved:
        return {
            "status": "BLOCKED",
            "command": requested,
            "reason": "COMMAND_NOT_FOUND",
            "resolved_executable": None,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }

    executed = [resolved, *requested[1:]]
    try:
        proc = subprocess.run(
            executed,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=process_env,
            shell=False,
        )
        return {
            "status": "PASS" if proc.returncode == 0 else "PARTIAL",
            "command": requested,
            "executed_command": executed,
            "resolved_executable": resolved,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip()[-1200:],
            "stderr": proc.stderr.strip()[-1200:],
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "BLOCKED",
            "command": requested,
            "executed_command": executed,
            "resolved_executable": resolved,
            "reason": "TIMEOUT",
            "stdout": (exc.stdout or "")[-1200:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-1200:] if isinstance(exc.stderr, str) else "",
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
