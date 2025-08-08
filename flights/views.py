from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Airline, Flight, Booking , UserDetails
from .serializers import AirlineSerializer, FlightSerializer, BookingSerializer , UserDetailsSerializer


# API to list and create airlines
class AirlineListCreateView(APIView):
    def get(self, request):
        airlines = Airline.objects.all()
        serializer = AirlineSerializer(airlines, many=True)
        return Response(serializer.data)

    def post(self, request):    
        serializer = AirlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to retrieve, update, and delete an airline
class AirlineDetailView(APIView):
    def get_object(self, pk):
        try:
            return Airline.objects.get(pk=pk)
        except Airline.DoesNotExist:
            return None

    def get(self, request, pk):
        airline = self.get_object(pk)
        if not airline:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AirlineSerializer(airline)
        return Response(serializer.data)

    def put(self, request, pk):
        airline = self.get_object(pk)
        if not airline:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AirlineSerializer(airline, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        airline = self.get_object(pk)
        if not airline:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        airline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API to list and create flights with timing information
class FlightListCreateView(APIView):
    def get(self, request):
        airline_id = request.query_params.get('airline_id')
        if airline_id:
            flights = Flight.objects.filter(airline_id=airline_id)
        else:
            flights = Flight.objects.all()

        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to retrieve, update, and delete a flight
class FlightDetailView(APIView):
    def get_object(self, pk):
        try:
            return Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return None

    def get(self, request, pk):
        flight = self.get_object(pk)
        if not flight:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlightSerializer(flight)
        return Response(serializer.data)

    def put(self, request, pk):
        flight = self.get_object(pk)
        if not flight:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlightSerializer(flight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        flight = self.get_object(pk)
        if not flight:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API to list and create bookings with a booking time

class BookingListCreateView(APIView):

    # To List All Bookings

    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        flight_id = request.data.get("flight")
        user_id = request.data.get("user")

        # Validate flight
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight:
            return Response({"error": "Flight not found!"}, status=status.HTTP_404_NOT_FOUND)

        # Validate user
        user = UserDetails.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking_time = serializer.validated_data.get("booking_time", now())

            # Ensure booking time is before departure
            if booking_time >= flight.departure_time:
                return Response({"error": "Booking time must be before departure time."}, status=status.HTTP_400_BAD_REQUEST)

            # Save booking with validated user and flight
            serializer.save(user=user, flight=flight, booking_time=booking_time)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):

    def get(self, request, username=None):
        if username:
            user = get_object_or_404(UserDetails, username=username)
            serializer = UserDetailsSerializer(user)
            return Response(serializer.data)
        else:
            users = UserDetails.objects.all()
            serializer = UserDetailsSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username):
        user = get_object_or_404(UserDetails, username=username)
        serializer = UserDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

