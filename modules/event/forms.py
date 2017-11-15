from django.forms import ModelForm, HiddenInput

from modules.event.models import (
    Venue,
    EventType,
    Event
)


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


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['owner']
