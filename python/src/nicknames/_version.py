from importlib.metadata import version

_PACKAGE_NAME = "nicknames"

try:
    __version__ = version(_PACKAGE_NAME)
except Exception as e:
    import warnings

    __version__ = "0.0.0"
    warnings.warn(
        f"Could not find metadata for the package {_PACKAGE_NAME}, setting version to {__version__}: {e}"  # noqa: E501
    )
