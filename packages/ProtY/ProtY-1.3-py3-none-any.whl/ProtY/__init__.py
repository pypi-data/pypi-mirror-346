from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("ProtY")
except PackageNotFoundError:
    __version__ = "1.0"