from django.apps import AppConfig


class ManagerSchoolConfig(AppConfig):
    name = 'manager_school'

    def ready(self):
        import manager_school.signals