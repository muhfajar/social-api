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
    list_display = ('name', 'capacity', 'city', 'owner')
    search_fields = ('name', 'city')
    ordering = ('name', 'city')
    list_filter = ('city', 'owner')

    def get_queryset(self, request):
        qs = super(VenueAdmin, self).get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name', 'owner')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('owner',)

    def get_queryset(self, request):
        qs = super(EventTypeAdmin, self).get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'type', 'image')}),
        (_('Detail'), {'fields': ('venue', 'date', 'open_gate')}),
    )
    list_display = ('name', 'type', 'venue', 'date', 'open_gate', 'owner')
    search_fields = ('name', 'type', 'venue', 'date', 'open_gate')
    ordering = ('name', 'type', 'venue', 'date', 'open_gate')
    list_filter = ('venue', 'type', 'date', 'owner')

    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'event', 'price', 'image')}),
    )
    list_display = ('name', 'event', 'price', 'owner')
    search_fields = ('name', 'event', 'price')
    ordering = ('name', 'event', 'price')
    list_filter = ('owner',)

    def get_queryset(self, request):
        qs = super(TicketAdmin, self).get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
