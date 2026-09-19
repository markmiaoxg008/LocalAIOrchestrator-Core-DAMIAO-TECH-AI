from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


def migration_readiness(root: Path) -> dict[str, Any]:
    workspace = Path(root).expanduser().resolve()
    dependencies = {
        "python": shutil.which("python3"),
        "git": shutil.which("git"),
    }
    missing = [name for name, path in dependencies.items() if path is None]

    return {
        "status": "PASS" if workspace.is_dir() and not missing else "BLOCKED",
        "workspace": str(workspace),
        "workspace_exists": workspace.is_dir(),
        "dependencies": dependencies,
        "required_missing": missing,
    }
