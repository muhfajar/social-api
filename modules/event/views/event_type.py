from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from modules.event.forms import EventTypeForm
from modules.event.models import EventType


@login_required
def event_type(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('event-type-list')
    else:
        form = EventTypeForm()
    return render(request, 'event/event_type/create.html', {'form': form, 'create': True})


@login_required
def event_type_update(request, event_type_id):
    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=EventType.objects.get(id=event_type_id))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect('event-type-list')
    else:
        form = EventTypeForm(instance=EventType.objects.get(id=event_type_id))
    return render(request, 'event/event_type/create.html', {'form': form, 'id': event_type_id})


@login_required
def event_type_delete(event_type_id):
    obj = EventType.objects.get(id=event_type_id)
    obj.delete()
    return redirect('event-type-list')


@login_required
def event_type_list(request):
    owner = request.user
    event_types = EventType.objects.all().filter(owner_id__exact=owner.id)
    return render(request, 'event/event_type/list.html', {'event_types': event_types})
