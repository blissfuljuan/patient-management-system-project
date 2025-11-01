from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False,
                                     widget=forms.CheckboxInput())

class PatientSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username","email","first_name","last_name","password1","password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.role = User.Role.PATIENT

        if commit:
            user.save()
            try:
                from patients.models import Patient
                Patient.objects.get_or_create(user=user, defaults={
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                })
            except Exception:
                pass
        return user