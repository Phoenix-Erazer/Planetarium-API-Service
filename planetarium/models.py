from datetime import datetime

from django.conf import settings
from django.db import models
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


class Reservation(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="reservations")


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow, on_delete=models.CASCADE
    )
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_sessions = models.ForeignKey(ShowSession, on_delete=models.CASCADE)
    reservations = models.ForeignKey(Reservation, on_delete=models.CASCADE)

