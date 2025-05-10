from fLZc_python import calculate_lz76_complexity, calculate_lz78_complexity, FLZC

def test_lz_complexities_match_expected():
    s = "000101000101111010001010100010101000000010000010"
    assert calculate_lz76_complexity(s) == 9
    assert calculate_lz78_complexity(s) == 16

def test_lz_dictionaries_are_correct_length():
    s = "000101000101111010001010100010101000000010000010"
    flzc = FLZC()
    c76, dict76 = flzc.calculate_lz76_with_dict(s)
    c78, dict78 = flzc.calculate_lz78_with_dict(s)

    assert isinstance(dict76, list)
    assert isinstance(dict78, list)
    assert c76 == 9
    assert c78 == 16
