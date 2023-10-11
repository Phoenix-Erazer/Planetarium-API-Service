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


class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user",)


class ReservationListSerializers(ReservationSerializers):
    user = UserSerializer(many=False, read_only=True)


class ShowSessionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializers(ShowSessionSerializers):
    astronomy_show_title = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome_name = serializers.CharField(source="planetarium_dome.name", read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show_title", "planetarium_dome_name", "show_time")


class ShowSessionDetailSerializers(ShowSessionSerializers):
    astronomy_show = AstronomyShowDetailSerializers(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializers(many=False, read_only=True)


class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_sessions", "reservations")


class TicketListSerializers(TicketSerializers):
    # show_sessions_user = serializers.CharField(source="show_sessions.user", read_only=True)
    # reservations_user = serializers.CharField(source="reservations_user.user", read_only=True)

    # class Meta:
    #     model = Ticket
    #     fields = ("id", "row", "seat", "show_sessions", "reservations_user")
    show_sessions = ShowSessionSerializers(many=False, read_only=True)
    reservations = ReservationSerializers(many=False, read_only=True)


class TicketDetailSerializers(TicketSerializers):
    show_sessions = ShowSessionSerializers(many=False, read_only=True)
    reservations = ReservationSerializers(many=False, read_only=True)
