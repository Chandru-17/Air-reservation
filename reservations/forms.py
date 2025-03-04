from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation,Passenger,Flight

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ReservationForm(forms.ModelForm):
    passenger = forms.ModelMultipleChoiceField(
        queryset=Passenger.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # ✅ Allows selecting multiple passengers
        label="Select Passengers"
    )

    flight = forms.ModelChoiceField(
        queryset=Flight.objects.all(),
        empty_label="Select Flight",
        label="Select Flight"
    )

    class Meta:
        model = Reservation
        fields = ['passenger', 'flight', 'seat_number']