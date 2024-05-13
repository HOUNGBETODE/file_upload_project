# authentication/views.py

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib import messages
from django.template import Context
from django.conf import settings
from authentication import forms
from users.models import User
import pyotp


# function to send mail to user from our app
def send_email(request):
# defining :
    # - email subject
    subject = 'Login MFA Bulka'
    # - email sender
    from_email = settings.EMAIL_HOST_USER
    # - email receiver
    to_email = [request.session['email']] 
# generating the otp code based on random_base32() and setting the expiration time [interval=300 for 5 minutes]
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
# getting the code
    otp = totp.now()
# setting session variables to deal with user submission and validating it against the correct one
    # - session['otp_secret_key'] stores the otp code sent to user
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    # - session['otp_valid_date'] stores the the date untill the code will be valid for submission
    request.session['otp_valid_date'] = str(valid_date)
# loading the HTML template and passing it user mail and otp code
    html_template = get_template('authentication/email.html')
    html_content = html_template.render({'email': to_email[0], 'otp_code': otp})
# creating the email message, setting the content-type, and sending it
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()


# view to handle user login
def login_view(request):
    if 'user_log_in' not in request.session:
        form = forms.LoginForm()
        if request.method == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                try:
                    # checking whether provided username exists
                    user = User.objects.get(username=username)
                except:
                    messages.error(request, 'invalid username or password')
                else:
                    # checking whether the provided password is the correct one for the given username
                    if user.check_password(userpass):
                        # creating session variables and sending email to user, then redirecting it to code submission view
                        request.session['email'] = user.email
                        request.session['user_name'] = username
                        request.session['user_pass'] = userpass
                        send_email(request)
                        return redirect('otp-v')
                    else:
                        messages.error(request, 'invalid username or password')
            else:
                messages.error(request, 'login failed')
        return render(request, 'authentication/login.html', context={'form': form})


# view to handle otp template displaying, user code submission and asking back
def otp_view(request) :
    # when session['email'], session['otp_secret_key'] and session['otp_valid_date'] does not exist in session
    # and user is still trying to access the otp template view, redirect it to login page
    try :
        request.session['email']
        request.session['otp_secret_key']
        request.session['otp_valid_date']
    except KeyError as k:
        return redirect('login')
    else:
        if request.method == "POST":
            # retrieving user code...
            gatheredCode = ''
            for letter in 'orlane':
                gatheredCode+=request.POST.get(letter)
            # performing checkings...
            if datetime.now() <= datetime.fromisoformat(request.session['otp_valid_date']):
                # this check for code validity
                totp = pyotp.TOTP(request.session['otp_secret_key'], interval=300)
                # this check for code correctness
                if totp.verify(gatheredCode) :
                    # login and redirect user
                    user = authenticate(request, 
                                        username=request.session['user_name'], 
                                        password=request.session['user_pass']
                                        )
                    if user is not None:
                        # delete session variables
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        del request.session['user_name']
                        request.session['user_log_in'] = True
                        login(request, user)
                        return redirect('home')  
                else:
                    messages.error(request, "The provided digits do not match what we have sent to your inbox mail.")
            else:
                messages.error(request, 'Your OTP code has expired. Ask for another one.')
            # del request.POST
        return render(request, 'authentication/ask_for_otp.html', {})


# view to resend otp code to user
def otp_resend_view(request):
    try:
        send_email(request)
    except:
        messages.error(request, 'We encounter an error while sending you the email.')
    else:
        messages.success(request, 'Code has been sent to you successfully.')
    return redirect('otp-v')


# protected view to display home page
@login_required
def home_view(request):
    return render(request, 'authentication/home.html')
