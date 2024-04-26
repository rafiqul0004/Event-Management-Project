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
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form=forms.RegistrationForm(request.POST)
        if register_form.is_valid():
                user = register_form.save()

                # Generate confirmation link
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                confirm_link=f"https://vibevento.onrender.com/user/active/{uid}/{token}"
                email_subject="Confirm Your Email"
                email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
                email=EmailMultiAlternatives(email_subject,'',to=[user.email])
                email.attach_alternative(email_body,'text/html')
                email.send()
                messages.success(request,'A verification mail sent to your email')
                return redirect('login')
    else:
        register_form=forms.RegistrationForm()
    return render(request,'signup.html',{'form':register_form,'type':'signup'})


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
    # Fetch user details
    user_details = User.objects.get(pk=request.user.pk)
    
    # Fetch event tracking data
    event_tracking_data = EventTracking.objects.filter(user=request.user, accepted=True)
    
    return render(request, 'profile.html', {'user_details': user_details, 'data': event_tracking_data})

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


# --------------------------------Contact Form --------------------------------
@require_POST
def contact_us(request):
    # Get form data
    name = request.POST.get('name')
    email = request.POST.get('emailAddress')
    message = request.POST.get('message')

    # You can add validation here if needed

    # Send email
    subject = f"Message from {name}"
    message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    sender_email = email  # Using the email provided in the contact form as the sender's email address
    recipient_email = ['kr.rafiqul@gmail.com']  # Recipient's email address

    try:
        send_mail(subject, message_body, sender_email, recipient_email)
        # Email sent successfully
        return JsonResponse({'success': True})
    except Exception as e:
        # Error sending email
        return JsonResponse({'success': False, 'error_message': str(e)})