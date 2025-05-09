import tuxparse


def test_version():
    assert type(tuxparse.__version__) is str
