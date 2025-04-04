from django.db import models

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

    departure_time = models.DateTimeField()  # New field for departure time
    arrival_time = models.DateTimeField()  # New field for arrival time

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
    booking_time = models.DateTimeField()  # New field for selecting booking time

    def __str__(self):
        booking_time_str = self.booking_time.strftime('%Y-%m-%d %H:%M') if self.booking_time else "No Booking Time"
        return f"{self.flight} - {self.passenger_name} - {self.number_of_seats} - {self.seat_class} - {booking_time_str}"