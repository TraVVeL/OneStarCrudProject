from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializer import RoomSerializer, BookingSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from .models import Room, Booking


class CreateRoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            return Response({"success": f"room was created: {room.id}"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListRoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get("sort_by", "created_at")
        order = self.request.query_params.get("order", "asc")

        if sort_by not in ["price", "created_at"]:
            sort_by = "created_at"

        if order == "desc":
            sort_by = f"-{sort_by}"
        return queryset.order_by(sort_by)


class DeleteRoomView(generics.DestroyAPIView):
    queryset = Room.objects.all()

    def delete(self, request, *args, **kwargs):
        room = self.get_object()
        room.bookings.all().delete()
        room.delete()
        return Response({"success": "room was deleted"}, status=HTTP_200_OK)


class CreateBookingView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response({"booking_id": booking.id}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListBookingView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get("room_id")

        if not room_id:
            raise ValidationError({"error": "room_id is required"})

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise ValidationError({"error": f"room with id {room_id} does not exist"})

        return Booking.objects.filter(room_id=room_id).order_by("date_start")


class DeleteBookingView(generics.DestroyAPIView):
    queryset = Booking.objects.all()

    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.delete()
        return Response({"success": "room was deleted"}, status=HTTP_200_OK)
