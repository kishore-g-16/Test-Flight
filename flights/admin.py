from django.contrib import admin
from .models import Airline, Flight, Booking, UserDetails

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'airline', 'flight_number', 'flight_class', 'departure_time', 'arrival_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger_name', 'flight', 'seat_class', 'number_of_seats', 'booking_time')

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
