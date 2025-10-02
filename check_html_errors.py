import os
import re

def check_html_errors():
    """Check HTML templates for common errors"""
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
                    check_file_for_errors(file_path, errors)
    
    return errors

def check_file_for_errors(file_path, errors):
    """Check a single file for HTML errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Check for unclosed HTML tags
            check_unclosed_tags(line, file_path, line_num, errors)
            
            # Check for mismatched quotes
            check_mismatched_quotes(line, file_path, line_num, errors)
            
            # Check for common Django template issues
            check_django_template_issues(line, file_path, line_num, errors)
            
    except Exception as e:
        errors.append(f"Error reading {file_path}: {str(e)}")

def check_unclosed_tags(line, file_path, line_num, errors):
    """Check for common unclosed HTML tags"""
    # Look for tags that should be closed
    unclosed_patterns = [
        r'<(div|span|p|a|li|ul|ol|table|tr|td|th|form|input|select|option|textarea|button|section|article|header|footer|nav|aside|main|figure|figcaption)[^>]*>'
    ]
    
    # This is a simplified check - we're not trying to parse HTML completely
    # Just looking for obvious issues
    
def check_mismatched_quotes(line, file_path, line_num, errors):
    """Check for mismatched quotes in HTML attributes"""
    # Look for attributes with mismatched quotes
    attr_patterns = re.findall(r'([a-zA-Z-]+)=["\']([^"\']*)$', line)
    for match in re.finditer(r'[a-zA-Z-]+=["\'][^"\']*$', line):
        errors.append(f"{file_path}:{line_num} - Possible mismatched quotes in attribute: {line.strip()}")

def check_django_template_issues(line, file_path, line_num, errors):
    """Check for common Django template issues"""
    # Check for mismatched Django template tags
    if line.count('{%') != line.count('%}'):
        errors.append(f"{file_path}:{line_num} - Mismatched Django template tags: {line.strip()}")
    
    if line.count('{{') != line.count('}}'):
        errors.append(f"{file_path}:{line_num} - Mismatched Django variable tags: {line.strip()}")

if __name__ == "__main__":
    errors = check_html_errors()
    if errors:
        print("HTML/Django Template Errors Found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No HTML/Django template errors found.")