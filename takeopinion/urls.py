"""
URL configuration for takeopinion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from accounts.views import get_entities
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/entities/<str:entity_type>/", csrf_exempt(get_entities), name='get_entities'),
]

# Add internationalized patterns
urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("treatments/", include("treatments.urls")),
    path("hospitals/", include("hospitals.urls")),
    path("doctors/", include("doctors.urls")),
    path("blogs/", include("blogs.urls")),
    path("book/", include("bookings.urls")),
    path("accounts/", include("accounts.urls")),
    path("feedbacks/", include("feedbacks.urls")),
    path("payments/", include("payments.urls")),
    path("hotels/", include("hotels.urls")),
    path("enquiries/", include("enquiry_bot.urls")),
    prefix_default_language=False,  # Don't prefix the default language
)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static and media files in production using WhiteNoise
# This is needed for Render deployment
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)