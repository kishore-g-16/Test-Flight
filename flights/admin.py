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
    list_display = ('id', 'get_username', 'flight')
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'  # Sets column header in admin

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
