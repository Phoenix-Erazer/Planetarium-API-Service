from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from planetarium.models import ShowTheme, ShowSession, AstronomyShow, PlanetariumDome
from planetarium.serializers import ShowSessionSerializer, ShowSessionListSerializer, ShowSessionDetailSerializer

SHOW_SESSION_URL = reverse("planetarium:showsession-list")


def detail_url(show_session_id: int):
    return reverse("planetarium:showsession-detail", args=[show_session_id])


def sample_show_session(**params):
    default = {"show_time": "2023-10-22T19:05:00+03:00"}
    default.update(params)

    return ShowSession.objects.create(**default)


class UnauthenticatedShowSessionApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)
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
        planetarium_dome = PlanetariumDome.objects.create(name="test", rows=5, seats_in_row=5)
        show_theme = ShowTheme.objects.create(name="name test")

        astronomy_show = AstronomyShow.objects.create(
            title="astronomy_show1_test",
        )
        astronomy_show.description.add(show_theme)

        tickets_available = (
                planetarium_dome.rows * planetarium_dome.rows
        )

        show_session_with_astronomy_show = sample_show_session(
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
        )

        res = self.client.get(SHOW_SESSION_URL)

        shows_session = ShowSession.objects.all()
        serializer = ShowSessionListSerializer(shows_session, many=True)

        print("res.data:", res.data)
        print("serializer.data:", res.data)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_shows_session(self):
        planetarium_dome = PlanetariumDome.objects.create(name="test", rows=5, seats_in_row=5)
        show_theme = ShowTheme.objects.create(name="name test")

        astronomy_show = AstronomyShow.objects.create(
            title="astronomy_show1_test",
        )
        astronomy_show.description.add(show_theme)

        show_session = sample_show_session(
            astronomy_show=astronomy_show,
            planetarium_dome=planetarium_dome,
        )

        url = detail_url(show_session.id)
        res = self.client.get(url)

        serializer = ShowSessionDetailSerializer(show_session)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_shows_session(self):
        planetarium_dome = PlanetariumDome.objects.create(name="test", rows=5, seats_in_row=5)
        show_theme = ShowTheme.objects.create(name="name test")

        astronomy_show = AstronomyShow.objects.create(
            title="astronomy_show1_test",
        )
        astronomy_show.description.add(show_theme)

        payload = {
            "astronomy_show": astronomy_show,
            "planetarium_dome": planetarium_dome
        }

        res = self.client.post(SHOW_SESSION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


# class AdminShowSessionApiTests(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             "admin@gmail.com",
#             "adminpassword",
#             is_staff=True
#         )
#         self.client.force_authenticate(self.user)
#
#     def test_create_show_session(self):
#         planetarium_dome1 = PlanetariumDome.objects.create(name="test", rows=5, seats_in_row=5)
#         show_theme = ShowTheme.objects.create(name="name test")
#
#         astronomy_show1 = AstronomyShow.objects.create(
#             title="astronomy_show1_test",
#         )
#         astronomy_show1.description.add(show_theme)
#
#         payload = {
#             "astronomy_show": astronomy_show1.id,
#             "planetarium_dome": planetarium_dome1.id,
#             "show_time": "2023-10-22T19:05:00+03:00"
#         }
#
#         res = self.client.post(SHOW_SESSION_URL, payload)
#         show_session = ShowSession.objects.get(id=res.json()["id"])
#         astronomy_shows = show_session.astronomy_show
#         planetarium_domes = show_session.planetarium_dome
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertIn(planetarium_dome1, planetarium_domes)
#         self.assertIn(astronomy_show1, astronomy_shows)

