from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "featured"]


class BookingSerializer(serializers.ModelSerializer):
    time = serializers.CharField(source="get_reservation_slot_display", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "first_name",
            "reservation_date",
            "reservation_slot",
            "time",
        ]

    def validate(self, attrs):
        date = attrs.get("reservation_date")
        slot = attrs.get("reservation_slot")
        duplicate = Booking.objects.filter(
            reservation_date=date, reservation_slot=slot
        )
        if self.instance:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise serializers.ValidationError(
                "This date and time are already booked."
            )
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
