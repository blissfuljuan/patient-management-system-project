from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .forms import PatientForm
from .models import Patient


# Create your views here.
class PatientListView(ListView):
    model = Patient
    template_name = 'patients/patient-list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        return (Patient.objects
                .order_by('last_name', 'first_name')
                .only('id', 'last_name', 'first_name', 'email', 'phone'))

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:list')

class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:list')