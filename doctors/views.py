from datetime import date

from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView

from appointments.models import AppointmentStatus, Appointment
from scheduling.models import ClinicSession, AvailabilitySlot, AvailabilityStatus
from .forms import DoctorDashboardFilterForm
from .models import Doctor


# Create your views here.
class DoctorDashboardView(TemplateView):
    template_name = 'doctors/doctor-dashboard.html'

    def get_context_data(self, doctor_id: int, **kwargs):
        ctx = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(pk=doctor_id)
        form = DoctorDashboardFilterForm(self.request.GET or None)
        if form.is_valid():
            start, end = form.cleaned_range()
        else:
            today = timezone.localdate()
            start, end = today, today + timezone.timedelta(days=14)

        sessions_qs = (
            ClinicSession.objects
            .select_related('doctor_clinic__clinic', 'room', 'doctor_clinic__doctor')
            .filter(doctor_clinic__doctor=doctor, date__gte=start, date__lte=end)
            .annotate(
                total_appointments=Count('appointments', distinct=True),
                pending=Count('appointments', filter=Q(appointments__status=AppointmentStatus.PENDING), distinct=True),
                confirmed=Count('appointments', filter=Q(appointments__status=AppointmentStatus.CONFIRMED), distinct=True),
                completed=Count('appointments', filter=Q(appointments__status=AppointmentStatus.COMPLETED), distinct=True),
                no_show=Count('appointments', filter=Q(appointments__status=AppointmentStatus.NO_SHOW), distinct=True),
            )
            .order_by('date', 'start_time')
        )

        totals = sessions_qs.aggregate(
                sessions=Count('id'),
                appointments=Count('appointments', distinct=True),
                pending=Count('appointments', filter=Q(appointments__status=AppointmentStatus.PENDING), distinct=True),
                confirmed=Count('appointments', filter=Q(appointments__status=AppointmentStatus.CONFIRMED),
                                distinct=True),
                completed=Count('appointments', filter=Q(appointments__status=AppointmentStatus.COMPLETED),
                                distinct=True),
                no_show=Count('appointments', filter=Q(appointments__status=AppointmentStatus.NO_SHOW), distinct=True),
        )

        appts_by_session = {
            s.id: list(
                Appointment.objects
                .select_related('patient', 'guest', 'service')
                .filter(session=s)
                .exclude(status=AppointmentStatus.CANCELLED)
                .order_by('start_time')
            )
            for s in sessions_qs
        }

        ctx.update({
            'doctor': doctor,
            'form': form,
            'start': start, 'end': end,
            'sessions': sessions_qs,
            'totals': totals,
            'appts_by_session': appts_by_session,
        })
        return ctx

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