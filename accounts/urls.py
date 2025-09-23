from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/portal/', views.patient_portal, name='patient_portal'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('patient/submit-review/', views.submit_review, name='submit_review'),
    path('reviews/', views.reviews_page, name='reviews_page'),  # New reviews page
    path('api/reviews/', views.reviews_api, name='reviews_api'),  # API endpoint for reviews
]