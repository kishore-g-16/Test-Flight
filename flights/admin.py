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
    list_display = ('id', 'username', 'full_name', 'gender', 'date_of_birth', 'mobile_number', 'email', 'is_special_person', 'is_covid_vaccinated')
    readonly_fields = ('username',)
