from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from modules.event.forms import TicketForm
from modules.event.models import Ticket, Event


@login_required
def ticket(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.event = event
            obj.save()
            return redirect('event-list')
    else:
        form = TicketForm()
    return render(request, 'event/ticket/create.html', {'form': form, 'create': True, 'event': event})


@login_required
def ticket_update(request, ticket_id, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=Ticket.objects.get(id=ticket_id))
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.event = event
            obj.save()
            return redirect('event-list')
    else:
        form = TicketForm(instance=Ticket.objects.get(id=ticket_id))
    return render(request, 'event/ticket/create.html', {'form': form, 'id': ticket_id})


@login_required
def ticket_delete(ticket_id):
    obj = Ticket.objects.get(id=ticket_id)
    obj.delete()
    return redirect('event-list')


@login_required
def ticket_list(request, event_id):
    event = Event.objects.get(id=event_id)
    owner = request.user
    tickets = Ticket.objects.all().filter(owner_id__exact=owner.id).filter(event_id__exact=event.id)
    return render(request, 'event/ticket/list.html', {'tickets': tickets, 'event': event})
