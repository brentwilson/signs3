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


@api_view(['GET'])
def current_combined(request, roomID):
    override_data = check_for_override(roomID)

    sessions_by_time = Sessions.objects.filter(
        Q(end__gte=override_data['currentDateTime']) & Q(start__lte=override_data['todaysEndDate'])).exclude(scheduleStatus='Cancel').order_by(
        'start')
    sessions_to_show = sessions_by_time.filter(room__related_rooms=roomID)
    messages = Messages.objects.filter(Q(start__lte=override_data['currentDateTime']) & Q(end__gte=override_data['currentDateTime']) & (
        Q(room=roomID) | Q(global_message=True)))

    sessions_serializer = SessionsSerializer(sessions_to_show, many=True)
    room_serializer = RoomsSerializer(override_data['room_settings'])
    messages_serializer = MessagesSerializer(messages, many=True)

    return Response({
        'room_data': room_serializer.data,
        'sessions': sessions_serializer.data,
        'messages': messages_serializer.data,
        'currentDateTime': override_data['currentDateTime'],
        'todaysEndDate': override_data['todaysEndDate']

    })


@api_view(['GET'])
def current_data(request, roomID):
    override_data = check_for_override(roomID)

    sessions_by_time = Sessions.objects.filter(
        Q(end__gte=override_data['currentDateTime']) & Q(
            start__lte=override_data['todaysEndDate'])
        & Q(room=roomID)).exclude(scheduleStatus='Cancel').order_by('start')
    messages = Messages.objects.filter(Q(start__lte=override_data['currentDateTime']) & Q(end__gte=override_data['currentDateTime']) & (
        Q(room=roomID) | Q(global_message=True)))

    sessions_serializer = SessionsSerializer(sessions_by_time, many=True)
    room_serializer = RoomsSerializer(override_data['room_settings'])
    messages_serializer = MessagesSerializer(messages, many=True)

    return Response({
        'room_data': room_serializer.data,
        'sessions': sessions_serializer.data,
        'messages': messages_serializer.data,
        'currentDateTime': override_data['currentDateTime'],
        'todaysEndDate': override_data['todaysEndDate']

    })


@api_view(['GET'])
def current_data_with_images(request, roomID):
    override_data = check_for_override(roomID)

    sessions_by_time = Sessions.objects.filter(
        Q(end__gte=override_data['currentDateTime']) & Q(start__lte=override_data['todaysEndDate']) & Q(
            room=roomID)).exclude(scheduleStatus='Cancel').order_by(
        'start')
    messages = Messages.objects.filter(
        Q(start__lte=override_data['currentDateTime']) & Q(end__gte=override_data['currentDateTime']) & (
            Q(room=roomID) | Q(global_message=True)))
    rotating_media = ScheduledMedia.objects.filter(Q(room=roomID) & (
        Q(start__lte=override_data['currentDateTime']) & Q(end__gte=override_data['currentDateTime']) | Q(
            start__isnull=True))).order_by('list_order')

    sessions_serializer = SessionsSerializer(sessions_by_time, many=True)
    room_serializer = RoomsSerializer(override_data['room_settings'])
    messages_serializer = MessagesSerializer(messages, many=True)
    rotating_media_serializer = ScheduledMediaSerializer(
        rotating_media, many=True)

    return Response({
        'room_data': room_serializer.data,
        'sessions': sessions_serializer.data,
        'messages': messages_serializer.data,
        'currentDateTime': override_data['currentDateTime'],
        'todaysEndDate': override_data['todaysEndDate'],
        'media': rotating_media_serializer.data

    })
