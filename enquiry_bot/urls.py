from django.urls import path
from . import views

app_name = 'enquiry_bot'

urlpatterns = [
    path('', views.enquiry_bot_view, name='bot_interface'),
    path('chat/', views.chat_message_api, name='chat_api'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('chat-history/<int:enquiry_id>/', views.get_chat_history, name='chat_history'),
    path('my-enquiries/', views.user_enquiries, name='user_enquiries'),
    path('analyze-report/', views.analyze_medical_report, name='analyze_report'),
    path('full-bot/', views.full_bot_interface, name='full_bot_interface'),
    path('video-call/<int:doctor_id>/', views.video_call_view, name='video_call'),
    path('video-call/', views.video_call_view, name='video_call_general'),
]