import numpy as np
import matplotlib.pyplot as plt
from fLZc_python.python_wrapper.flzc import FLZC, calculate_lz76_complexity, calculate_lz78_complexity
from fLZc_python.python_wrapper.LZc_binarise import LZc_binarise
from fLZc_python.python_wrapper.LZc_normfac import LZcNormaliser

from fLZc_python import FLZC



'''
check if correspods to what we get with matlab version
with matlab (running LZc_demo.m), we get:

input sequence = 000101000101111010001010100010101000000010000010

alphabet size   =   2
sequence length =  48

LZ76c =   9
LZ78c =  16

LZ76c dictionary: 0.001.0100.01011.110.10001010.1000101010000.000100.00010
LZ78c dictionary: 0.00.1.01.000.10.11.110.100.010.101.0001.0101.0000.00010.00001.


'''

def main():
    # Define the input sequence
    s = '000101000101111010001010100010101000000010000010'

    # Alphabet size and sequence length
    unique_chars = set(s)
    a = len(unique_chars)  # Should be 2 for binary
    n = len(s)

    print(f"\nInput sequence = {s}")
    print(f"\nAlphabet size   = {a:3d}")
    print(f"Sequence length = {n:3d}")

    # Initialise FLZC calculator
    flzc = FLZC()
    normaliser = LZcNormaliser()

    # Calculate LZ76 and LZ78 complexities
    c76 = calculate_lz76_complexity(s)
    c78 = calculate_lz78_complexity(s)  

    print(f"\nLZ76c = {c76:3d}")
    print(f"LZ78c = {c78:3d}")

    # Calculate with dictionaries (requires C implementation support)
    c76_dict, dict76 = flzc.calculate_lz76_with_dict(s)
    c78_dict, dict78 = flzc.calculate_lz78_with_dict(s)  

    print(f"\nLZ76c dictionary: {dict76}")
    print(f"LZ78c dictionary: {dict78}\n")

    # Calculate running complexities 
    running_c76 = flzc.running_lz76_complexity(s)
    running_c78 = flzc.running_lz78_complexity(s)  

    ### Normalisation factors ###
    # Get theoretical values for LZ76 and LZ78 (load from data files)

    # apply MATLAB-style normalisation factors (with +1 indexing)
    all_lengths = np.arange(1, n+1)
    norm_factors_76 = normaliser.get_norm_factors(all_lengths, a, 76)
    norm_factors_78 = normaliser.get_norm_factors(all_lengths, a, 78)

    #apply normalisation factors
    crn76 = running_c76 / norm_factors_76
    crn78 = running_c78 / norm_factors_78

    plt.figure(figsize=(10, 6))
    plt.suptitle(f'LZ76c and LZ78c: alphabet size = {a}, sequence length = {n}\n')

    # plot for Unnormalised LZc values
    plt.subplot(2, 1, 1)
    plt.plot(range(1, n+1), running_c76, label='LZ76c')
    plt.plot(range(1, n+1), running_c78, label='LZ78c')
    plt.xlim([0, n+1])
    plt.title('Unnormalised')
    plt.xlabel('Sequence length')
    plt.legend()
    plt.grid(True)

    # plot for Normalised LZc values
    plt.subplot(2, 1, 2)
    plt.plot(range(1, n+1), crn76, label='LZ76c')
    plt.plot(range(1, n+1), crn78, label='LZ78c')
    plt.xlim([0, n+1])
    plt.ylim([0, 1.05*max(np.max(crn76), np.max(crn78))])
    plt.title('Normalised')
    plt.xlabel('Sequence length')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    return c76,c78

if __name__ == "__main__":
    main()