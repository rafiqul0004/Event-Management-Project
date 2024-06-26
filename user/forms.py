from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import PasswordResetForm
# from .models import Author

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model=Author
#         fields="__all__"

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    class Meta:
        model=User
        fields=['username','first_name', 'last_name', 'email']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  
        if commit:
            user.save()
        return user

class ChangeUserForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name', 'last_name', 'email']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))