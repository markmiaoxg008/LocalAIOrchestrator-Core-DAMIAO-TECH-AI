import tempfile
from pathlib import Path

from runtime.atomic_file import atomic_write_bytes, atomic_write_text
from runtime.executable_resolution import resolve_executable, run_resolved_command
from runtime.provider_router import Provider, select_provider

from runtime.workspace_migration import migration_readiness


def test_atomic_write_bytes_and_text():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        binary = root / "a.bin"
        text = root / "b.txt"

        atomic_write_bytes(binary, b"abc")
        atomic_write_text(text, "hello")

        assert binary.read_bytes() == b"abc"
        assert text.read_text(encoding="utf-8") == "hello"


def test_executable_resolution_python():
    path = resolve_executable("python3")
    assert path is not None
    assert Path(path).is_file()

    result = run_resolved_command(
        ["python3", "-c", "print('oss-core-ok')"],
        timeout=10,
    )

    assert result["returncode"] == 0
    assert "oss-core-ok" in result["stdout"]


def test_workspace_migration_readiness():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        result = migration_readiness(root)

        assert isinstance(result, dict)
        assert "status" in result

def test_provider_routing_local_preference_and_fallback():
    providers = [
        Provider(name="cloud", available=True, local=False),
        Provider(name="local", available=True, local=True),
    ]
    assert select_provider(providers).name == "local"

    unavailable_local = [
        Provider(name="local", available=False, local=True),
        Provider(name="cloud", available=True, local=False),
    ]
    assert select_provider(unavailable_local).name == "cloud"


def test_atomic_write_replaces_existing_file():
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "state.txt"
        path.write_text("old", encoding="utf-8")
        atomic_write_text(path, "new")
        assert path.read_text(encoding="utf-8") == "new"


def test_run_resolved_command_blocks_empty_command():
    result = run_resolved_command([])
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "COMMAND_NOT_FOUND"
    assert result["resolved_executable"] is None


def test_run_resolved_command_blocks_missing_executable():
    result = run_resolved_command(
        ["damiao-definitely-missing-executable"],
        path="",
        system="Linux",
    )
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "COMMAND_NOT_FOUND"
    assert result["resolved_executable"] is None


def test_workspace_migration_readiness_blocks_missing_workspace():
    with tempfile.TemporaryDirectory() as td:
        missing = Path(td) / "missing"
        result = migration_readiness(missing)
        assert result["status"] == "BLOCKED"
        assert result["workspace_exists"] is False


def test_provider_routing_returns_none_when_all_unavailable():
    providers = [
        Provider(name="local", available=False, local=True),
        Provider(name="cloud", available=False, local=False),
    ]
    assert select_provider(providers) is None


def test_provider_routing_respects_disabled_fallback():
    providers = [
        Provider(name="cloud", available=True, local=False),
    ]
    assert select_provider(providers, prefer_local=True, allow_fallback=False) is None
