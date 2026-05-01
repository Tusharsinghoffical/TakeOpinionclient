from .translations import get_translations
from django.conf import settings

def translation_context(request):
    """Add translations to the context for all templates"""
    # Get the current language from the session or use default
    language_code = request.session.get('django_language', settings.LANGUAGE_CODE.split('-')[0])

    # Get translations for the current language
    translations = get_translations(language_code)

    # Fetch latest approved feedbacks for footer display
    footer_reviews = []
    try:
        from feedbacks.models import Feedback
        footer_reviews = list(
            Feedback.objects.filter(is_approved=True)
            .select_related('patient__user', 'doctor', 'hospital', 'treatment')
            .order_by('-created_at')[:4]
        )
    except Exception:
        pass

    return {
        'translations': translations,
        'current_language': language_code,
        'available_languages': settings.LANGUAGES,
        'footer_reviews': footer_reviews,
    }