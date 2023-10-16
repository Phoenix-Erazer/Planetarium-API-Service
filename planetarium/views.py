from django.db.models import Count, F
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    Reservation,
    ShowSession,
    Ticket,
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
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
from rest_framework.pagination import PageNumberPagination


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class AstronomyShowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AstronomyShow.objects.all().prefetch_related("description")
    serializer_class = AstronomyShowSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AstronomyShowDetailSerializer
        if self.action == "list":
            return AstronomyShowListSerializer

        return AstronomyShowSerializer


class ReservationPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 100


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.prefetch_related(
                    "tickets__show_sessions",
                    # "tickets__show_sessions__astronomy_show",
                    # "tickets__show_sessions__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer


class ShowSessionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )
