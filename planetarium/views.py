from django.db.models import Count, F
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
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    ReservationSerializer,
    ShowSessionSerializer,
    TicketSerializer,
    ShowSessionListSerializer,
    AstronomyShowDetailSerializer,
    AstronomyShowListSerializer,
    ShowSessionDetailSerializer,
    ReservationListSerializer,
)
from user.models import User


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all().prefetch_related("description")
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AstronomyShowDetailSerializer
        if self.action == "list":
            return AstronomyShowListSerializer

        return AstronomyShowSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related(
                    "tickets__show_sessions",
                    # "tickets__show_sessions__astronomy_show",
                    # "tickets__show_sessions__planetarium_dome"
    )
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = (
                queryset
                .select_related("astronomy_show", "planetarium_dome")
                .annotate(
                    tickets_available=(
                            F("planetarium_dome__seats_in_row") *
                            F("planetarium_dome__rows") -
                            Count("tickets")
                    )
                )
            ).order_by("id")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionDetailSerializer

        return ShowSessionSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("show_sessions", "reservations")
    serializer_class = TicketSerializer
