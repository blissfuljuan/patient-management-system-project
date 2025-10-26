from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

ROLE_GROUPS = {
    "System Admin" : [],
    "Doctor" : [],
    "Clinic Staff" : [],
    "Patient" : [],
}

MODEL_PERMS = {
    "patients.Patient": ["add_patient", "view_patient", "change_patient", "delete_patient"],
    "appointments.Appointment": ["add_appointment", "view_appointment", "change_appointment"],
    "doctors.Doctor": ["view_doctor", "change_doctor"],
}

ROLE_RULES = {
    "System Admin": ["*"],
    "Doctor": [
        "patients.Patient:view_patient",
        "patients.Appointment:add_appointment",
        "patients.Appointment:view_appointment",
        "patients.Appointment:change_appointment",
        "doctors.Doctor:view_doctor",
    ],
    "Clinic Staff": [
        "patients.Patient:add_patient",
        "patients.Patient:view_patient",
        "patients.Patient:change_patient",
        "patients.Appointment:add_appointment",
        "patients.Appointment:view_appointment",
        "patients.Appointment:change_appointment",
        "doctors.Doctor:view_doctor",
    ],
    "Patient": [
        "patients.Patient:view_patient",
        "patients.Appointment:view_appointment",
    ],
}

class Command(BaseCommand):
    help = 'Create RBAC groups and assign permissions'

    def handle(self, *args, **options):
        # Ensure group exist
        groups = {name: Group.objects.get_or_create(name=name)[0] for name in ROLE_GROUPS}

        # Build a map of "app.Model:perm_codename" -> Permission
        perm_map = {}
        for model_label, codenames in MODEL_PERMS.items():
            app_label, model_name = model_label.split('.')
            model = apps.get_model(app_label, model_name)
            for perm in Permission.objects.filter(content_type__app_label=app_label,
                                                  content_type__model=model._meta.model_name):
                perm_map[f"{app_label}.{model_name}:{perm.codename}"] = perm

        # Assign permission per Role
        all_perms = list(Permission.objects.all())
        for role, rules in ROLE_RULES.items():
            group = groups[role]
            group.permissions.clear()
            if rules == ["*"]:
                group.permissions.set(all_perms)
            else:
                selected = []
                for rule in rules:
                    p = perm_map.get(rule)
                    if p:
                        selected.append(p)
                group.permissions.set(selected)

        self.stdout.write(self.style.SUCCESS('RBAC group and permissions configured.'))