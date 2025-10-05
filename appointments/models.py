from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# FK dependencies
PATIENT_FK = 'patients.Patient'
SERVICE_FK = 'doctors.Service'
SLOT_FK = 'scheduling.AvailabilitySlot'
SESSION_FK = 'scheduling.ClinicSession'
GUEST_FK = 'patients.GuestPatient'

# Create your models here.
class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    NO_SHOW = 'NO_SHOW', 'No Show'

class BookingChannel(models.TextChoices):
    ONLINE = 'ONLINE', 'Online'
    WALK_IN = 'WALK_IN', 'Walk-in'
    DOCTOR = 'DOCTOR', 'Doctor'

class Appointment(models.Model):
    patient = models.ForeignKey(
        PATIENT_FK,
        on_delete=models.PROTECT, related_name='appointments',
        null=True, blank=True)
    service = models.ForeignKey(
        SERVICE_FK,
        on_delete=models.PROTECT, related_name='appointments')
    slot = models.ForeignKey(
        SLOT_FK,
        on_delete=models.PROTECT, related_name='appointments')
    session = models.ForeignKey(
        SESSION_FK,
        on_delete=models.PROTECT, related_name='appointments')
    guest = models.ForeignKey(
        GUEST_FK,
        on_delete=models.PROTECT, related_name='appointments',
        null=True, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=12,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING)
    booking_channel = models.CharField(
        max_length=20,
        choices=BookingChannel.choices,
        default=BookingChannel.ONLINE)

    is_walk_in = models.BooleanField(default=False)
    walk_in_name = models.CharField(max_length=120, blank=True)
    walk_in_phone = models.CharField(max_length=32, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at',]
        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F('start_time')), name='appt_valid_time'),
        ]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['booking_channel']),
            models.Index(fields=['start_time']),
        ]

    def __str__(self):
        who = self.patient or self.guest or "Unknown"
        return f"Appointment {self.pk} * {who} * {self.status}"

    def clean(self):
        if bool(self.patient) == bool(self.guest):
            raise ValidationError("Exactly one of patient or guest must be provided")

        if self.is_walk_in and self.booking_channel != BookingChannel.WALK_IN:
            raise ValidationError({"is_walk_in": "When walk-in, booking channel must be WALKIN."})

        if self.is_walk_in and not (self.walk_in_name and self.walk_in_phone):
            raise ValidationError("Walk-in appointments requires walk-in name and phone.")

class AppointmentNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notes')
    author_name = models.CharField(max_length=80)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at',]

    def __str__(self):
        return f"Note by {self.author_name} on {self.appointment}"

class AppointmentAudit(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='audit')
    old_status = models.CharField(max_length=12, choices=AppointmentStatus.choices, blank=True)
    new_status = models.CharField(max_length=12, choices=AppointmentStatus.choices, blank=True)
    changed_at = models.DateTimeField(default=timezone.now)
    changed_by = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ['changed_at',]

    def __str__(self):
        return f"Audit #{self.pk} -> {self.appointment_id}: {self.old_status} -> {self.new_status}"