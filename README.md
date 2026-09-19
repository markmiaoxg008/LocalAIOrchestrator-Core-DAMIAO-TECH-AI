# Local AI Orchestrator Core — DAMIAO TECH AI

A minimal open-source subset of a larger local-first AI orchestration system.

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

A minimal public smoke check is available without exposing private orchestration logic:

    python3 -m runtime.provider_router selftest

This validates the public provider-routing component in isolation. Higher-level routing policy and private DAMIAO TECH AI orchestration are intentionally outside the scope of this repository.

## Status

Early-stage open-source runtime primitives extracted from an actively developed local-first AI orchestration project.
