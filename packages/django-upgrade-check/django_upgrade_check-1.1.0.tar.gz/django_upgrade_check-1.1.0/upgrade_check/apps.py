from django.apps import AppConfig


class DjangoUpgradeCheckConfig(AppConfig):
    name = "upgrade_check"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        # register checks and signals
        from . import checks  # noqa
        from . import signals  # noqa
