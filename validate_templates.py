import os
import re

def validate_templates():
    """Validate Django templates for common issues"""
    template_dirs = [
        'core/templates/core',
        'accounts/templates/accounts',
        'bookings/templates/bookings'
    ]
    
    all_issues = []
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for file in os.listdir(template_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(template_dir, file)
                    issues = validate_single_template(file_path)
                    all_issues.extend(issues)
    
    return all_issues

def validate_single_template(file_path):
    """Validate a single template file"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Check for proper Django block structure
        block_starts = len(re.findall(r'{%\s*block\s+\w+\s*%}', content))
        block_ends = len(re.findall(r'{%\s*endblock\s*%}', content))
        
        if block_starts != block_ends:
            issues.append(f"{file_path}: Mismatched block tags - {block_starts} starts, {block_ends} ends")
        
        # Check for proper Django template tag structure
        template_tags = re.findall(r'{%.*?%}', content)
        for tag in template_tags:
            if not is_valid_django_tag(tag):
                issues.append(f"{file_path}: Invalid Django tag structure: {tag}")
        
        # Check for common HTML structure issues
        issues.extend(check_html_structure(content, file_path))
        
        # Check for form issues
        issues.extend(check_form_structure(content, file_path))
        
    except Exception as e:
        issues.append(f"{file_path}: Error reading file - {str(e)}")
    
    return issues

def is_valid_django_tag(tag):
    """Check if a Django tag has proper structure"""
    # Remove the {% and %} parts
    inner = tag[2:-2].strip()
    
    # Basic validation - this is simplified
    if not inner:
        return False
    
    return True

def check_html_structure(content, file_path):
    """Check for common HTML structure issues"""
    issues = []
    
    # Check for meta tags in proper location (should be in head)
    if '<meta' in content and not content.startswith('<!DOCTYPE') and not content.startswith('<html'):
        # This is a simplified check
        pass
    
    # Check for form tags
    form_starts = len(re.findall(r'<form', content, re.IGNORECASE))
    form_ends = len(re.findall(r'</form>', content, re.IGNORECASE))
    
    if form_starts != form_ends:
        issues.append(f"{file_path}: Mismatched form tags - {form_starts} starts, {form_ends} ends")
    
    return issues

def check_form_structure(content, file_path):
    """Check for form-specific issues"""
    issues = []
    
    # Look for forms with POST method but no CSRF token
    forms = re.findall(r'<form[^>]*method=["\']post["\'][^>]*>', content, re.IGNORECASE)
    for form in forms:
        if '{% csrf_token %}' not in content:
            # Check if it's in the same form context
            issues.append(f"{file_path}: Form with POST method missing CSRF token: {form}")
    
    return issues

if __name__ == "__main__":
    issues = validate_templates()
    if issues:
        print("Template Validation Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No template validation issues found.")