from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from planetarium.models import ShowTheme, PlanetariumDome
from planetarium.serializers import (
    ShowThemeSerializers,
    PlanetariumDomeSerializers,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializers


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializers
