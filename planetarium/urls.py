from django.urls import path, include

from planetarium.views import ShowThemeViewSet, PlanetariumDomeViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet)
router.register("planetarium-domes", PlanetariumDomeViewSet)


urlpatterns = [
    # path("show_themes/", show_theme_list, name="show-theme-list"),
    path("", include(router.urls))
]

app_name = "planetarium"
