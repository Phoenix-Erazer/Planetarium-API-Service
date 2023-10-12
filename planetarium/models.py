from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from user.models import User


class ShowTheme(models.Model):
    name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return str(self.name)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=64, null=True)
    description = models.ManyToManyField(
        ShowTheme, related_name="astronomy_shows"
    )

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
    astronomy_show = models.ForeignKey(
        AstronomyShow, on_delete=models.CASCADE
    )
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f" {self.astronomy_show}: {self.planetarium_dome}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_sessions = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservations = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    def clean(self):
        if not(1 <= self.seat <= self.show_sessions.planetarium_dome.seats_in_row):
            raise ValidationError({
                "seat": f"seat must be in range [1, {self.show_sessions.planetarium_dome.seats_in_row}, not {self.seat}"
            })

        if not(1 <= self.row <= self.show_sessions.planetarium_dome.rows):
            raise ValidationError({
                "rows": f"row must be in range [1, {self.show_sessions.planetarium_dome.rows}, not {self.row}"
            })

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ("row", "seat", "show_sessions")
