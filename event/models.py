from django.db import models
from django.contrib.auth.models import User
from category.models import Category
# Create your models here.
class Event(models.Model):
    organizer = models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='event/media/upload',null=True,blank=True)
    date=models.DateField()
    time=models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    is_public = models.BooleanField(default=True)
    attendee_count=models.IntegerField(default=0)
    category=models.ManyToManyField(Category)
    tags=models.CharField(max_length=250)

    def __str__(self) -> str:
        return f'Event : {self.name} {self.organizer.username}'