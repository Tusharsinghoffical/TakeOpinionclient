from django.urls import path
from . import views

urlpatterns = [
    path("", views.treatments_home, name="treatments_home"),
    path("filter/", views.filter_treatments, name="filter_treatments"),
    path("<slug:slug>/", views.treatment_detail, name="treatment_detail"),
]