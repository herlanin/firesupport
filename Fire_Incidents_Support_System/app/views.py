"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

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

def analysisPlotting(request):
    """Renders the analysisplotting page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/analysisplotting.html',
        {
            'title':'Analysis and Plotting',
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
