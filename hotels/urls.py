from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotels_list, name='list'),
    path('<slug:slug>/', views.hotel_detail, name='detail'),
    path('api/search/', views.search_hotels_api, name='search_api'),
    path('suggestions/<int:booking_id>/', views.suggest_hotels_after_payment, name='suggestions'),
]