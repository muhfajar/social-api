"""social_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from modules.event.views import core, venue

urlpatterns = [
    url(r'^$', core.home, name='home'),

    url(r'^venue/$', venue.venue, name='venue'),
    url(r'^venue/(?P<venue_id>[0-9]+)/$', venue.venue_update, name='venue-update'),
    url(r'^venue/(?P<venue_id>[0-9]+)/delete/$', venue.venue_delete, name='venue-delete'),
    url(r'^venue/list/$', venue.venue_list, name='venue-list'),

    url(r'^category/(?P<event_type>\w+)/$', core.category, name='type'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core.signup, name='signup'),
    url(r'^settings/$', core.settings, name='settings'),
    url(r'^settings/password/$', core.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
]

# Change admin site title
admin.site.site_header = _("Event Management")
admin.site.site_title = _("Admin Panel")
