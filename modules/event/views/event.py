import twitter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

from modules.event.forms import EventForm
from modules.event.models import Event
from social_api.settings import SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET


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
    return render(request, 'event/event/list.html', {'events': events})


def event_detail(request, event_id):
    event_data = Event.objects.get(id=event_id)
    return render(request, 'event/event/detail.html', {'event': event_data})


def tweet(request, event_id):
    event_data = Event.objects.get(id=event_id)
    url = request.build_absolute_uri('/')
    try:
        user_data = UserSocialAuth.objects.get(user_id__exact=event_data.owner)
    except UserSocialAuth.DoesNotExist:
        # fallback if user not login using twitter
        return redirect("https://twitter.com/intent/tweet?text=Please see my {} here: {}event/get/{}".format(
            event_data.name, url, event_data.id
        ))

    access_token = user_data.extra_data['access_token']
    oauth_token = access_token['oauth_token']
    oauth_secret = access_token['oauth_token_secret']

    t = twitter.Twitter(
        auth=twitter.OAuth(
            oauth_token, oauth_secret,
            SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET
        )
    )
    t.statuses.update(status="Please see my {} here: {}event/get/{}".format(event_data.name, url, event_data.id))

    return redirect('event-detail', event_id=event_id)


@login_required
def category(request, event_type):
    owner = request.user
    events = Event.objects.all().filter(type__name__contains=event_type).filter(owner_id__exact=owner.id)
    return render(request, 'event/event/category.html', {'events': events, 'category': event_type})
