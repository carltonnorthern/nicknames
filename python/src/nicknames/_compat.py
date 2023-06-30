from contextlib import contextmanager
from pathlib import Path

try:
    from importlib.resources import as_file, files

    # This is the new way, but it's not available in Python 3.9+
    @contextmanager
    def load_resource(package: str, resource: str) -> Path:
        """
        Load a resource from a package. Returns a context manager that yields a Path.
        """
        with as_file(files(package).joinpath(resource)) as f:
            yield f

except ImportError:
    from importlib.resources import path

    # This is the old way, deprecated starting in Python 3.11
    @contextmanager
    def load_resource(package: str, resource: str) -> Path:
        """
        Load a resource from a package. Returns a context manager that yields a Path.
        """
        with path(package, resource) as f:
            yield f
