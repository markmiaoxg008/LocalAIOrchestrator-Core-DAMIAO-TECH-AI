# Local AI Orchestrator Core — DAMIAO TECH AI

Small, reusable Python runtime primitives for local-first AI applications. This project provides atomic persistence, safe executable resolution, simple local/cloud provider selection, and workspace readiness checks without requiring a full AI-agent framework.

## Included

- atomic file persistence
- executable resolution and controlled command execution
- provider routing with local/cloud failover
- workspace migration readiness checks

## Not Included

The following remain private and are intentionally not part of this repository:

- higher-level orchestration
- planner and task-contract logic
- memory intelligence
- capability evolution
- computer interaction
- repository intelligence
- product-specific logic
- private application architecture

## Requirements

- Python 3.11+
- macOS or Linux for generic runtime components

## Installation

Clone the repository, then install it in editable mode:

    python3 -m pip install -e .

## Tests

```bash
python3 -m pytest -q
python3 -m runtime.provider_router selftest
```

## Provider Routing Example

Use the public routing primitive directly:

```python
from runtime.provider_router import Provider, select_provider

providers = [
    Provider("local", available=False, local=True),
    Provider("cloud", available=True),
]

selected = select_provider(providers)
print(selected.name if selected else "none")  # cloud
```

A minimal public smoke check is also available:

    python3 -m runtime.provider_router selftest

This validates the public provider-routing component in isolation. Higher-level routing policy and private DAMIAO TECH AI orchestration are intentionally outside the scope of this repository.

## Status

Early-stage open-source runtime primitives extracted from an actively developed local-first AI orchestration project.
