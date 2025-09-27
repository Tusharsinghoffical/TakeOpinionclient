from django.urls import path
from . import views

urlpatterns = [
    path("", views.treatments_home, name="treatments_home"),
    path("filter/", views.filter_treatments, name="filter_treatments"),
    path("pricing/", views.treatments_pricing, name="treatments_pricing"),
    path("pricing/new/", views.new_treatments_pricing, name="new_treatments_pricing"),
    path("<slug:slug>/", views.treatment_detail, name="treatment_detail"),
]