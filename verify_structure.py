#!/usr/bin/env python
"""
Verify the package structure and imports
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Current directory:", current_dir)
print("Python path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

print("\nDirectory structure:")
for root, dirs, files in os.walk("."):
    level = root.replace(current_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")

print("\nTesting imports:")
try:
    import takeopinion
    print("✓ takeopinion package imported successfully")
except Exception as e:
    print(f"✗ Failed to import takeopinion: {e}")

try:
    import takeopinion.settings
    print("✓ takeopinion.settings imported successfully")
except Exception as e:
    print(f"✗ Failed to import takeopinion.settings: {e}")

try:
    import takeopinion.settings_prod
    print("✓ takeopinion.settings_prod imported successfully")
except Exception as e:
    print(f"✗ Failed to import takeopinion.settings_prod: {e}")

try:
    import takeopinion.wsgi
    print("✓ takeopinion.wsgi imported successfully")
except Exception as e:
    print(f"✗ Failed to import takeopinion.wsgi: {e}")

# Check if there are any files with incorrect names
print("\nChecking for incorrect file names:")
for root, dirs, files in os.walk("."):
    for file in files:
        if "akeopinion" in file:
            print(f"Found file with 'akeopinion': {os.path.join(root, file)}")
    for dir in dirs:
        if "akeopinion" in dir:
            print(f"Found directory with 'akeopinion': {os.path.join(root, dir)}")