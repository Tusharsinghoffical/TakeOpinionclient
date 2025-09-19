from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctors_list, name="doctors_list"),
    path("<slug:slug>/", views.doctor_detail, name="doctor_detail"),
]


