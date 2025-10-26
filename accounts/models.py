from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        SYSADMIN = "SYSADMIN", "System Admin"
        DOCTOR = "DOCTOR", "Doctor"
        STAFF = "STAFF", "Clinic Staff"
        PATIENT = "PATIENT", "Patient"

    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.PATIENT,
    )