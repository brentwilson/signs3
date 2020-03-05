from django import forms
from .models import Rooms, Event


class SetDevice(forms.Form):
    MODE_CHOICES = (
        ('','----------------'),
        ('Today', 'Today'),
        ('Rotating Media', 'Rotating Media'),
        ('cs_plan', 'Customer Success Plan'),
        ('cs_deploy', 'Customer Success Deploy'),
        ('cs_extend', 'Customer Success Extend'),
        ('cs_optimize', 'Customer Success Optimize'),
        ('Combined Room', 'Hallway Room'),
        ('Custom Content', 'Custom Content')
    )
    mode = forms.ChoiceField(choices=MODE_CHOICES, label="Choose Mode")
    roomID = forms.ModelChoiceField(queryset=Rooms.objects.all().order_by('name'), label="Choose Room")