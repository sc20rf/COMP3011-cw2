from django.urls import path
from . import views

# URL Configurations for this app
urlpatterns = [
    path('airports/', views.get_airport_info),
    path('flights/', views.get_flight_info),
    path('make-booking/', views.make_booking),
    path('invoice/<str:booking_id>/', views.create_invoice),
    path('confirm/<str:booking_id>/', views.confirm_invoice)
]