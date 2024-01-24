from django.shortcuts import render
from event.models import Event
from category.models import Category

def home(request,category_slug=None):
    data=Event.objects.all()
    if category_slug is not None:
        category=Category.objects.get(slug=category_slug)
        data=Event.objects.filter(category=category)
    categories=Category.objects.all()
    return render(request,'home.html',{'data':data, 'categories':categories})

def about_us(request):
    return render(request,'about_us.html')