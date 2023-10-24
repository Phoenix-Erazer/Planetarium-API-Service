from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from planetarium.models import ShowTheme, ShowSession, AstronomyShow, PlanetariumDome
from planetarium.serializers import ShowSessionSerializer

SHOW_THEME_URL = reverse("planetarium:showsession-list")


def sample_show_session(**params):
    default = {"show_time": "2023-10-22T19:05:00+03:00"}
    default.update(params)

    return ShowSession.objects.create(**default)


class UnauthenticatedShowSessionApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_THEME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@gmail.com",
            "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_shows_session(self):
        sample_show_session()
        show_session_with_astronomy_show = sample_show_session()
        planetarium_dome = PlanetariumDome.objects.create(name="test", rows=5, seats_in_row=5)
        show_theme = ShowTheme.objects.create(name="name test")

        astronomy_show = AstronomyShow.objects.create(
            title="astronomy_show1_test",
            description=show_theme
        )

        show_session_with_astronomy_show.astronomy_show.add(astronomy_show)
        show_session_with_astronomy_show.planetarium_dome.add(planetarium_dome)

        res = self.client.get(SHOW_THEME_URL)

        shows_session = ShowSession.objects.all()
        serializer = ShowSessionSerializer(shows_session, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
