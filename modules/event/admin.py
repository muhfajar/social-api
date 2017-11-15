from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from modules.event.models import (
    Venue, EventType, Event, Ticket
)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'capacity', 'image')}),
        (_('Location'), {'fields': ('city', 'location',)}),
    )
    list_display = ('name', 'capacity', 'city')
    search_fields = ('name', 'city')
    ordering = ('name', 'city')
    list_filter = ('city',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'type', 'image')}),
        (_('Detail'), {'fields': ('venue', 'date', 'open_gate')}),
    )
    list_display = ('name', 'type', 'venue', 'date', 'open_gate')
    search_fields = ('name', 'type', 'venue', 'date', 'open_gate')
    ordering = ('name', 'type', 'venue', 'date', 'open_gate')
    list_filter = ('venue', 'type', 'date')


@admin.register(Ticket)
class EventTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'event', 'price', 'image')}),
    )
    list_display = ('name', 'event', 'price')
    search_fields = ('name', 'event', 'price')
    ordering = ('name', 'event', 'price')
