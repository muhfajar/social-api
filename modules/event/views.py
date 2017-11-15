from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

from modules.event.forms import VenueForm
from modules.event.models import Event, Venue


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            # set permission
            group = Group.objects.get(name='event-cordinator')
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    owner = request.user
    events = Event.objects.all().filter(owner_id__exact=owner.id)
    return render(request, 'event/home.html', {'events': events})


@login_required
def category(request, event_type):
    owner = request.user
    events = Event.objects.all().filter(type__name__contains=event_type).filter(owner_id__exact=owner.id)
    return render(request, 'event/category.html', {'events': events, 'category': event_type})


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'event/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        password_form = PasswordChangeForm
    else:
        password_form = AdminPasswordChangeForm

    if request.method == 'POST':
        form = password_form(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = password_form(request.user)
    return render(request, 'event/password.html', {'form': form})


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
def venue_delete(request, venue_id):
    obj = Venue.objects.get(id=venue_id)
    obj.delete()
    return redirect('venue-list')


@login_required
def venue_list(request):
    owner = request.user
    venues = Venue.objects.all().filter(owner_id__exact=owner.id)
    return render(request, 'event/venue/list.html', {'venues': venues})
