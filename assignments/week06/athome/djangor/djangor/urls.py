from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from djangor_app.views import EntryListView
from djangor_app.views import EntryCreate
from registration.views import register

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', EntryListView.as_view(), name='entry_list'),
    url(r'^add/', EntryCreate.as_view(), name='entry_create'),
    # Superseded by specific entries for register and default auth_urls (see below).
    # url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.simple.SimpleBackend', 'success_url':'/'},
                           name='registration_register'),
    # For login logout. See /Users/matt/Projects/scipy/lib/python2.7/site-packages/registration/backends/simple/urls.py
    url(r'', include('registration.auth_urls')),
    )
