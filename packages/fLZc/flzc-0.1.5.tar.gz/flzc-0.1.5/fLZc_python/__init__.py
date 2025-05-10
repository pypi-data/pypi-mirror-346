# fLZc_python/__init__.py
from .python_wrapper.flzc import (FLZC,calculate_lz76_complexity,calculate_lz78_complexity)
from .python_wrapper import LZc_binarise       
from .python_wrapper import LZc_normfac


try:
    from importlib.metadata import version
    __version__ = version("fLZc")
except ImportError:
    __version__ = "unknown"


__all__ = [
    'FLZC',
    'calculate_lz76_complexity', 
    'calculate_lz78_complexity',
    'LZc_binarise',
    'LZc_normfac'
]
