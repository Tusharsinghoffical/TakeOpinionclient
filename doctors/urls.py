from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctors_list, name="doctors_list"),
    path("<slug:slug>/", views.doctor_detail, name="doctor_detail"),
    path("media-upload/<int:doctor_id>/", views.doctor_media_upload, name="doctor_media_upload"),
    path("media-manage/", views.doctor_media_manage, name="doctor_media_manage"),
    path("api/search/", views.search_doctors_api, name="search_doctors_api"),
]