#!/usr/bin/env python
"""
Script to verify deployment files and data
"""
import os
import sys
import json

def check_files():
    """Check if all required deployment files exist"""
    required_files = [
        'render.yaml',
        'build.sh',
        'requirements.txt',
        'export_data.py',
        'import_data.py',
        'deploy_to_render.py',
        'RENDER_DEPLOYMENT.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✓ All required deployment files present")
    return True

def check_fixtures():
    """Check if fixtures directory exists and has data"""
    if not os.path.exists('fixtures'):
        print("⚠ Fixtures directory not found")
        return False
    
    fixtures = os.listdir('fixtures')
    if not fixtures:
        print("⚠ Fixtures directory is empty")
        return False
    
    print(f"✓ Found {len(fixtures)} fixture files:")
    for fixture in fixtures:
        print(f"  - {fixture}")
    
    return True

def check_build_script():
    """Check if build script has correct permissions and content"""
    if not os.path.exists('build.sh'):
        print("⚠ build.sh not found")
        return False
    
    # Check if build.sh is executable
    if os.name != 'nt':  # Not Windows
        import stat
        st = os.stat('build.sh')
        if not (st.st_mode & stat.S_IEXEC):
            print("⚠ build.sh is not executable")
            return False
    
    print("✓ build.sh script is properly configured")
    return True

def check_render_config():
    """Check render.yaml configuration"""
    if not os.path.exists('render.yaml'):
        print("⚠ render.yaml not found")
        return False
    
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
            if 'buildCommand: "./build.sh"' not in content:
                print("⚠ buildCommand not properly configured in render.yaml")
                return False
            if 'startCommand: "gunicorn' not in content:
                print("⚠ startCommand not properly configured in render.yaml")
                return False
    except Exception as e:
        print(f"⚠ Error reading render.yaml: {e}")
        return False
    
    print("✓ render.yaml configuration is correct")
    return True

def main():
    """Main verification function"""
    print("=== TakeOpinion Deployment Verification ===")
    
    checks = [
        check_files,
        check_fixtures,
        check_build_script,
        check_render_config
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("=== All deployment checks passed! ===")
        print("Your application is ready for deployment to Render.")
        print("Run commit_and_deploy.bat to commit changes and deploy.")
    else:
        print("=== Some deployment checks failed ===")
        print("Please fix the issues before deploying.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)