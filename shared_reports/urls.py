from django.urls import path
from . import views

app_name = 'shared_reports'

urlpatterns = [
    path('', views.share_report_page, name='share_report'),
    path('my-reports/', views.my_shared_reports, name='my_reports'),
    path('doctor-inbox/', views.doctor_reports_inbox, name='doctor_inbox'),
    path('<int:report_id>/chat/', views.report_chat, name='report_chat'),
]
