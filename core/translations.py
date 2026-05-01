# Simple translation dictionary for basic multi-language support
# This is a lightweight alternative to Django's gettext system

TRANSLATIONS = {
    'en': {
        # Navigation
        'home': 'Home',
        'medical_services': 'Medical Services',
        'doctors': 'Doctors',
        'hospitals': 'Hospitals',
        'treatments': 'Treatments',
        'resources': 'Resources',
        'blogs': 'Blogs',
        'reviews': 'Reviews',
        'hotels': 'Hotels',
        'pricing': 'Pricing',
        'comparison': 'Comparison',
        'login': 'Login',
        'sign_up': 'Sign Up',
        
        # Common terms
        'search_doctors_hospitals_treatments': 'Search doctors, hospitals, treatments...',
        'takeopinion': 'TakeOpinion',
        
        # Footer
        'quick_links': 'Quick Links',
        'patient_stories': 'Patient Stories',
        
        # Buttons
        'connect_with_experts': 'Connect with Experts',
        'explore_treatments': 'Explore Treatments',
    },
    'hi': {
        # Navigation
        'home': 'होम',
        'medical_services': 'चिकित्सा सेवाएं',
        'doctors': 'डॉक्टर',
        'hospitals': 'अस्पताल',
        'treatments': 'उपचार',
        'resources': 'संसाधन',
        'blogs': 'ब्लॉग',
        'reviews': 'समीक्षाएं',
        'hotels': 'होटल',
        'pricing': 'मूल्य निर्धारण',
        'comparison': 'तुलना',
        'login': 'लॉग इन करें',
        'sign_up': 'साइन अप करें',
        
        # Common terms
        'search_doctors_hospitals_treatments': 'डॉक्टर, अस्पताल, उपचार खोजें...',
        'takeopinion': 'टेक ऑपिनियन',
        
        # Footer
        'quick_links': 'त्वरित लिंक',
        'patient_stories': 'रोगी की कहानियाँ',
        
        # Buttons
        'connect_with_experts': 'विशेषज्ञों से जुड़ें',
        'explore_treatments': 'उपचार एक्सप्लोर करें',
    },
    'es': {
        # Navigation
        'home': 'Inicio',
        'medical_services': 'Servicios Médicos',
        'doctors': 'Doctores',
        'hospitals': 'Hospitales',
        'treatments': 'Tratamientos',
        'resources': 'Recursos',
        'blogs': 'Blogs',
        'reviews': 'Reseñas',
        'hotels': 'Hoteles',
        'pricing': 'Precios',
        'comparison': 'Comparación',
        'login': 'Iniciar Sesión',
        'sign_up': 'Registrarse',
        
        # Common terms
        'search_doctors_hospitals_treatments': 'Buscar doctores, hospitales, tratamientos...',
        'takeopinion': 'TakeOpinion',
        
        # Footer
        'quick_links': 'Enlaces Rápidos',
        'patient_stories': 'Historias de Pacientes',
        
        # Buttons
        'connect_with_experts': 'Conectar con Expertos',
        'explore_treatments': 'Explorar Tratamientos',
    },
    'fr': {
        # Navigation
        'home': 'Accueil',
        'medical_services': 'Services Médicaux',
        'doctors': 'Médecins',
        'hospitals': 'Hôpitaux',
        'treatments': 'Traitements',
        'resources': 'Ressources',
        'blogs': 'Blogs',
        'reviews': 'Avis',
        'hotels': 'Hôtels',
        'pricing': 'Tarification',
        'comparison': 'Comparaison',
        'login': 'Se Connecter',
        'sign_up': "S'inscrire",
        
        # Common terms
        'search_doctors_hospitals_treatments': 'Rechercher des médecins, hôpitaux, traitements...',
        'takeopinion': 'TakeOpinion',
        
        # Footer
        'quick_links': 'Liens Rapides',
        'patient_stories': 'Témoignages de Patients',
        
        # Buttons
        'connect_with_experts': 'Se Connecter avec des Experts',
        'explore_treatments': 'Explorer les Traitements',
    }
}

def get_translations(language_code):
    """Get translations for a specific language"""
    return TRANSLATIONS.get(language_code, TRANSLATIONS['en'])

def translate(key, language_code):
    """Translate a key to a specific language"""
    translations = get_translations(language_code)
    return translations.get(key, key)