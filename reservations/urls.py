from django.urls import path
from .views import flight_list,book_flight,booking_confirmation,payment,user_logout,add_passenger,travelers

from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='reservations/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('flights/', flight_list, name='flight_list'),
    path('flights/<int:flight_id>/book/', book_flight, name='book_flight'),
    path("add-passenger/", add_passenger, name="add_passenger"),
    path('booking/<int:reservation_id>/confirmation/', booking_confirmation, name='booking_confirmation'),
     path('payment/<int:reservation_id>/', payment, name='payment'),
    path('payment/success/<int:reservation_id>/', booking_confirmation, name='payment_success'),
    path('payment/cancel/', lambda request: render(request, 'reservations/payment_cancel.html'), name='payment_cancel'),
    # path('my-bookings/', my_bookings, name='my_bookings'),
    path('travelers/', travelers, name='travelers'),
]
