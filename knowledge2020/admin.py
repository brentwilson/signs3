from django.contrib import admin
from .models import *

# Register your models here.


class MediaAdmin(admin.ModelAdmin):
    list_display = 'name', 'media_thumb', 'media_type'
    list_filter = ('media_type',)
    search_fields = 'name',


class SponsorsAdmin(admin.ModelAdmin):
    list_display = 'sponsorName', 'image_tag'


class SpeakersAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'last_name'


class SpeakersInline(admin.TabularInline):
    model = Speakers.sessions.through


class SessionsAdmin(admin.ModelAdmin):
    list_display = ('agenda_session_id', 'session_id',
                    'session_code', 'name', 'start', 'end')
    list_filter = ('room',)
    search_fields = ('name', 'agenda_session_id', 'session_id', 'session_code')

    inlines = [
        SpeakersInline,
    ]


class SessionsinRoomInline(admin.TabularInline):
    model = Sessions
    list_display = ('agenda_session_id', 'session_id',
                    'session_code', 'name', 'start', 'end')
    search_fields = ('name', 'agenda_session_id', 'session_id', 'session_code')


class ScheduledMediaAdmin(admin.ModelAdmin):
    list_display = 'name', 'ad_thumb', 'start', 'end', 'list_order'
    readonly_fields = ('ad_thumb',)
    list_filter = ('room',)
    search_fields = ('name', 'room')


class ScheduledMediaInline(admin.TabularInline):
    model = ScheduledMedia.room.through
    verbose_name = 'Scheduled Media'
    list_display = 'name', 'list_order', 'start', 'end'


class RoomsAdmin(admin.ModelAdmin):
    list_display = 'roomID', 'event', 'name', 'override_date_time', 'room_logo'
    search_fields = ('name', 'roomID')

    inlines = [
        SessionsinRoomInline,
        ScheduledMediaInline
    ]


class EventsAdmin(admin.ModelAdmin):
    list_display = 'name', 'override_date_time', 'active'


admin.site.register(Sessions, SessionsAdmin)
admin.site.register(Event, EventsAdmin)
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Messages)
admin.site.register(Speakers, SpeakersAdmin)
admin.site.register(ScheduledMedia, ScheduledMediaAdmin)
admin.site.register(MediaFiles, MediaAdmin)
admin.site.register(Logos, SponsorsAdmin)
