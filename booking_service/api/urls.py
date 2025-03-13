from django.urls import path
from .views import (
    CreateRoomView, ListRoomView, CreateBookingView, DeleteBookingView, ListBookingView, DeleteRoomView
)


urlpatterns = [
    path("rooms/create", CreateRoomView.as_view(), name="room-create"),
    path("rooms/list", ListRoomView.as_view(), name="room-list"),
    path("rooms/delete/<int:pk>", DeleteRoomView.as_view(), name="delete-room"),

    path("bookings/create", CreateBookingView.as_view(), name="create-booking"),
    path("bookings/list", ListBookingView.as_view(), name="booking-list"),
    path("bookings/delete/<int:pk>", DeleteBookingView.as_view(), name="delete-booking"),
]
