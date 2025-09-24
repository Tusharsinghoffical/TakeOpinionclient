from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_page, name="booking_page"),
    path("confirmation/<int:booking_id>/", views.booking_confirmation, name="booking_confirmation"),
    path("post-payment/", views.post_payment, name="post_payment"),
    path("consultation/<int:doctor_id>/", views.consultation_booking, name="consultation_booking"),
    path("api/create-google-meet/", views.create_google_meet, name="create_google_meet"),
]