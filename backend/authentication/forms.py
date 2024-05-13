# authentication/forms.py

from captcha.fields import CaptchaField 
from django import forms

# defining a custom form to handle login request
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63) # the username field defined
    password = forms.CharField(max_length=63, widget=forms.PasswordInput) # the password field defined
    captcha = CaptchaField() # the captcha field defined