import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Flight
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from .forms import RegisterForm
from .models import Flight, Reservation, Passenger
from .forms import ReservationForm
from django.contrib.auth.forms import AuthenticationForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Passenger


stripe.api_key = settings.STRIPE_SECRET_KEY

def flight_list(request):
    query = request.GET.get("query", "")
    flights = Flight.objects.all()

    if query:
        flights = flights.filter(
            departure_city__icontains=query  # Search by departure city
        ) | flights.filter(
            destination_city__icontains=query  # Search by destination city
        )
    return render(request, 'reservations/flight_list.html', {'flights': flights, "query": query})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flight_list')
    else:
        form = RegisterForm()
    
    return render(request, 'reservations/register.html', {'form': form})

def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            passengers = form.cleaned_data['passenger']  # Get selected passengers
            seat_number = form.cleaned_data['seat_number']

            # Create a single reservation and assign multiple passengers
            reservation = Reservation.objects.create(flight=flight, seat_number=seat_number)
            reservation.passenger.set(passengers)  # ✅ Assign multiple passengers

            return redirect('booking_confirmation', reservation_id=reservation.id)  
    else:
        form = ReservationForm(initial={'flight': flight})

    return render(request, 'reservations/book_flight.html', {'form': form, 'flight': flight})

def booking_confirmation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'reservations/booking_confirmation.html', {'reservation': reservation})

def payment(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': reservation.flight.flight_number},
                'unit_amount': int(reservation.flight.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"http://127.0.0.1:8000/payment/success/{reservation.id}/",
        cancel_url=f"http://127.0.0.1:8000/payment/cancel/",
    )

    return redirect(session.url, code=303)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flight_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login') 

@csrf_exempt
def add_passenger(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')

        if name and email:
            passenger = Passenger.objects.create(name=name, email=email)
            return JsonResponse({"success": True, "name": passenger.name, "email": passenger.email})

    return JsonResponse({"success": False})

# def my_bookings(request):
#     if request.user.is_authenticated:
#         try:
#             passenger = Passenger.objects.get(user=request.user)
#             reservations = Reservation.objects.filter(passenger=passenger)
#         except Passenger.DoesNotExist:
#             reservations = []  
#     else:
#         reservations = []

#     return render(request, "my_bookings.html", {"reservations": reservations})

def travelers(request):
    return render(request,'travelers.html')
