from django import forms

from patients.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'border-gray-300 rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'phone': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
        }

class GuestPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'border-gray-300 rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'border-gray-300 rounded-md'}),
            'phone': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'}),
        }