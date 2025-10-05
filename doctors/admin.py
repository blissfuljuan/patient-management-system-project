from django.contrib import admin

from doctors import models
from doctors.models import Room, DoctorService, Service, DoctorClinic


# Register your models here.
@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name','first_name', 'email', 'prc_license_no', 'specialty', 'active')
    search_fields = ('last_name', 'first_name', 'email', 'prc_license_no', 'specialty')
    list_filter = ('active',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'default_duration_min', 'active')
    list_field = ('active',)
    search_fields = ('name', )

@admin.register(DoctorService)
class DoctorServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'service', 'duration_min', 'fee_amount', 'active')
    list_filter = ('active',)
    autocomplete_fields = ('doctor', 'service')

@admin.register(models.Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'province', 'phone', 'active')
    list_filter = ('active', )
    search_fields = ('name', 'city', 'province')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'clinic', 'name', 'capacity', 'active')
    list_filter = ('active', 'clinic')
    search_fields = ('name', 'clinic__name')
    autocomplete_fields = ('clinic',)

@admin.register(DoctorClinic)
class DoctorClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'clinic', 'default_duration_min', 'max_daily_bookings', 'active')
    search_fields = ('doctor__last_name', 'clinic__name')
    list_filter = ('active', )
    autocomplete_fields = ('doctor', 'clinic')