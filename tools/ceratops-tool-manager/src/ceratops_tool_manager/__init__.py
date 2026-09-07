"""Deterministic local tool deployment; source stays in the owning repository."""

from importlib.metadata import PackageNotFoundError, version

TOOL_ID = "ceratops-tool-manager"
try:
    __version__ = version(TOOL_ID)
except PackageNotFoundError:
    __version__ = "source"
