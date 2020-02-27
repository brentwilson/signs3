from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe


class MediaFiles(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('',  'Select Media Type'),
        ('img', 'IMAGE'),
        ('video', 'VIDEO')
    )
    name = models.CharField(max_length=255)
    media_file = models.FileField()
    media_type = models.CharField(max_length=15, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return self.name

    def media_thumb(self):
        if self.media_type == 'img':
            return mark_safe('<img src="%s" style="max-height:125px;"/>' % self.media_file.url)

    media_thumb.short_description = 'Image Thumbnail'

    class Meta:
        verbose_name_plural = "media files"
        verbose_name = "media file"


class Logos(models.Model):
    sponsorName = models.CharField(max_length=255, null=True)
    logo = models.ForeignKey(MediaFiles, null=True,
        blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "logos"
        verbose_name = "logo"

    def __str__(self):
        return self.sponsorName

    def image_tag(self):
        return mark_safe('<img src="%s" style="max-height:80px;"/>' % self.logo.media_file.url)

    image_tag.short_description = 'Image'


class Event(models.Model):
    eventId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    refreshKey = models.CharField(max_length=255, default="1")
    override_date_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "events"
        verbose_name = "event"

    def __str__(self):
        return self.name


class Rooms(models.Model):
    TEMPLATE_CHOICES = (
        ('today_standard', 'Default'),
        ('creatorcon', 'Creator Con'),
        ('noheader', 'Hide Header')
    )
    roomID = models.IntegerField(primary_key=True)
    event = models.ForeignKey(
        Event, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location_name = models.TextField(blank=True, null=True)
    logo = models.ForeignKey(Logos, null=True, blank=True, on_delete=models.CASCADE)
    override_date_time = models.DateTimeField(null=True, blank=True)
    page_content = RichTextField(null=True, blank=True)
    rotating_media_interval = models.PositiveSmallIntegerField(
        null=True, blank=True, default=15, validators=[MaxValueValidator(400), MinValueValidator(7)])
    related_rooms = models.ManyToManyField("self", blank=True)
    current_template = models.CharField(
        max_length=255, choices=TEMPLATE_CHOICES, default='today_standard')

    class Meta:
        verbose_name_plural = "rooms"
        verbose_name = "room"

    def __str__(self):
        return self.name

    def room_logo(self):
        if self.logo:
            return self.logo.image_tag()

    room_logo.short_description = 'Logo'


class ScheduledMedia(models.Model):
    name = models.CharField(max_length=255)
    media = models.ForeignKey(MediaFiles, on_delete=models.CASCADE)
    room = models.ManyToManyField(Rooms)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    list_order = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def ad_thumb(self):
        if self.media.media_type == 'img':
            return mark_safe('<img src="%s" style="max-height:80px;"/>' % self.media.media_file.url)

    ad_thumb.short_description = 'Image Thumbnail'

    class Meta:
        verbose_name_plural = "Scheduled Media"
        verbose_name = "Scheduled Media"


class Sessions(models.Model):
    agenda_session_id = models.CharField(max_length=16, primary_key=True)
    session_id = models.CharField(max_length=32)
    session_code = models.CharField(max_length=32, null=True, blank=True)
    scheduleStatus = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sponsor = models.ForeignKey(Logos, blank=True, null=True, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    ad_hoc_session = models.NullBooleanField(blank=True, null=True)
    room = models.ForeignKey(Rooms, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sessions"
        verbose_name = "Session"

    def __str__(self):
        return self.session_code + " | " + self.name


class Speakers(models.Model):
    speaker_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    sessions = models.ManyToManyField(Sessions)

    class Meta:
        verbose_name_plural = "Speakers"
        verbose_name = "Speaker"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Messages(models.Model):
    room = models.ForeignKey(Rooms, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    global_message = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Messages"
        verbose_name = "Message"

    def __str__(self):
        return self.message
