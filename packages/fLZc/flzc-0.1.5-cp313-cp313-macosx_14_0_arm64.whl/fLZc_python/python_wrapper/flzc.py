import ctypes
import numpy as np
from typing import Tuple
import os
import sys
import importlib.resources as pkg_res

DSEPCHAR = '.'




class FLZC:
    def __init__(self, lib_path=None):
        ext = {
            "darwin": ".dylib",
            "linux":  ".so",
            "win32":  ".dll",
        }.get(sys.platform, ".so")

        if lib_path is None:
            base = os.path.dirname(os.path.abspath(__file__))
            # 1) source‐tree copy
            candidate = os.path.abspath(os.path.join(base, os.pardir, "liblzc" + ext))
            if os.path.exists(candidate):
                lib_path = candidate
            else:
                # 2) installed package copy
                try:
                    pkg_root = pkg_res.files("fLZc_python")
                    candidate2 = str(pkg_root / f"liblzc{ext}")
                    if os.path.exists(candidate2):
                        lib_path = candidate2
                    else:
                        lib_path = candidate
                except Exception:
                    lib_path = candidate

        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"liblzc{ext} not found at: {lib_path}")

        self.lib = ctypes.CDLL(lib_path)
        self._define_prototypes()
        
    
    def _define_prototypes(self):
        # define original C function names (defined in C scripts)

        # ========== LZ76 Functions ==========
        self.lib.LZ76c.argtypes = [ctypes.c_char_p] #load using ctypes (ctypes.CDLL(lib_path))
        self.lib.LZ76c.restype = ctypes.c_size_t
        
        self.lib.LZ76cd.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        self.lib.LZ76cd.restype = ctypes.c_size_t
        
        self.lib.LZ76cr.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)]
        self.lib.LZ76cr.restype = None
        
        self.lib.LZ76crd.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_char)]
        self.lib.LZ76crd.restype = None

        # ========== LZ78 Functions ==========
        self.lib.LZ78c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
        self.lib.LZ78c.restype = ctypes.c_size_t
        
        self.lib.LZ78cr.argtypes = [
            ctypes.c_char_p, 
            ctypes.POINTER(ctypes.c_char), 
            ctypes.POINTER(ctypes.c_size_t)
        ]
        self.lib.LZ78cr.restype = None

    # ========== LZ76 Methods ==========
    def calculate_lz76_complexity(self, binary_str: str) -> int:
        return self.lib.LZ76c(binary_str.encode('utf-8'))
    
    def calculate_lz76_with_dict(self, binary_str: str) -> Tuple[int, list]:
        max_dict_len = 2 * len(binary_str) + 2 # from DLEN(n)
        dict_buf = (ctypes.c_char * max_dict_len)() # buffer of size DLEN(n)
        # call C function
        # print(f"Binary string: {binary_str}")
        # print(f"Encoded binary string: {binary_str.encode('utf-8')}")
        c = self.lib.LZ76cd(binary_str.encode('utf-8'), dict_buf)
        dict_str = dict_buf.value.decode('utf-8')
        patterns = dict_str.split(DSEPCHAR)  # split sequence using the separator
        return c, patterns
    
    def running_lz76_complexity(self, binary_str: str) -> np.ndarray:
        n = len(binary_str)
        c_arr = (ctypes.c_size_t * n)()
        self.lib.LZ76cr(binary_str.encode('utf-8'), c_arr)
        return np.array(c_arr)
    

    # ========== LZ78 Methods ==========
    def calculate_lz78_complexity(self, binary_str: str) -> int:
        """Returns complexity and automatically populates dictionary"""
        # append NUL terminator for C strings
        c_str = (binary_str + '\0').encode('utf-8')
        max_dict_len = 2 * len(binary_str) + 2
        dict_buf = (ctypes.c_char * max_dict_len)()
        c = self.lib.LZ78c(c_str, dict_buf)
        return c

    def calculate_lz78_with_dict(self, binary_str: str) -> Tuple[int, list]:
        max_dict_len = 2 * len(binary_str) + 2
        dict_buf = (ctypes.c_char * max_dict_len)()
        c_str = (binary_str + '\0').encode('utf-8')  # esure NUL termination
        c = self.lib.LZ78c(c_str, dict_buf)
        
        # decode and split on DSEPCHAR (.)
        dict_str = dict_buf.value.decode('utf-8', errors='ignore')
        patterns = [p for p in dict_str.split('.') if p]  # split on '.' and filter empties
        
        return c, patterns

    def running_lz78_complexity(self, binary_str: str) -> np.ndarray:
        n = len(binary_str)
        c_arr = (ctypes.c_size_t * n)()  # correct type for running complexities
        max_dict_len = 2 * n + 2
        dict_buf = (ctypes.c_char * max_dict_len)()
        c_str = (binary_str + '\0').encode('utf-8')
        self.lib.LZ78cr(c_str, dict_buf, c_arr)  # pass dict_buf and c_arr
        return np.array(c_arr)
    



# ========== Convenience Functions ==========
def calculate_lz76_complexity(binary_str: str) -> int:
    return FLZC().calculate_lz76_complexity(binary_str)

def calculate_lz78_complexity(binary_str: str) -> int:
    return FLZC().calculate_lz78_complexity(binary_str)