from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

ROLE_TO_GROUP = {
    User.Role.SYSADMIN: "System Admin",
    User.Role.DOCTOR: "Doctor",
    User.Role.STAFF: "Clinic Staff",
    User.Role.PATIENT: "Patient",
}

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_group_on_save(sender, instance: User, created, **kwargs):
    group_name = ROLE_TO_GROUP.get(instance.role)
    if not group_name:
        return

    # Remove from other RBAC groups, add to the current one
    rbac_groups = Group.objects.filter(name__in=ROLE_TO_GROUP.values())
    instance.groups.remove(*rbac_groups)
    group = Group.objects.get(name=group_name)
    instance.groups.add(group)