"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app import models
from app.models import Resource

resources=Resource.returnResources()

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
    """Renders the mapdata page."""
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
    return render(
        request,
        'app/delayVS.html',
        {
            'title':'Delay VS. X',
            'loss':resources['timeXloss'],
            'year':datetime.now().year,
        }
    )

def neighborhood_bar(request):
    """Renders the neighborhood_bar page."""
    return render(
        request,
        'app/neighborhood_bar.html',
        {
            'title':'Incidents per neighborhood',
            'neighborhood':resources['neighborhoodxfireincident'],
            'lossBar':resources['averageLossesNeighborhood'],
            'year':datetime.now().year,
        }
    )

def incidentsXlosses(request):
    """Renders the incidentsXlosses page."""
    return render(
        request,
        'app/incidentsXlosses.html',
        {
            'title':'Incidents X Losses',
            'incidentsXlosses':resources['incidentsXLosses'],
            'year':datetime.now().year,
        }
    )
def normal(request):
    """Renders the normal page."""
    return render(
        request,
        'app/normal.html',
        {
            'title':'Incidents X Losses',
            'normal':resources['normalLosses'],
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
            'neighborhood':resources['neighborhoodxfireincident'],
            'lossPie':resources['averageLossesNeighborhood'],
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
