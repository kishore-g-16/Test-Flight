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
    def get(self, request):
        bookings = Booking.objects.all()
        if not bookings.exists():
            return Response({"error": "No bookings found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        flight_id = request.data.get("flight")
        flight = Flight.objects.filter(id=flight_id).first()

        if not flight:
            return Response({"error": "Flight not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking_time = serializer.validated_data.get("booking_time", now())

            if booking_time < flight.departure_time:
                serializer.save(booking_time=booking_time)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Booking time must be before departure time"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to create and cancel a booking
class BookingCreateCancelView(APIView):
    def post(self, request):
        """Create and save a new booking"""
        flight_id = request.data.get("flight")
        flight = Flight.objects.filter(id=flight_id).first()

        if not flight:
            return Response({"error": "Flight not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking_time = serializer.validated_data.get("booking_time", now())

            if booking_time < flight.departure_time:
                serializer.save(booking_time=booking_time)
                return Response(
                    {"message": "Booking created successfully!", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response({"error": "Booking time must be before departure time"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, booking_id):
        """Cancel a booking by deleting it"""
        booking = Booking.objects.filter(id=booking_id).first()

        if not booking:
            return Response({"error": "Booking not found!"}, status=status.HTTP_404_NOT_FOUND)

        booking.delete()
        return Response({"message": "Booking canceled successfully!"}, status=status.HTTP_204_NO_CONTENT)

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

