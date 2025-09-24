#!/usr/bin/env python
"""
Debug script to check environment variables on Render
"""

import os

print("=== RENDER ENVIRONMENT DEBUG ===")
print(f"Current working directory: {os.getcwd()}")

# List all environment variables that might be relevant
print("\n=== RELEVANT ENVIRONMENT VARIABLES ===")
for key, value in os.environ.items():
    if 'django' in key.lower() or 'setting' in key.lower() or 'takeopinion' in key.lower() or 'akeopinion' in key.lower():
        print(f"{key}: {value}")

# Check if there are any files with problematic names
print("\n=== DIRECTORY CONTENTS ===")
try:
    items = os.listdir('.')
    print("Root directory items:")
    for item in sorted(items):
        marker = "[DIR]" if os.path.isdir(item) else "[FILE]"
        print(f"  {marker} {item}")
        
    if 'takeopinion' in items:
        print("\nFound 'takeopinion' directory")
        takeopinion_items = os.listdir('takeopinion')
        print("takeopinion directory items:")
        for item in sorted(takeopinion_items):
            marker = "[DIR]" if os.path.isdir(os.path.join('takeopinion', item)) else "[FILE]"
            print(f"  {marker} {item}")
    else:
        print("\nERROR: 'takeopinion' directory NOT found!")
        
except Exception as e:
    print(f"Error listing directory: {e}")

print("\n=== DEBUG COMPLETE ===")