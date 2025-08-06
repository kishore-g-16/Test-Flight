from django.contrib import admin
from .models import Airline, Flight, Booking , UserDetails

admin.site.register(Airline)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(UserDetails)