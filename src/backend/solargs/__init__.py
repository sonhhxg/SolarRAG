"""SON-GPT: Next Generation Data Interaction Solution with LLMs.
"""
from solargs import _version  # noqa: E402

_CORE_LIBS = ["api", "core"]

_LIBS = _CORE_LIBS


__version__ = _version.version

__ALL__ = ["__version__"]


def __getattr__(name: str):
    # Lazy load
    import importlib

    if name in _LIBS:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")