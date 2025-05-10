from fLZc_python.examples.lzc_demo import main

def test_demo_main_returns_expected():
    c76, c78 = main()
    assert isinstance(c76, int)
    assert isinstance(c78, int)