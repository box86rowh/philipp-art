from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'art_database.views.home', name='home'),
                       url(r'^accounts/login/', 'art_database.views.login', name='login'),
)
