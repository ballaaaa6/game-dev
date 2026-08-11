#!/usr/bin/env python3
"""Shared paths for phase artifacts.

Keeping these paths in one small module prevents generated manifests from
drifting back into the workspace root when a phase script is rerun.
"""

from __future__ import annotations

from pathlib import Path


def phase_root(workspace: Path, phase: int | str) -> Path:
    return workspace / "Phases" / f"Phase{phase}"


def phase_artifacts_dir(workspace: Path, phase: int | str) -> Path:
    return phase_root(workspace, phase) / "artifacts"


def phase_docs_dir(workspace: Path, phase: int | str) -> Path:
    return phase_root(workspace, phase) / "docs"


def phase_references_dir(workspace: Path, phase: int | str) -> Path:
    return phase_root(workspace, phase) / "references"


def workspace_relative(path: Path, workspace: Path) -> str:
    return path.relative_to(workspace).as_posix()
