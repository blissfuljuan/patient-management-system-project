from django.db import transaction
from django.utils import timezone

from .models import BookingChannel, Appointment, AppointmentStatus, AppointmentAudit
from patients.models import GuestPatient, Patient
from scheduling.models import AvailabilitySlot

def _audit(appt: Appointment, old: str, new: str, actor: str = ''):
    AppointmentAudit.objects.create(
        appointment=appt, old_status=old or '',
        new_status=new or '', changed_by=actor
    )

def _copy_guest_to_patient(guest: GuestPatient) -> Patient:
    return Patient.objects.create(
        first_name=guest.first_name,
        last_name=guest.last_name,
        email=guest.email or "",
        phone=guest.phone or "",
        dob=guest.dob or "",
    )

@transaction.atomic
def book_with_guest(*, slot: AvailabilitySlot,
                    service, guest_data: dict,
                    channel: str = BookingChannel.WALK_IN, is_walk_in: bool = True) -> Appointment:
    guest = Patient.objects.create(**guest_data)
    appt = Appointment.objects.create(
        start_time=slot.slot_start,
        end_time=slot.slot_end,
        status=AppointmentStatus.PENDING,
        booking_channel=channel,
        is_walk_in=is_walk_in,
        walk_in_name=f"{guest.first_name} {guest.last_name}",
        walk_in_phone={guest.phone} or "",
        service=service,
        slot=slot,
        session=slot.session,
        guest=guest,
    )

    return appt

@transaction.atomic
def book_with_patient(*, slot: AvailabilitySlot, service, patient: Patient,
                      channel: str = BookingChannel.ONLINE) -> Appointment:
    appt = Appointment.objects.create(
        start_time=slot.slot_start,
        end_time=slot.slot_end,
        status=AppointmentStatus.PENDING,
        booking_channel=channel,
        is_walk_in=(channel == BookingChannel.WALK_IN),
        service=service,
        slot=slot,
        session=slot.session,
        patient=patient,
    )
    _audit(appt, old='', new=AppointmentStatus.PENDING, actor=channel)
    return appt

@transaction.atomic
def mark_confirmed(appt: Appointment, *, actor: str = 'system'):
    old = appt.status
    appt.status = AppointmentStatus.CONFIRMED
    appt.save(update_fields=['status'])
    _audit(appt, old=old, new=appt.status, actor=actor)

@transaction.atomic
def mark_completed(appt: Appointment, *, actor: str = 'system'):
    old = appt.status
    if appt.guest and not appt.patient:
        patient = _copy_guest_to_patient(appt.guest)
        guest_id = appt.guest.id
        appt.patient = patient
        appt.guest = None
        appt.save(update_fields=['patient', 'guest'])
        GuestPatient.objects.filter(id=guest_id).delete()

    appt.status = AppointmentStatus.COMPLETED
    appt.save(update_fields=['status'])
    _audit(appt, old=old, new=appt.status, actor=actor)

@transaction.atomic
def mark_cancelled(appt: Appointment, *, actor: str = 'system'):
    old = appt.status
    was_confirmed = (old == AppointmentStatus.CONFIRMED)
    guest_id = appt.guest.id

    appt.status = AppointmentStatus.CANCELLED
    appt.save(update_fields=['status'])
    _audit(appt, old=old, new=appt.status, actor=actor)

    if was_confirmed and guest_id and appt.patient_id is None:
        GuestPatient.objects.filter(id=guest_id).delete()

@transaction.atomic
def mark_no_show(appt: Appointment, *, actor: str = 'system'):
    old = appt.status
    was_confirmed = (old == AppointmentStatus.CONFIRMED)
    guest_id = appt.guest.id

    appt.status = AppointmentStatus.NO_SHOW
    appt.save(update_fields=['status'])
    _audit(appt, old=old, new=appt.status, actor=actor)

    if was_confirmed and guest_id and appt.patient_id is None:
        GuestPatient.objects.filter(id=guest_id).delete()