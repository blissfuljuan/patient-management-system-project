from django import forms

from .models import Patient, GuestPatient

BASE_INPUT = 'block w-full rounded-mb border border-gray-300 bg-white px-3 py-2' \
    'text-gray-900 shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "input", "placeholder": "First Name"}),
            'last_name': forms.TextInput(attrs={'class': "input", "placeholder": "Last Name"}),
            'email': forms.EmailInput(attrs={'class': "input"}),
            'phone': forms.TextInput(attrs={'class': "input"}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': "input"}),
        }

class GuestPatientForm(forms.ModelForm):
    class Meta:
        model = GuestPatient
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'border-gray-300 rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'phone': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
        }