"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: models.py

brief:
    Extends NetBox DCIM's core ``Cable`` model with additional metadata that
    are not part of the standard schema. For each physical cable we can store:

        • the actual cable length in metres (if known),
        • the cable manufacturer,
        • arbitrary notes or comments.

    The ``CableExtension`` model is linked one‑to‑one to ``Cable``.
    Deleting a ``Cable`` object deletes its extension automatically
    (``on_delete=models.CASCADE``).
"""

from django.db import models
from dcim.models import Cable

class CableExtension(models.Model):
    cable = models.OneToOneField(
        Cable,
        on_delete=models.CASCADE,
        related_name='extension'
    )
    cable_length = models.PositiveIntegerField(blank=True, null=True,
                                            help_text="Cable length in meters")
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Extension for cable {self.cable.id}"
