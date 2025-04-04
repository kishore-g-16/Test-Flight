from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Airline, Flight, Booking
from .serializers import AirlineSerializer, FlightSerializer, BookingSerializer


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

# API to list and create flights
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

# Booking Tickets
class BookingListCreateView(APIView):
    def get(self, request):
        booking = Booking.objects.all()
        serializer = BookingSerializer(booking, many=True)
        if not booking.exists():
            return Response({"error": "No bookings found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCreateCancelView(APIView):
    def post(self, request):
        """Create and save a new booking"""
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Booking created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, booking_id):
        """Cancel a booking by deleting it without using get_object_or_404()"""
        if not Booking.objects.filter(id=booking_id).exists():
            return Response(
                {"error": "Booking not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        Booking.objects.filter(id=booking_id).delete()
        return Response({"message": "Booking canceled successfully!"}, status=status.HTTP_204_NO_CONTENT)