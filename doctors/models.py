from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

# Create your models here.


class Doctor(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True)
    prc_license_no = models.CharField(max_length=64, unique=True)
    specialty = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['active']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

class Service(models.Model):
    name = models.CharField(max_length=80, unique=True)
    default_duration_min = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=15)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class DoctorService(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_services")
    duration_min = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('doctor', 'service')]
        indexes = [
            models.Index(fields=['doctor', 'service']),
        ]

    def __str__(self):
        return f"{self.doctor} - {self.service} ({self.duration_min}m)"

class Clinic(models.Model):
    name = models.CharField(max_length=120)
    address_line = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=80, blank=True)
    province = models.CharField(max_length=80, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=64, default="Asia/Manila")
    phone = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('name', 'address_line', 'city', 'province', 'zip_code')]
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class Room(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=80)
    capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('clinic', 'name')]
        ordering = ['clinic__name', 'name']

class DoctorClinic(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="clinics")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinics")
    default_duration_min = models.PositiveIntegerField( default=15, validators=[MinValueValidator(1)])
    max_daily_bookings = models.PositiveIntegerField(default=50, validators=[MinValueValidator(1)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('doctor', 'clinic')]
        ordering = ['doctor__last_name', 'clinic__name']

    def __str__(self):
        return f"{self.doctor} @ {self.clinic}"