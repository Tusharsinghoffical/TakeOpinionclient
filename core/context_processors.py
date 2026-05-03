from .translations import get_translations
from django.conf import settings

def translation_context(request):
    """Add translations to the context for all templates"""
    # Get the current language from the session or use default
    language_code = request.session.get('django_language', settings.LANGUAGE_CODE.split('-')[0])
    
    # Get translations for the current language
    translations = get_translations(language_code)
    
    return {
        'translations': translations,
        'current_language': language_code,
        'available_languages': settings.LANGUAGES,
    }