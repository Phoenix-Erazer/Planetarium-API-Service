from django.db.models import Count, F
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
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
    AstronomyShowImageSerializer,
)
from rest_framework.pagination import PageNumberPagination


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AstronomyShowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the astronomy shows with filters"""
        title = self.request.query_params.get("title")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("description")
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AstronomyShowDetailSerializer
        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "upload_image":
            return AstronomyShowImageSerializer

        return AstronomyShowSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        astronomy_show = self.get_object()
        serializer = self.get_serializer(astronomy_show, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Filter by title (ex. ?title=astronomy show)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 100


class ReservationViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_sessions",
        # "tickets__show_sessions__astronomy_show",
        # "tickets__show_sessions__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

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
    GenericViewSet,
):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = (
                queryset.select_related("astronomy_show", "planetarium_dome").annotate(
                    tickets_available=(
                        F("planetarium_dome__seats_in_row")
                        * F("planetarium_dome__rows")
                        - Count("tickets")
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
