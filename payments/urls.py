from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payment-success/', views.payment_success, name='payment_success'),
    path('static-payment/<int:booking_id>/', views.static_payment_demo, name='static_payment_demo'),
    path('process-static-payment/<int:booking_id>/', views.process_static_payment, name='process_static_payment'),
    path('static-payment-success/<int:payment_id>/', views.static_payment_success, name='static_payment_success'),
]