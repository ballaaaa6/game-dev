from pathlib import Path


class WorkspacePathError(ValueError):
    pass


def workspace_root(value=None):
    root = Path(value or Path(__file__).resolve().parents[2]).resolve()
    return root


def within_workspace(root, value):
    root = workspace_root(root)
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise WorkspacePathError(f"path is outside workspace: {path}") from exc
    return path


def relative_path(root, value):
    return within_workspace(root, value).relative_to(workspace_root(root)).as_posix()
