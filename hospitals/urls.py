from django.urls import path
from . import views

urlpatterns = [
    path("", views.hospitals_list, name="hospitals_list"),
    path("<slug:slug>/", views.hospital_detail, name="hospital_detail"),
]


