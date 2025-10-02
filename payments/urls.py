from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('success/', views.payment_success, name='payment_success'),
    path('static/<int:booking_id>/', views.static_payment_demo, name='static_payment_demo'),
    path('static/process/<int:booking_id>/', views.process_static_payment, name='process_static_payment'),
    path('static/success/<int:payment_id>/', views.static_payment_success, name='static_payment_success'),
    path('consultation/success/<int:payment_id>/', views.consultation_payment_success, name='consultation_payment_success'),
]