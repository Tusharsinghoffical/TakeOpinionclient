from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("health/", views.health_check, name="health_check"),
    path("static-check/", views.static_files_check, name="static_files_check"),
    path("search/", views.search, name="search"),
    path("stats/", views.get_home_stats, name="home_stats"),
    path("content/", views.get_home_content, name="home_content"),
    path("pricing/", views.pricing_page, name="pricing_page"),
    path("compare-treatments/", views.treatment_comparison, name="treatment_comparison"),
    path("debug-comparison/", views.debug_comparison, name="debug_comparison"),
    path("test-url/", views.test_url, name="test_url"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("api/hospitals-by-treatment/<int:treatment_id>/", views.get_hospitals_by_treatment, name="get_hospitals_by_treatment"),
    path("debug-stats/", views.debug_home_stats, name="debug_home_stats"),
    path("debug-stats-page/", views.debug_stats_page, name="debug_stats_page"),
    path("debug-home/", views.debug_home_page, name="debug_home_page"),
    path("test-stats/", views.test_stats_page, name="test_stats_page"),
    path("set-language/", views.set_language, name="set_language"),  # Language switching
]