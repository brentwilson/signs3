from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import HttpResponse
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
                redirect_view = '/knowledge2020/today/' + roomID

            elif mode == 'Combined Room':
                redirect_view = '/knowledge2020/hallway_room/' + roomID

            elif mode == 'cs_plan':
                redirect_view = '/knowledge2020/cs_plan/' + roomID

            elif mode == 'cs_deploy':
                redirect_view = '/knowledge2020/cs_deploy/' + roomID

            elif mode == 'cs_optimize':
                redirect_view = '/knowledge2020/cs_optimize/' + roomID

            elif mode == 'cs_extend':
                redirect_view = '/knowledge2020/cs_extend/' + roomID

            elif mode == 'Blank':
                redirect_view = '/knowledge2020/blank/' + roomID

            elif mode == 'Logo Only':
                redirect_view = '/knowledge2020/logo_only/' + roomID

            elif mode == 'Rotating Media':
                redirect_view = '/knowledge2020/today_slider/' + roomID

            elif mode == 'Custom Content':
                redirect_view = '/knowledge2020/content/' + roomID

            elif mode == 'Simple Logo':
                redirect_view = '/knowledge2020/simple_logo/' + roomID

            return redirect(redirect_view)

    else:
        form = SetDevice()

    context = {
        'form': form,

    }
    return render(request, "index.html", context)
