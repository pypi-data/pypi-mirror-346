import numpy as np
import scipy.io as sio
from pathlib import Path
import os


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
% LZc normalisation factors.

The normalisation divides the actual LZ complexity by the expected complexity of random sequences
Produces a ratio where:
≈1 means sequence is as complex as a random one
<1 means less complex than random
> 1 means more complex than random (rare but possible for short sequences)

The expected complexity for random sequences must be pre-computed through:
1. Generating many random sequences (e.g., 10,000 per length)
2. Calculating their LZ complexity
3. Computing statistics (means and (optionally) variance)
=> comp expensive so Binary normalisation data saved into .mat files (to be downloaded from: http://users.sussex.ac.uk/~lionelb/downloads/fLZc_data.zip)


% Returns means and (optionally) variances of LZc for random sequences with the supplied
% lengths and alphabet size from data files, as available.


% DEPRECATED AS NOT FIT FOR PURPOSE: If 'asymp' is true, then returns theoretical asymptotic
% upper bound values.

% n        vector of sequence lengths
% a        alphabet size
% ver      LZc version: 76 or 78
% asymp    DEPRECATED (flag for asymptotic vs. random normalisation)

% OUTPUT

% cm       random sequence mean LZc (or theoretical ceilings if asymp = false)
% ns       random sequence sample size
% cv       random sequence variances, if available
% cx       random sequence maxima, if available
"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class LZcNormaliser:
    def __init__(self, data_path="/Users/rbeaute/Projects/Pipeline4Complexity/fLZc/matlab/data"):
        """
        Initialise with path to data files relative to script location
        
        Args:
            data_path: Relative path from THIS script to the data folder
                      Default assumes 'fLZc_data' folder is in same directory
        """
        script_dir = Path(__file__).parent
        self.data_path = (script_dir / data_path).resolve()
        self.cache = {}
        
        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Data directory not found at: {self.data_path}\n"
                "Please either:\n"
                "1. Place the 'fLZc_data' folder in the same directory as this script, or\n"
                "2. Specify the correct relative path to the data folder"
            )
        
    def _load_mat_file(self, filepath):
        """Load MATLAB .mat file and extract relevant variables"""
        mat_data = sio.loadmat(filepath)
        return {
            'nmax': mat_data['nmax'][0,0],
            'cmean': mat_data['cmean'].flatten(),
            'cvar': mat_data.get('cvar', np.array([])).flatten(),
            'cmax': mat_data.get('cmax', np.array([])).flatten(),
            'nsamples': mat_data.get('nsamples', np.array([np.nan]))[0,0]
        }
    
    def get_norm_factors(self, n, alphabet_size, method):
        """
        Identical to MATLAB's LZc_normfac implementation
        
        Parameters:
            n: Sequence length(s) (int or array-like)
            alphabet_size: Alphabet size (int > 1)
            method: 76 (LZ76) or 78 (LZ78)
            
        Returns:
            Array of normalization factors matching MATLAB's output exactly
        """
        # Validate inputs
        n = np.asarray(n)
        if not np.all(n == np.floor(n)) or np.any(n <= 0):
            raise ValueError("Sequence lengths must be positive integers")
        if not isinstance(alphabet_size, int) or alphabet_size < 2:
            raise ValueError("Alphabet size must be integer > 1")
        if method not in [76, 78]:
            raise ValueError("Method must be 76 or 78")
        
        # Check cache or load data
        cache_key = f"LZ{method}c_a{alphabet_size:02d}"
        if cache_key not in self.cache:
            data_file = self.data_path / f"LZ{method}c_rand_a{alphabet_size:02d}.mat"
            if not data_file.exists():
                raise FileNotFoundError(
                    f"Normalization data file not found: {data_file}\n"
                    "Please download from:\n"
                    "http://users.sussex.ac.uk/~lionelb/downloads/fLZc_data.zip"
                )
            self.cache[cache_key] = self._load_mat_file(data_file)
        
        data = self.cache[cache_key]
        nmax = data['nmax']
        
        # Initialize output with NaN for lengths beyond available data
        cm = np.full_like(n, np.nan, dtype=float)
        
        # For valid lengths (n <= nmax), get the mean values
        valid_mask = n <= nmax
        valid_n = n[valid_mask]
        
        # MATLAB uses 1-based indexing, so we subtract 1
        cm[valid_mask] = data['cmean'][valid_n - 1]
        
        return cm