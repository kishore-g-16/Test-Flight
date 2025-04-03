from django.contrib import admin
from .models import Airline, Flight, Booking

admin.site.register(Airline)
admin.site.register(Flight)
admin.site.register(Booking)