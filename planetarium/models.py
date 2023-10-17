import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from user.models import User


class ShowTheme(models.Model):
    name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return str(self.name)


def astronomy_show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "astronomy_shows", filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=64, null=True)
    description = models.ManyToManyField(ShowTheme, related_name="astronomy_shows")
    image = models.ImageField(null=True, upload_to=astronomy_show_image_file_path)

    def __str__(self):
        return str(self.title)


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255, null=True)
    rows = models.IntegerField(default=0)
    seats_in_row = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f" {self.astronomy_show}: {self.planetarium_dome}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_sessions = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="tickets"
    )
    reservations = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "show_sessions")
        ordering = ("row",)

    @staticmethod
    def validate_seat(
        seat: int, row: int, seats_in_row: int, rows: int, error_to_raise
    ):
        if not (1 <= seat <= seats_in_row):
            raise error_to_raise(
                {"seat": f"seat must be in range [1, {seats_in_row}], not {seat}"}
            )

        if not (1 <= row <= rows):
            raise ValidationError(
                {"rows": f"row must be in range [1, {rows}, not {row}]"}
            )

    def clean(self):
        Ticket.validate_seat(
            self.seat,
            self.row,
            self.show_sessions.planetarium_dome.seats_in_row,
            self.show_sessions.planetarium_dome.rows,
            ValidationError,
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
