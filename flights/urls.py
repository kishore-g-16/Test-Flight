from django.urls import path
from .views import AirlineListCreateView, AirlineDetailView, FlightListCreateView, FlightDetailView

urlpatterns = [
    path('airlines/', AirlineListCreateView.as_view(), name='airline-list-create'),
    path('airlines/<int:pk>/', AirlineDetailView.as_view(), name='airline-detail'),
    path('flights/', FlightListCreateView.as_view(), name='flight-list-create'),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
]
