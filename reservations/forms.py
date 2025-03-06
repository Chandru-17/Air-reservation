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
    passengers = forms.ModelMultipleChoiceField(
        queryset=Passenger.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # ✅ Allows selecting multiple passengers
        required=True,
        label="Select Passengers"
    )

    flight = forms.ModelChoiceField(
        queryset=Flight.objects.all(),
        empty_label="Select Flight",
        label="Select Flight"
    )

    class Meta:
        model = Reservation
        fields = ['passengers', 'flight', 'seat_number']