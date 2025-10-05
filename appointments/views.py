from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from patients.models import Patient
from scheduling.models import AvailabilitySlot, AvailabilityStatus
from .forms import BookingChoiceForm, GuestInlineForm
from .models import Appointment, BookingChannel


# Create your views here.
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        return (Appointment.objects
                .select_related('patient', 'guest', 'service')
                .order_by('-created_at'))

@transaction.atomic
def book_appointment(request, slot_id: int):
    slot = get_object_or_404(
        AvailabilitySlot.objects.select_related('service', 'session'),
        pk=slot_id,
        status=AvailabilityStatus.AVAILABLE
    )

    service = slot.service

    if request.method == 'POST':
        choice_form = BookingChoiceForm(request.POST)
        guest_form = GuestInlineForm(request.POST)

        if choice_form.is_valid() and guest_form.is_valid():
            channel = choice_form.cleaned_data['booking_channel']
            is_walk_in = choice_form.cleaned_data.get('is_walk_in', False)
            patient_id = choice_form.cleaned_data.get('existing_patient_id')

            try:
                if patient_id:
                    patient = get_object_or_404(Patient, pk=patient_id)
                    from .services import book_with_patient
                    appt = book_with_patient(slot=slot, service=service, patient=patient, channel=channel)
                else:
                    guest_data = guest_form.as_guest_dict()
                    if is_walk_in:
                        if not guest_data['first_name'] or not guest_data['last_name'] or not guest_data['phone']:
                            messages.error(request, "Walk-in requires first/last name and phone.")
                            return render(request, 'appointments/book.html', {
                                'slot': slot, 'service': service,
                                'choice_form': choice_form, 'guest_form': guest_form
                            })
                    from .services import book_with_guest
                    appt = book_with_guest(
                        slot=slot, service=service, guest_data=guest_data, channel=channel, is_walk_in=is_walk_in
                    )
                messages.success(request, f"Appointment created: #{appt.pk}")
                return redirect('appointments:list')
            except Exception as e:
                messages.error(request, f"Booking failed: {e}")
    else:
        choice_form = BookingChoiceForm(initial={'booking_channel': BookingChannel.ONLINE})
        guest_form = GuestInlineForm()

    return render(request, 'appointments/book.html', {
        'slot': slot, 'service': service,
        'choice_form': choice_form, 'guest_form': guest_form,
    })