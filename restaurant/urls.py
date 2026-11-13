from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("booking/", views.booking, name="booking"),
    path("bookings", views.bookings_api, name="bookings_api"),
    path("bookings/", views.bookings_api),
]
