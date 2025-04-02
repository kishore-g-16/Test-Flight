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

    def __str__(self):
        return f"{self.airline.name} - {self.flight_number}"

