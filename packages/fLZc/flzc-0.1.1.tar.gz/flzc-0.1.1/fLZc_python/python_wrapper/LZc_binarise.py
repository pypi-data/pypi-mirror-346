import numpy as np


def LZc_binarise(x: np.ndarray, use_mean: bool = False) -> str:
    """
    Convert numerical data to a binary string (0s and 1s).
    
    Args:
        x: Input numerical array.
        use_mean: If True, use mean instead of median for threshold.
        
    Returns:
        Binary string (e.g., '001011...')
    """
    assert x.ndim == 1, "Input must be a 1D array"
    threshold = np.mean(x) if use_mean else np.median(x)
    binary_arr = (x > threshold).astype(int)
    return ''.join(binary_arr.astype(str))  # '0' and '1' string