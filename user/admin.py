from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    ShowSession,
    Ticket)
from .models import User


admin.site.register(User, UserAdmin)
admin.site.register(PlanetariumDome)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(ShowSession)
admin.site.register(Ticket)