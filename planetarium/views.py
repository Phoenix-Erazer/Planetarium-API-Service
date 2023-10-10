from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from planetarium.models import ShowTheme
from planetarium.serializers import ShowThemeSerializers


class ShowThemeViewSet(
    viewsets.ModelViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializers
