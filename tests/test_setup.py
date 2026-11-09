def test_python_setup():
    """Test that the Python setup is correct."""
    import sys
    assert sys.version_info >= (3, 6), "Python version must be 3.6 or higher"