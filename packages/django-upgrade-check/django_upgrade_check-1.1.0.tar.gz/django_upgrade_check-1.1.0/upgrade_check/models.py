import socket

from django.db import models
from django.utils.translation import gettext_lazy as _


def get_machine_name():
    return socket.gethostname()


class Version(models.Model):
    """
    Capture metadata about a "deployed" version.

    We tap into the ``post_migrate`` signal to capture a "deploy" event, and create a
    record of this. Multiple instances could be racing to perform such a "deploy", it
    may even just be more instances being scaled up. This means there are no strong
    guarantees about a version deploy being unique or only registered once.

    The information tracked in this model roughly allows reconstructing the deploy
    history of an instance. It's primarily used to figure out what the "last deployed"
    version to allow making comparisons for upgrade-checking purposes. Anything else is
    best-effort and captures potentially interesting metadata.
    """

    version = models.CharField(
        _("version"),
        max_length=100,
        editable=False,
        help_text=_("The recorded version number."),
    )
    git_sha = models.CharField(
        _("git hash"),
        max_length=100,
        editable=False,
        help_text=_("The recorded git commit hash."),
    )
    timestamp = models.DateTimeField(
        _("timestamp"),
        auto_now_add=True,
        help_text=_("Timestamp reflecting when this version was recorded."),
    )
    machine_name = models.CharField(
        _("machine name"),
        max_length=255,
        default=get_machine_name,
        editable=False,
        help_text=_("The host name of the machine this version was recorded on."),
    )

    class Meta:
        verbose_name = _("version")
        verbose_name_plural = _("versions")
        indexes = [
            models.Index(models.F("timestamp").desc(), name="timestamp_idx"),
        ]
        models.constraints = [
            models.CheckConstraint(
                name="non_empty_version", check=~models.Q(version="")
            ),
        ]
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.version}@{self.machine_name} - {self.timestamp.isoformat()}"
