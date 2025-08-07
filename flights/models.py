from django.db import models
from django.utils import timezone
import hashlib
import uuid

class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Flight(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)  # ForeignKey to Airline
    flight_number = models.CharField(max_length=20, unique=True)
    seat_count = models.PositiveIntegerField()
    flight_class = models.CharField(max_length=50,
            choices=[("Economy", "Economy"),
                     ("Business", "Business")
                     ])

    departure_time = models.DateTimeField(default=timezone.now)  # New field for departure time
    arrival_time = models.DateTimeField(default=timezone.now)  # New field for arrival time

    def __str__(self):
        departure_time_str = self.departure_time.strftime('%Y-%m-%d %H:%M') \
            if self.departure_time else "No Departure Time"
        return f"{self.airline.name} - {self.flight_number} ({departure_time_str})"


class Booking(models.Model):
    CLASS_CHOICES = [
        ("Economy", "Economy"),
        ("Business", "Business"),
    ]
    passenger_name = models.CharField(max_length=100)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE) # ForeignKey to Flight
    seat_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    number_of_seats = models.PositiveIntegerField()
    booking_time = models.DateTimeField(default=timezone.now)  # New field for selecting booking time

    def __str__(self):
        booking_time_str = self.booking_time.strftime('%Y-%m-%d %H:%M') if self.booking_time else "No Booking Time"
        return f"{self.flight} - {self.passenger_name} - {self.number_of_seats} - {self.seat_class} - {booking_time_str}"


class UserDetails(models.Model):

    # Auto Generateed User Name

    username = models.CharField(max_length=64, unique=True, blank=True)

    # Primary Fields
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100 , null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    id_proof_details = models.TextField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)

    is_special_person = models.BooleanField(default=False)
    is_covid_vaccinated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.username:
            # Use first name + birthdate to create base username
            base_username = f"{self.first_name.lower()}{self.date_of_birth.strftime('%Y%m%d')}"
            original = base_username
            count = 1
            while UserDetails.objects.filter(username=base_username).exists():
                base_username = f"{original}_{count}"
                count += 1
            self.username = base_username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
