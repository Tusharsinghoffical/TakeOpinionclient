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
    prefix_default_language=False,  
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)