from django.shortcuts import render,redirect
from .import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from event.models import Event
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from event_tracking.models import EventTracking
# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form=forms.RegistrationForm(request.POST)
        if register_form.is_valid():
                user = register_form.save()

                # Generate confirmation link
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                confirm_link=f"http://127.0.0.1:8000/user/active/{uid}/{token}"
                email_subject="Confirm Your Email"
                email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
                email=EmailMultiAlternatives(email_subject,'',to=[user.email])
                email.attach_alternative(email_body,'text/html')
                email.send()
                messages.success(request,'A mail sent to your account')
                return redirect('signup')
    else:
        register_form=forms.RegistrationForm()
    return render(request,'signup.html',{'form':register_form,'type':'Signup'})


def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('signup')
    else:
        return redirect('signup')
    
    

class UserLoginView(LoginView):
    template_name='signup.html'
    def get_success_url(self) -> str:
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request,'Logged in successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request,'Information incorrect')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['type'] = 'login'
        return context
    
def profile(request):
    data= EventTracking.objects.filter(user=request.user, accepted=True)
    return render(request, 'profile.html', {'data': data})

@login_required   
def organize_event(request):
    data=Event.objects.filter(organizer=request.user)
    return render(request,'organize_events.html',{'data':data})
    
@login_required
def user_logout(request):
    logout(request)
    return redirect('homepage')

@login_required   
def edit_profile(request):
    if request.method == 'POST':
        profile_form=forms.ChangeUserForm(request.POST,instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            email_subject="Update Profile"
            email_body=render_to_string('update_email.html')
            email=EmailMultiAlternatives(email_subject,'',to=[request.user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            messages.success(request,'Account Updated Successfully')
            return redirect('profile')
    else:
        profile_form=forms.ChangeUserForm(instance=request.user)
    return render(request,'update_profile.html',{'form':profile_form})