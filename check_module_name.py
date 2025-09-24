#!/usr/bin/env python
"""
Check for module name truncation issues
"""

import os
import sys

def check_module_name_issues():
    print("=== CHECKING MODULE NAME ISSUES ===")
    
    # Simulate what might happen in Render environment
    settings_module = "takeopinion.settings_prod"
    print(f"Original settings module: {settings_module}")
    
    # Check for various types of truncation that might occur
    truncations = [
        settings_module[1:],  # Remove first character: "akeopinion.settings_prod"
        settings_module[:-1],  # Remove last character: "takeopinion.settings_pro"
        settings_module[2:],   # Remove first 2 chars: "keopinion.settings_prod"
        settings_module[:10],  # First 10 chars only: "takeopinion"
        settings_module[1:11], # Characters 1-11: "akeopinion"
    ]
    
    print("\nTesting possible truncations:")
    for i, truncated in enumerate(truncations, 1):
        print(f"  {i}. '{truncated}'")
    
    # Test importing each truncated version
    print("\nTesting imports of truncated versions:")
    import importlib
    for i, truncated in enumerate(truncations, 1):
        try:
            mod = importlib.import_module(truncated)
            print(f"  {i}. '{truncated}' - ✓ SUCCESS (This shouldn't happen!)")
        except ImportError as e:
            print(f"  {i}. '{truncated}' - ✗ FAILED (as expected): {e}")
        except Exception as e:
            print(f"  {i}. '{truncated}' - ✗ ERROR: {e}")
    
    # Check if any files or directories match these truncated names
    print("\nChecking for files/directories matching truncated names:")
    cwd = os.getcwd()
    items = os.listdir(cwd)
    
    for truncated in truncations:
        # Check if the first part of truncated name matches any directory
        first_part = truncated.split('.')[0]
        if first_part in items:
            print(f"  Found directory matching '{first_part}'")
        elif os.path.exists(first_part):
            print(f"  Found file/path matching '{first_part}'")
        else:
            print(f"  No match for '{first_part}'")

def main():
    check_module_name_issues()
    print("\n=== CHECK COMPLETE ===")

if __name__ == "__main__":
    main()