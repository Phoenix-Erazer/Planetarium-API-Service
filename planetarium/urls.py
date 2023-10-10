from django.urls import path, include

from planetarium.views import (
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    AstronomyShowViewSet,
    ReservationViewSet,
    ShowSessionViewSet,
    TicketViewSet,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("planetarium-domes", PlanetariumDomeViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)
router.register("reservations", ReservationViewSet)
router.register("show-sessions", ShowSessionViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [
    # path("show_themes/", show_theme_list, name="show-theme-list"),
    path("", include(router.urls))
]

app_name = "planetarium"
