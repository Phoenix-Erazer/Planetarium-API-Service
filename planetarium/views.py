from rest_framework import viewsets
from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    Reservation,
    ShowSession,
    Ticket,
)
from planetarium.serializers import (
    ShowThemeSerializers,
    PlanetariumDomeSerializers,
    AstronomyShowSerializers,
    ReservationSerializers,
    ShowSessionSerializers,
    TicketSerializers,
    ShowSessionListSerializers,
    ReservationListSerializers,
    UserSerializer,
    AstronomyShowDetailSerializers,
    AstronomyShowListSerializers,
    TicketListSerializers,
    ShowSessionDetailSerializers, TicketDetailSerializers,
)
from user.models import User


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializers


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializers


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all().prefetch_related("description")
    serializer_class = AstronomyShowSerializers

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AstronomyShowDetailSerializers
        if self.action == "list":
            return AstronomyShowListSerializers

        return AstronomyShowSerializers


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related("user")
    serializer_class = ReservationSerializers

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializers

        return ReservationSerializers


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related("astronomy_show", "planetarium_dome")
    serializer_class = ShowSessionSerializers

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializers
        if self.action == "retrieve":
            return ShowSessionDetailSerializers

        return ShowSessionSerializers


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("show_sessions", "reservations")
    serializer_class = TicketSerializers

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializers
        if self.action == "retrieve":
            return TicketDetailSerializers
        return TicketSerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("user")
    serializer_class = UserSerializer
