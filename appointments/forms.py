from django import forms

from appointments.models import BookingChannel


class BookingChoiceForm(forms.Form):
    booking_channel = forms.ChoiceField(
        label = "Booking Channel",
        choices = BookingChannel.choices,
        widget=forms.Select(attrs={'class': 'border-gray-300 rounded-md'})
    )

    existing_patient_id = forms.IntegerField(
        required = False,
        label = "Existing Patient ID",
        widget=forms.NumberInput(attrs={
            'class': 'border-gray-300 rounded-md',
            'placeholder': 'Enter Patient ID (optional)',})
    )

    is_walk_in = forms.BooleanField(
        required = False,
        label = "Is Walk In?",
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-sky-600 border-gray-300 rounded'})
    )

class GuestInlineForm(forms.Form):
    first_name = forms.CharField(
        max_length=80, required = False,
        widget=forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'})
    )
    last_name = forms.CharField(
        max_length=80, required=False,
        widget=forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'border-gray-300 rounded-md'})
    )
    phone = forms.CharField(
        max_length=32, required=False,
        widget=forms.TextInput(attrs={'class': 'border-gray-300 rounded-md'})
    )
    dob = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border-gray-300 rounded-md'})
    )

    def as_guest_dict(self):
        return {
            'first_name': self.cleaned_data.get('first_name', ''),
            'last_name': self.cleaned_data.get('last_name', ''),
            'email': self.cleaned_data.get('email', ''),
            'phone': self.cleaned_data.get('phone', ''),
            'dob': self.cleaned_data.get('dob', None),
        }