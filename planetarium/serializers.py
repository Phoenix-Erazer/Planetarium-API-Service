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


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class AstronomyShowSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "image")


class AstronomyShowImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "image")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    description = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class AstronomyShowDetailSerializer(AstronomyShowSerializer):
    description = ShowThemeSerializer(many=True, read_only=True)


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show_title = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome_name = serializers.CharField(source="planetarium_dome.name", read_only=True)
    planetarium_dome_seat = serializers.IntegerField(source="planetarium_dome.seats_in_row", read_only=True)
    planetarium_dome_row = serializers.IntegerField(source="planetarium_dome.rows", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = (
            "id", "astronomy_show_title", "planetarium_dome_name", "planetarium_dome_seat",
            "planetarium_dome_row", "show_time", "planetarium_dome", "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
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
        fields = ("id", "row", "seat", "show_sessions")


class TicketSeatRowSerializer(ShowSessionSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowDetailSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)
    tickets = TicketSeatRowSerializer(many=True, read_only=True)

    class Meta:
        model = ShowSession
        fields = (
            "id", "astronomy_show", "planetarium_dome", "show_time",
            "tickets")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False,  allow_empty=False)

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


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
