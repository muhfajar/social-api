from django.db import models

from location_field.models.plain import PlainLocationField


class Venue(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7, verbose_name='Coordinate')
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    type = models.OneToOneField(EventType)
    venue = models.OneToOneField(Venue)
    date = models.DateField()
    open_gate = models.TimeField()
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event)
    price = models.IntegerField()
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name
