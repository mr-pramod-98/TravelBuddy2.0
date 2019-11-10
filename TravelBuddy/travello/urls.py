from django.urls import path
from . import views

urlpatterns = [
    path('TravelBuddy/<str:username>/', views.travello, name='travello'),
    path('TravelBuddy/<str:username>/<str:destination_id>', views.destination_details, name='destination_details'),
    path('TravelBuddy/<str:username>/<str:destination_id>/booking', views.bookings, name='bookings'),
    path('TravelBuddy/<str:username>/<str:destination_id>/booking_confirmed', views.bookings_confirmed, name='bookings_confirmed')
]
