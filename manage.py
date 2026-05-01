#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Use the DJANGO_SETTINGS_MODULE environment variable if set, otherwise default to takeopinion.settings for development
    # Explicitly check for truncated module name and fix it
    settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "takeopinion.settings")
    
    # Debug: Print the settings module being used
    print(f"manage.py: Using DJANGO_SETTINGS_MODULE: {settings_module}")
    
    # Check if the module name has been truncated and fix it
    if settings_module.startswith("akeopinion."):
        corrected_module = "t" + settings_module
        print(f"manage.py: Correcting truncated module name from {settings_module} to {corrected_module}")
        os.environ["DJANGO_SETTINGS_MODULE"] = corrected_module
        settings_module = corrected_module
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()