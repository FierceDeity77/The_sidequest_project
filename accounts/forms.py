from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(UserCreationForm): # inherited from django usercreation form you can also build a form from scratch
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"] # pw1 and pw2 django will check if they match

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['password1'].help_text = "Must be at least 8 characters"
        self.fields['username'].label = "Username"
        # self.fields['avatar'].label = "Avatar"
        