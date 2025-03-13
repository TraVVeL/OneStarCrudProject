from rest_framework import serializers
from .models import Room, Booking
from datetime import datetime


class RoomSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Room
        fields = ['id', 'description', 'price', 'created_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "date_start", "date_end"]

    def validate(self, data):
        date_start = data.get("date_start")
        date_end = data.get("date_end")

        if date_start >= date_end:
            raise serializers.ValidationError("Start date must be before end date")
        if date_start < datetime.today().date():
            raise serializers.ValidationError("Start date cannot be in the past")

        room_id = data.get("room")
        overlapping_bookings = Booking.objects.filter(
            room_id=room_id,
            date_start__lt=date_end,
            date_end__gt=date_start
        )
        if overlapping_bookings.exists():
            raise serializers.ValidationError(f"Room {room_id} is already booked for the selected dates")

        return data
