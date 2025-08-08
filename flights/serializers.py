from rest_framework import serializers
from .models import Airline, Flight , Booking , UserDetails

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserDetails.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'user', 'flight', 'seat_class', 'number_of_seats', 'booking_time']

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

