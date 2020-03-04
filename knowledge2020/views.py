from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from .serializers import *
from django.db.models import Q
import requests

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = SetDevice(request.POST)
        if form.is_valid():
            roomID = request.POST['roomID']
            mode = request.POST['mode']
            # room_settings = Rooms.objects.get(roomID=roomID)

            if mode == 'Today':
                redirect_view = '/knowledge2020/current/' + roomID

            elif mode == 'Combined Room':
                redirect_view = '/knowledge2020/combined/' + roomID

            elif mode == 'Blank':
                redirect_view = '/knowledge2020/blank/' + roomID

            elif mode == 'Logo Only':
                redirect_view = '/knowledge2020/logo_only/' + roomID

            elif mode == 'Rotating Media':
                redirect_view = '/knowledge2020/graphics/' + roomID

            elif mode == 'Custom Content':
                redirect_view = '/knowledge2020/content/' + roomID

            return redirect(redirect_view)

    else:
        form = SetDevice()

    context = {
        'form': form,
    }
    
    return render(request, "index.html", context)


def current(request, roomID):
    room_settings = Rooms.objects.get(roomID=roomID)
    body_class = room_settings.current_template
    context = {
        'roomID': roomID,
        'body_class': body_class
    }
    return render(request, "today.html", context)

def graphics(request, roomID):
    context = {
        'roomID': roomID,
        'body_class': 'slider_page'
    }
    return render(request, "graphics.html", context)


def combined(request, roomID):
    context = {
        'roomID': roomID,
        'body_class': 'combined'
    }
    return render(request, 'combined.html', context)


def custom_content(request, roomID):
    override_data = check_for_override(roomID)

    context = {
        'roomID': roomID,
        'body_class': 'custom_content',
        'custom_content': override_data['room_settings'].page_content
    }

    return render(request, "custom_content.html", context)


def default_screen(request, roomID):

    context = {
        'roomID': roomID,
        'body_class': 'custom_content'
    }

    return render(request, "default.html", context)


def check_for_override(roomID):
    room_settings = Rooms.objects.get(roomID=roomID)
    global_overrides = Event.objects.get(eventId=room_settings.event.eventId)

    if room_settings.override_date_time:
        override = True
        currentDateTime = room_settings.override_date_time
        todaysEndDate = datetime.combine(currentDateTime, time.max)

    elif global_overrides.override_date_time:
        override = True
        currentDateTime = global_overrides.override_date_time
        todaysEndDate = datetime.combine(currentDateTime, time.max)

    else:
        override = False
        currentDateTime = datetime.now()
        current_date = datetime.today()
        todaysEndDate = datetime.combine(current_date, time.max)

    override_data = {
        'room_settings': room_settings,
        'override': override,
        'currentDateTime': currentDateTime,
        'todaysEndDate': todaysEndDate

    }

    return override_data
