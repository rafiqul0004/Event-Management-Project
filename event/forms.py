from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Event
        exclude = ['organizer', 'attendee_count']
