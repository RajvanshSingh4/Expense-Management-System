import sys
import os

# Get the project root directory (two levels up from test/conftest.py)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)