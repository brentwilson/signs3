from rest_framework import serializers
from .models import *


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFiles
        fields = '__all__'


class LogosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = '__all__'


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'


class SessionsSerializer(serializers.ModelSerializer):

    room_data = RoomsSerializer(source='room')

    class Meta:
        model = Sessions
        fields = ('session_code', 'agenda_session_id', 'session_id', 'name', 'description', 'start', 'end', 'sponsor', 'ad_hoc_session',
        'room_data')


class AdHocRoomsSerializer(serializers.ModelSerializer):
    room_data = RoomsSerializer(source='related_rooms')

    class Meta:
        model = Sessions
        fields = ('session_code', 'agenda_session_id', 'session_id',
        'name', 'description', 'start', 'end', 'room_data')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class ScheduledMediaSerializer(serializers.ModelSerializer):
    media_data = MediaSerializer(source='media')

    class Meta:
        model = ScheduledMedia
        fields = ('name', 'start', 'end', 'list_order', 'media_data')


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
