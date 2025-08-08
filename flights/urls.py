from django.urls import path
from .views import AirlineListCreateView, AirlineDetailView, FlightListCreateView, FlightDetailView, \
    BookingListCreateView, UserDetailsView

urlpatterns = [
    path('airlines/', AirlineListCreateView.as_view(), name='airline-list-create'),
    path('airlines/<int>/', AirlineDetailView.as_view(), name='airline-detail'),
    path('flights/', FlightListCreateView.as_view(), name='flight-list-create'),
    path('flights/<int>/', FlightDetailView.as_view(), name='flight-detail'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('users/', UserDetailsView.as_view(), name='user-list-create'),
    path('users/<str:username>/', UserDetailsView.as_view(), name='user-detail'),
]
