from datetime import timedelta, datetime

from django.db import transaction
from django.utils import timezone

from .models import ClinicSession, AvailabilitySlot, AvailabilityStatus, ClinicSessionStatus


def _dt_range(start_dt, end_dt, step_min):
    cur = start_dt
    delta = timedelta(minutes=step_min)
    while cur + delta < end_dt:
        yield cur, cur + delta
        cur += delta

@transaction.atomic
def regenerate_slots(session: ClinicSession, service, *, created_by=None):
    AvailabilitySlot.objects.filter(session=session).exclude(status=AvailabilityStatus.BOOKED).delete()

    start_dt = datetime.combine(session.date, session.start_time)
    end_dt = datetime.combine(session.date, session.end_time)
    bulk = []

    for s, e, in _dt_range(start_dt, end_dt, session.slot_minutes):
        bulk.append(AvailabilitySlot(
            session=session,
            service=service,
            slot_start=s,
            slot_end=e,
            status=AvailabilityStatus.AVAILABLE,
        ))
    AvailabilitySlot.objects.bulk_create(bulk)
    return len(bulk)

@transaction.atomic
def publish_session(session: ClinicSession):
    if session.status != ClinicSessionStatus.DRAFT:
        return False

    session.status = ClinicSessionStatus.PUBLISHED
    session.published_at = timezone.now()
    session.save(update_fields=['status', 'published_at'])
    return True

def close_expired_holds(now=None):
    now = now or timezone.now()
    qs = AvailabilitySlot.objects.filter(status=AvailabilityStatus.AVAILABLE.HELD, hold_expires__lte=now)
    return qs.update(status=AvailabilityStatus.AVAILABLE, hold_expires=now)