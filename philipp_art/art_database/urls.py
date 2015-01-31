from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'art_database.views.home', name='home'),
                       url(r'^locations/(?P<id>\w+)/edit', 'art_database.views.edit_location', name='edit_location'),
                       url(r'^accounts/login/', 'art_database.views.login', name='login'),
)
