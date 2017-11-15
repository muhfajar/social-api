from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from modules.event.forms import EventForm
from modules.event.models import Event


@login_required
def event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('event-list')
    else:
        form = EventForm()
    return render(request, 'event/event/create.html', {'form': form, 'create': True})


@login_required
def event_update(request, event_id):
    if request.method == 'POST':
        form = EventForm(request.POST, instance=Event.objects.get(id=event_id))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('event-list')
    else:
        form = EventForm(instance=Event.objects.get(id=event_id))
    return render(request, 'event/event/create.html', {'form': form, 'id': event_id})


@login_required
def event_delete(event_id):
    obj = Event.objects.get(id=event_id)
    obj.delete()
    return redirect('event-list')


@login_required
def event_list(request):
    owner = request.user
    events = Event.objects.all().filter(owner_id__exact=owner.id)
    return render(request, 'event/event/list.html', {'events': events,
                                                     'url': request.build_absolute_uri("/").rstrip("/")})


def event_detail(request, event_id):
    event_data = Event.objects.get(id=event_id)
    return render(request, 'event/event/detail.html', {'event': event_data,
                                                       'url': request.build_absolute_uri("/").rstrip("/")})


@login_required
def category(request, event_type):
    owner = request.user
    events = Event.objects.all().filter(type__name__contains=event_type).filter(owner_id__exact=owner.id)
    return render(request, 'event/event/category.html', {'events': events, 'category': event_type})