from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .import forms
from .import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from event_tracking.models import EventTracking
from .models import Event
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
@method_decorator(login_required,name='dispatch')
class AddEventView(CreateView):
     model=models.Event
     form_class=forms.EventForm
     template_name='add_event.html'
     success_url=reverse_lazy('add_events')
     def form_valid(self, form):
          form.instance.organizer=self.request.user
          return super().form_valid(form)
     
@method_decorator(login_required,name='dispatch')
class EditEventView(UpdateView):
      model=models.Event
      form_class=forms.EventForm
      template_name='add_event.html'
      pk_url_kwarg = 'id'
      success_url=reverse_lazy('profile')

@method_decorator(login_required,name='dispatch')
class DeleteEventView(DeleteView):
     model=models.Event
     template_name='delete.html'
     pk_url_kwarg = 'id'
     success_url=reverse_lazy('profile')

class DetailEventView(DetailView):
    model = models.Event
    template_name = 'detail.html'
    pk_url_kwarg = 'id'


def accept_event(request, id):
    event = get_object_or_404(Event, pk=id)
    if event.organizer == request.user:
        return HttpResponse("You cannot accept your own event.")
    
    if EventTracking.objects.filter(user=request.user, event=event).exists():
        pass
    else:
        event.attendee_count += 1
        event.save()
        event_tracking = EventTracking(user=request.user, event=event, accepted=True)
        event_tracking.save()
        return redirect('profile')

    return render(request, 'deetail_event')

def attendee_list(request, id):
    event = get_object_or_404(Event, pk=id)
    attendees = EventTracking.objects.filter(event=event, accepted=True)
    return render(request, 'attendee_list.html', {'event': event, 'attendees': attendees})
