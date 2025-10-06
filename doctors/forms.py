from django import forms
from django.utils import timezone

BASE_INPUT = 'block w-full rounded-mb border border-gray-300 bg-white px-3 py-2' \
    'text-gray-900 shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500'

class DoctorDashboardFilterForm(forms.Form):
    start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': BASE_INPUT})
    )
    end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': BASE_INPUT})
    )

    def cleaned_range(self):
        today = timezone.localdate()
        start = self.cleaned_data["start"] or today
        end = self.cleaned_data["end"] or today
        if end < start:
            start, end = end, start
        return start, end