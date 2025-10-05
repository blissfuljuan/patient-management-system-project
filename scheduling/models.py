from MySQLdb.constants.CR import NULL_POINTER
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class ClinicSessionStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PUBLISHED = 'PUBLISHED', 'Published'
    CLOSED = 'CLOSED', 'Closed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class ClinicSession(models.Model):
    doctor_clinic = models.ForeignKey('doctors.DoctorClinic', on_delete=models.CASCADE, related_name='sessions')
    room = models.ForeignKey('doctors.Room', on_delete=models.CASCADE, related_name='sessions')

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    slot_minutes = models.PositiveIntegerField(default=15, validators=[MinValueValidator(1)])
    max_capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    overbook_limit = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])

    status = models.CharField(max_length=12, choices=ClinicSessionStatus.choices, default=ClinicSessionStatus.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(end_time__gt=models.F('start_time')), name='session_valid_time'),
        ]

    def __str__(self):
        return f"{self.doctor_clinic} * {self.date} {self.start_time}-{self.end_time}"

class AvailabilityStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    HELD = 'HELD', 'Held'
    BOOKED = 'BOOKED', 'Booked'
    CLOSED = 'CLOSED', 'Closed'

class AvailabilitySlot(models.Model):
    session = models.ForeignKey(ClinicSession, on_delete=models.CASCADE, related_name='slots')
    service = models.ForeignKey('doctors.Service', on_delete=models.PROTECT, related_name='slots')

    slot_start = models.DateTimeField()
    slot_end = models.DateTimeField()
    status = models.CharField(max_length=10, choices=AvailabilityStatus.choices, default=AvailabilityStatus.AVAILABLE)
    hold_expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-slot_start']
        unique_together = [('session', 'slot_start', 'service')]
        constraints = [
            models.CheckConstraint(check=models.Q(slot_end__gt=models.F('slot_start')), name='slot_valid_time'),
        ]

    def __str__(self):
        return f"{self.session} * {self.slot_start:%H:%M}-{self.slot_end:%H:%M}"

class SessionChange(models.Model):
    session = models.ForeignKey(ClinicSession, on_delete=models.CASCADE, related_name='changes')
    change_type = models.CharField(max_length=40)
    details_json = models.JSONField(default=dict, blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='session_changes')
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

class SessionCancellation(models.Model):
    session = models.ForeignKey(ClinicSession, on_delete=models.CASCADE, related_name='cancellations')
    reason = models.CharField(max_length=255, blank=True)
    policy_code = models.CharField(max_length=40, blank=True)
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='session_cancellations')
    cancelled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-cancelled_at']