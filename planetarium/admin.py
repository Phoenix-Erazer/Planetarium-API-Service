from django.contrib import admin

from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    ShowSession,
    Ticket,
    Reservation,
)


@admin.register(ShowTheme)
class ShowThemeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(AstronomyShow)
class AstronomyShowAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    list_filter = ["title"]
    search_fields = ["title"]


@admin.register(ShowSession)
class ShowSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "astronomy_show", "planetarium_dome", "show_time"]
    search_fields = ["planetarium_dome"]


@admin.register(PlanetariumDome)
class PlanetariumDomeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "rows", "seats_in_row"]
    list_filter = ["name"]
    search_fields = ["name"]


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "row", "seat", "show_sessions", "reservation"]
    search_fields = ["show_sessions"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_filter = ["user"]
    search_fields = ["user__username"]
    inlines = (TicketInline,)
