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
]