#!/usr/bin/env python3
"""
Reproduce the BytesWarning issue with --setup-show and bytes parameters
"""
import sys
import tempfile
import os

# Add pytest source to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_bytes_warning():
    """Test the bytes warning issue"""
    # Create a temporary test file
    test_content = '''
import pytest

@pytest.mark.parametrize('data', [b'Hello World'])
def test_data(data):
    pass
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        test_file = f.name
    
    try:
        # Import and run pytest programmatically
        import pytest
        
        # Run with -bb equivalent and --setup-show
        old_argv = sys.argv
        sys.argv = ['pytest', '--setup-show', test_file, '-v']
        
        # Enable BytesWarning
        import warnings
        warnings.filterwarnings('error', category=BytesWarning)
        
        # Run pytest
        exit_code = pytest.main()
        print(f"Exit code: {exit_code}")
        
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sys.argv = old_argv
        os.unlink(test_file)

if __name__ == "__main__":
    test_bytes_warning()