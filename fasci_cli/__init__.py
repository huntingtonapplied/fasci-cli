"""fasci CLI — Campaign management from your terminal."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("fasci-cli")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
