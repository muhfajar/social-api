from django.forms import ModelForm, HiddenInput

from modules.event.models import (
    Venue,
    EventType)


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'
        exclude = ['owner', 'location']


class EventTypeForm(ModelForm):
    class Meta:
        model = EventType
        fields = '__all__'
        exclude = ['owner']
