from django.contrib import admin

from scheduling.models import AvailabilitySlot, ClinicSession, SessionChange, SessionCancellation


# Register your models here.
class AvailabilitySlotInline(admin.TabularInline):
    model = AvailabilitySlot
    extra = 0
    readonly_fields = ('slot_start', 'slot_end', 'status', 'hold_expires')
    autocomplete_fields = ('service', )

@admin.register(ClinicSession)
class ClinicSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor_clinic', 'room', 'date', 'start_time', 'end_time', 'status', 'published_at')
    list_filter = ('status', 'date')
    search_fields = ('doctor_clinic__doctor__last_name', 'doctor_clinic__first_name')
    autocomplete_fields = ('doctor_clinic','room')
    inlines = [AvailabilitySlotInline, ]

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'service', 'slot_start', 'slot_end', 'status', 'hold_expires')
    list_filter = ('status', 'service')
    autocomplete_fields = ('session', 'service')

@admin.register(SessionChange)
class SessionChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'change_type', 'changed_by', 'changed_at')
    autocomplete_fields = ('session', 'changed_by')

@admin.register(SessionCancellation)
class SessionCancellationAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'policy_code', 'cancelled_by', 'cancelled_at')
    autocomplete_fields = ('session', 'cancelled_by')