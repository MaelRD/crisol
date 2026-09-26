"""El Crisol: personal knowledge, learning and memory system."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("crisol")
except PackageNotFoundError:  # running from a source tree without installing
    __version__ = "0.0.0"
