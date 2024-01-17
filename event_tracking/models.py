from django.db import models
from django.contrib.auth.models import User
from event.models import Event
# Create your models here.
class EventTracking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    accepted=models.BooleanField(default=False)