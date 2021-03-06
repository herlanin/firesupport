"""
Definition of urls for Fire_Incidents_Support_System.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views

import app.forms
import app.views
from django.contrib import admin

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^mapdata', app.views.mapdata, name='mapdata'),
    url(r'^delayVS', app.views.delayVS, name='delayVS'),
    url(r'^neighborhood_bar', app.views.neighborhood_bar, name='neighborhood_bar'),
    url(r'^neighborhood_pie', app.views.neighborhood_pie, name='neighborhood_pie'),
    url(r'^incidentsXlosses', app.views.incidentsXlosses, name='incidentsXlosses'),
    url(r'^normal', app.views.normal, name='normal'),
    url(r'^contact$', app.views.contact, name='contact'),
    #url(r'^about', app.views.about, name='about'),
  ##  url(r'^login/$',
  #  #    django.contrib.auth.views.login,
  #      {
  #          'template_name': 'app/login.html',
  #          'authentication_form': app.forms.BootstrapAuthenticationForm,
  #          'extra_context':
  #          {
  #              'title': 'Log in',
  #              'year': datetime.now().year,
  #          }
  #      },
  #      name='login'),
   # url(r'^logout$',
      #  django.contrib.auth.views.logout,
     #   {
      #      'next_page': '/',
      #  },
     #   name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
]
