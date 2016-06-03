"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app import models
from app.models import Incident

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home',
            'year':datetime.now().year,
        }
    )

def mapdata(request):
    """Renders the data page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/mapdata.html',
        {
            'title':'Map & Data',
            'year':datetime.now().year,
        }
    )

def delayVS(request):
    """Renders the delayVS page."""
    assert isinstance(request, HttpRequest)
    x=models.Incident.returnIncidents()

    return render(
        request,
        'app/delayVS.html',
        {
            'title':'Delay VS. X',
            'loss':x['loss'],
            'victims':x['victims'],
            'neighborhood':x['neighborhood'],
            'year':datetime.now().year,
        }
    )

def neighborhood_bar(request):
    """Renders the neighborhood page."""
    return render(
        request,
        'app/neighborhood_bar.html',
        {
            'title':'Incidents per neighborhood',
            'neighborhood':models.neighborhoodxfireincident(),
            'year':datetime.now().year,
        }
    )
def neighborhood_pie(request):
    """Renders the neighborhood page."""
    return render(
        request,
        'app/neighborhood_pie.html',
        {
            'title':'Incidents per neighborhood',
            'neighborhood':models.neighborhoodxfireincident(),
            'year':datetime.now().year,
        }
    )
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Application description page.',
            'year':datetime.now().year,
        }
    )
