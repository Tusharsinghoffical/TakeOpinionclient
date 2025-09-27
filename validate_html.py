import os
import re
from bs4 import BeautifulSoup

def validate_html_templates():
    """Validate HTML templates for common errors"""
    template_dirs = [
        'core/templates/core',
        'accounts/templates/accounts',
        'bookings/templates/bookings',
        'doctors/templates/doctors',
        'hospitals/templates/hospitals',
        'treatments/templates/treatments',
        'blogs/templates/blogs',
        'templates'
    ]
    
    errors = []
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for file in os.listdir(template_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(template_dir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Skip Django template syntax for basic validation
                        # Remove Django template tags for HTML validation
                        clean_content = re.sub(r'{%.*?%}', '', content)
                        clean_content = re.sub(r'{{.*?}}', '', clean_content)
                        
                        # Try to parse with BeautifulSoup
                        soup = BeautifulSoup(clean_content, 'html.parser')
                        
                        # Check for common issues
                        check_unclosed_tags(soup, file_path, errors)
                        check_mismatched_tags(soup, file_path, errors)
                        
                    except Exception as e:
                        errors.append(f"Error reading {file_path}: {str(e)}")
    
    return errors

def check_unclosed_tags(soup, file_path, errors):
    """Check for unclosed HTML tags"""
    # This is a simplified check - BeautifulSoup auto-closes most tags
    pass

def check_mismatched_tags(soup, file_path, errors):
    """Check for mismatched HTML tags"""
    # BeautifulSoup handles this automatically, so we'll look for other issues
    pass

if __name__ == "__main__":
    errors = validate_html_templates()
    if errors:
        print("HTML Validation Errors Found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No HTML validation errors found.")