# Contributing

Thank you for your interest in Local AI Orchestrator Core — DAMIAO TECH AI.

## Scope

This repository contains a small open-source subset of a larger private system. Contributions should stay within the publicly documented runtime primitives.

## Before Submitting

1. Open a GitHub Issue describing the bug, improvement, or proposal.
2. Keep changes small and focused.
3. Add or update tests when behavior changes.
4. Run the test suite before submitting a pull request.

## Tests

    python3 -m pytest -q
    python3 -m runtime.provider_router selftest

## Pull Requests

Pull requests should explain the problem, the change, and how it was verified. All pull requests must pass CI.
