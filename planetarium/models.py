from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return str(self.name)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=64, null=True)
    description = models.ManyToManyField(ShowTheme, related_name="astronomy_shows")

    def __str__(self):
        return str(self.title)


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255, null=True)
    rows = models.IntegerField(default=0)
    seats_in_row = models.IntegerField()


class Reservation:
    created_at = models.DateTimeField()
    # user


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    show_time = models.DateTimeField()


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_sessions = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    reservations = models.ForeignKey(Reservation, on_delete=models.CASCADE)
