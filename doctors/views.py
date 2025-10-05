from datetime import date

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from scheduling.models import ClinicSession, AvailabilitySlot, AvailabilityStatus
from .models import Doctor


# Create your views here.
class HomeView(TemplateView):
    template_name = 'doctors/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["doctors"] = Doctor.objects.filter(active=True).order_by("last_name", "first_name")
        return ctx

class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors/doctors_list.html'
    context_object_name = "doctors"
    paginate_by = 20

    def get_queryset(self):
        return Doctor.objects.filter(active=True).order_by("last_name", "first_name")

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctors/doctor_detail.html'
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        sessions = (
            ClinicSession.objects
            .filter(doctor_clinic__doctor=self.object, date__gte=today)
            .order_by("date", "start_time")[:20]
        )

        slots_by_session = {}
        for session in sessions:
            slots = (AvailabilitySlot.objects
                     .filter(session=session, status=AvailabilityStatus.AVAILABLE)
                     .select_related("service")
                     .order_by("slot_start"))
            slots_by_session[session.pk] = list(slots)

            ctx["sessions"] = sessions
            ctx["slots_by_session"] = slots_by_session
            return ctx;