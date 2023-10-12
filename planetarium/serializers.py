from django.db import transaction
from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    Reservation,
    ShowSession,
    Ticket
)
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class ShowThemeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class AstronomyShowSerializers(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description",)


class AstronomyShowListSerializers(AstronomyShowSerializers):
    description = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class AstronomyShowDetailSerializers(AstronomyShowSerializers):
    description = ShowThemeSerializers(many=True, read_only=True)


class ShowSessionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializers(ShowSessionSerializers):
    astronomy_show_title = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome_name = serializers.CharField(source="planetarium_dome.name", read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show_title", "planetarium_dome_name", "show_time", "planetarium_dome")


class TicketSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializers, self).validate(attrs)
        Ticket.validate_seat(
            attrs["seat"],
            attrs["row"],
            attrs["show_sessions"].planetarium_dome.seats_in_row,
            attrs["show_sessions"].planetarium_dome.rows,
            serializers.ValidationError
        )

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_sessions", "reservations")


class TicketSeatRowSerializers(ShowSessionSerializers):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class ShowSessionDetailSerializers(ShowSessionSerializers):
    astronomy_show = AstronomyShowDetailSerializers(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializers(many=False, read_only=True)
    tickets = TicketSeatRowSerializers(many=True, read_only=True)

    class Meta:
        model = ShowSession
        fields = (
            "id", "astronomy_show", "planetarium_dome", "show_time",
            "tickets")
# class TicketCreateReservationSerializers(TicketSerializers):
#     reservations = ReservationSerializers(many=False, read_only=False)


class ReservationSerializers(serializers.ModelSerializer):
    tickets = TicketSerializers(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop('tickets')
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation
