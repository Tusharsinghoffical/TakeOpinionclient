from django.urls import path
from . import views

urlpatterns = [
    path("", views.hospitals_list, name="hospitals_list"),
    path("<slug:slug>/", views.hospital_detail, name="hospital_detail"),
    path("<slug:slug>/test/", views.hospital_test, name="hospital_test"),
    path("<slug:slug>/simple-test/", views.hospital_simple_test, name="hospital_simple_test"),
    path("<slug:slug>/debug/", views.hospital_media_debug, name="hospital_media_debug"),
    path("api/search/", views.search_hospitals_api, name="search_hospitals_api"),
]