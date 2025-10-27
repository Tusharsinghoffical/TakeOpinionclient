from django.urls import path
from . import views

urlpatterns = [
    path("", views.treatments_home, name="treatments_home"),
    path("filter/", views.filter_treatments, name="filter_treatments"),
    path("pricing/", views.treatments_pricing, name="treatments_pricing"),
    path("pricing/new/", views.new_treatments_pricing, name="new_treatments_pricing"),
    path("api/hospitals/<int:treatment_id>/", views.get_hospitals_for_treatment, name="get_hospitals_for_treatment"),
    path("api/search/", views.search_entities, name="search_entities"),
    path("category/<slug:category_slug>/", views.treatments_home, name="treatments_by_category"),
    path("<slug:slug>/", views.treatment_detail, name="treatment_detail"),
    path("<slug:slug>/comparison/", views.treatment_comparison, name="treatment_comparison"),
]