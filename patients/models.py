from datetime import date

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=32, blank=True,
        validators=[RegexValidator(r"^[0-9+\-()]*$", "Digits and + - ( ) only.")]
    )
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def age(self) -> int | None:
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

class GuestPatient(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=32, blank=True,
        validators=[RegexValidator(r"^[0-9+\-()]*$", "Digits and + - ( ) only.")]
    )
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return f"Guest: {self.last_name}, {self.first_name}"