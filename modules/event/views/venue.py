from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from modules.event.forms import VenueForm
from modules.event.models import Venue


@login_required
def venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('venue-list')
    else:
        form = VenueForm()
    return render(request, 'event/venue/create.html', {'form': form})


@login_required
def venue_update(request, venue_id):
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=Venue.objects.get(id=venue_id))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('venue-list')
    else:
        form = VenueForm(instance=Venue.objects.get(id=venue_id))
    return render(request, 'event/venue/create.html', {'form': form, 'id': venue_id})


@login_required
def venue_delete(venue_id):
    obj = Venue.objects.get(id=venue_id)
    obj.delete()
    return redirect('venue-list')


@login_required
def venue_list(request):
    owner = request.user
    venues = Venue.objects.all().filter(owner_id__exact=owner.id)
    return render(request, 'event/venue/list.html', {'venues': venues})
