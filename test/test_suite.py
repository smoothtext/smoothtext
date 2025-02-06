import pytest
import sys
import os

# Add the src directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)


def run_tests():
    """Run all tests in the project"""
    test_path = os.path.dirname(__file__)
    return pytest.main([test_path])


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
