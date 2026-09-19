from __future__ import annotations

from dataclasses import dataclass
import sys
from typing import Iterable


@dataclass(frozen=True)
class Provider:
    name: str
    available: bool = True
    local: bool = False


def select_provider(
    providers: Iterable[Provider],
    *,
    prefer_local: bool = True,
    allow_fallback: bool = True,
) -> Provider | None:
    candidates = [provider for provider in providers if provider.available]
    if not candidates:
        return None

    if prefer_local:
        for provider in candidates:
            if provider.local:
                return provider

    if allow_fallback:
        return candidates[0]

    return None


def run_selftest() -> bool:
    providers = [
        Provider(name="local", available=False, local=True),
        Provider(name="cloud", available=True, local=False),
    ]
    selected = select_provider(providers)
    return selected is not None and selected.name == "cloud"


if __name__ == "__main__":
    if sys.argv[1:] != ["selftest"]:
        print("usage: python -m runtime.provider_router selftest", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(0 if run_selftest() else 1)
