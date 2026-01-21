from django.urls import path
from . import views

app_name = 'feedbacks'

urlpatterns = [
    path('submit/<str:content_type>/<int:object_id>/', views.submit_feedback, name='submit_feedback'),
    path('list/<str:content_type>/<int:object_id>/', views.feedback_list, name='feedback_list'),
]