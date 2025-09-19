from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("countries/", views.countries, name="countries"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]


