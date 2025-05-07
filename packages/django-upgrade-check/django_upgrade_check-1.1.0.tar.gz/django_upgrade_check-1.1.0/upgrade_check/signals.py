from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .recorder import record_current_version


@receiver(post_migrate, dispatch_uid="upgrade_check.record_current_version")
def update_current_version(sender, **kwargs):
    record_current_version()
