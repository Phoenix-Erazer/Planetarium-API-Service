from rest_framework import viewsets
from planetarium.models import ShowTheme, PlanetariumDome, AstronomyShow, Reservation
from planetarium.serializers import (
    ShowThemeSerializers,
    PlanetariumDomeSerializers,
    AstronomyShowSerializers, ReservationSerializers,
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
