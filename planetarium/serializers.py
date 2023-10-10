from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    Reservation, ShowSession, Ticket
)


class ShowThemeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class AstronomyShowSerializers(serializers.ModelSerializer):
    # description = ShowThemeSerializers(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description",)


class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user",)


class ShowSessionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializers(ShowSessionSerializers):
    astronomy_show = AstronomyShowSerializers(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializers(many=False, read_only=True)


class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_sessions", "reservations")
