from rest_framework import viewsets
from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    Reservation,
    ShowSession, Ticket,
)
from planetarium.serializers import (
    ShowThemeSerializers,
    PlanetariumDomeSerializers,
    AstronomyShowSerializers,
    ReservationSerializers,
    ShowSessionSerializers,
    TicketSerializers,
    ShowSessionListSerializers,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializers


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializers


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializers


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializers


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related("astronomy_show", "planetarium_dome")
    serializer_class = ShowSessionSerializers

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializers

        return ShowSessionSerializers


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializers
