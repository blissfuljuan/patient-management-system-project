from django.contrib import admin
from patients.models import Patient, GuestPatient


# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'phone', 'dob', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('dob', 'created_at')

@admin.register(GuestPatient)
class GuestPatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'dob', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')