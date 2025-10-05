from django.contrib import admin

from .models import AppointmentNote, Appointment, AppointmentAudit


# Register your models here.
class AppointmentNoteInline(admin.TabularInline):
    model = AppointmentNote
    extra = 0

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'booking_channel', 'is_walk_in', 'start_time',
                    'end_time', 'patient', 'guest', 'service', 'slot')
    list_filter = ('status', 'booking_channel', 'is_walk_in', 'created_at')
    search_fields = ('walk_in_name', 'walk_in_phone', 'patient__first_name',
                     'patient__last_name', 'service__name')
    autocomplete_fields = ('patient', 'service', 'slot', 'guest', 'session')
    inlines = [AppointmentNoteInline]

@admin.register(AppointmentNote)
class AppointmentNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'author_name', 'created_at')
    search_fields = ('appointment__patient__last_name', 'author_name')

@admin.register(AppointmentAudit)
class AppointmentAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('old_status', 'new_status')
    search_fields = ('appointment__patient__last_name', 'changed_by')