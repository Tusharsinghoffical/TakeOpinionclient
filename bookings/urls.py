from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path("", views.booking_page, name="booking_page"),
    path("new/", views.new_booking_page, name="new_booking_page"),
    path("api/doctors/<int:treatment_id>/", views.get_doctors_by_treatment, name="get_doctors_by_treatment"),
    path("api/hospitals/<int:treatment_id>/", views.get_hospitals_by_treatment, name="get_hospitals_by_treatment"),
    path("api/rooms/<int:hospital_id>/", views.get_rooms_by_hospital, name="get_rooms_by_hospital"),
    path("confirmation/<int:booking_id>/", views.booking_confirmation, name="booking_confirmation"),
    path("post-payment/", views.post_payment, name="post_payment"),
    path("consultation/<int:doctor_id>/", views.consultation_booking, name="consultation_booking"),
    path("payment/<int:booking_id>/", views.payment_page, name="payment_page"),
    path("api/create-google-meet/", views.create_google_meet, name="create_google_meet"),
    # Admin dashboard URLs
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/update-status/<int:booking_id>/<str:status>/", views.update_booking_status, name="update_booking_status"),
]