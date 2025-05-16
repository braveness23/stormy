#!/usr/bin/env python3
import sys
import os
import pytest

def main():
    """Run all tests for the AI-CAD Workbench."""
    # Get the directory containing this script
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the parent directory to PYTHONPATH so tests can import the package
    sys.path.insert(0, os.path.dirname(root_dir))
    
    # Run pytest with common options
    args = [
        "Tests",  # Test directory
        "-v",     # Verbose output
        "--tb=short",  # Shorter traceback format
        "--import-mode=importlib",  # Use importlib for imports
    ]
    
    # Add any command line arguments passed to this script
    args.extend(sys.argv[1:])
    
    # Run the tests
    return pytest.main(args)

if __name__ == "__main__":
    sys.exit(main())
