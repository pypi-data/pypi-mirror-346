# fLZc_python — Fast Lempel–Ziv Complexity for Python

A Python wrapper around the [fLZc C library](https://github.com/lcbarnett/fLZc), implementing the original LZ76c<sup>1</sup> and LZ78c<sup>2</sup> versions of complexity measures (with optional normalisation) in optimized C, exposed via a clean Python API.

## Features

- **LZ76c & LZ78c**: exact implementations of the original Lempel–Ziv algorithms  
- **Running complexity**: compute the complexity profile along a sequence  
- **Dictionary output**: retrieve the phrase dictionary used by the algorithm  
- **Normalisation**: theoretical or empirical scaling factors (as in the original fLZc)  
- **Pure-Python API** built on C for maximum speed (via ctypes)  
- **Works out-of-the-box** on macOS & Linux; Windows support untested  



## Installation (Development Mode)

This project uses scikit-build-core + CMake under PEP 517.

### Prerequisites

- Python 3.8–3.13  
- pip, a C99-compatible compiler, and CMake ≥ 3.15  
- macOS or Linux (Windows support not yet tested)  

### Step by step

Clone and install in editable mode:

```bash
git clone https://github.com/romybeaute/fLZc_python.git
cd fLZc_python
python -m venv .flzcvenv
source .flzcvenv/bin/activate

# clean previous builds (optional)
rm -rf build/ dist/ _skbuild/ fLZc_python/liblzc.*

# install in editable mode (builds & places the shared library)
pip install -e .
```


### Examples & Testing
- Demo:\\
fLZc_python/examples/lzc_demo.py provides an end-to-end example (including plotting).

- Unit tests:\\
Run pytest tests/ to verify correctness on canonical sequences.



### Implementation Details
- **LZ76c** follows the algorithm of Kaspar & Schuster <sup>1</sup>, with optional dictionary retrieval and running-profile support.  
- **LZ78c** leverages the khashl hash-map for linear-time parsing and also supports dictionary & running outputs.  
- **Normalisation** factors are precomputed (via MATLAB data) for alphabets up to size 10; see the original MATLAB repo for details.


### Acknowledgements
Wraps the original **fLZc** library by Lionel Barnett (University of Sussex).



## License

Distributed under the MIT License. See `LICENSE` for details.



## References
1. A. Lempel & J. Ziv, “On the Complexity of Finite Sequences,” _IEEE Trans. Inf. Theory_ 22(1), 1976.  
2. A. Lempel & J. Ziv, “Compression of Individual Sequences via Variable-Rate Coding,” _IEEE Trans. Inf. Theory_ 24(5), 1978.  
3. F. Kaspar & H. G. Schuster, “Easily Calculable Measure for the Complexity of Spatiotemporal Patterns,” _Phys. Rev. A_ 36(2), 1987. 