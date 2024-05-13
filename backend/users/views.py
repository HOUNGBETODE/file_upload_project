from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import SingupForm
from users.models import User

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
from django.http import QueryDict, HttpResponse
from .models import User
import json

def signup_view(request):
    form = SingupForm()
    if request.method == "POST":
        # print(dir(request))
        # requestBody = json.loads(request.body.decode())
        # POST = QueryDict('', mutable=True)
        # POST.update(requestBody)
        # print(requestBody)
        # print(POST)
        form = SingupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f"User {form.cleaned_data['username']} has been created successfully.")
                return redirect('login')
            except:
                messages.error(request, "User creation failed.")
            form = SingupForm()
    return render(request, 'signup.html', {'form': form})


def looking_for_username(request):
    if request.method == 'GET' :
        banned = ['admin', 'adminuser', 'administrator', 'sudo', 'superuser', 'root']
        query = request.GET.get('query').lower()
        if(query):
            if any(query.startswith(notA) for notA in banned) or User.objects.filter(username__iexact=query) :
                return HttpResponse('taken', status=200)
            else :
                return HttpResponse('available', status=200)
        return HttpResponse(status=500)
    else:
        return HttpResponse(status=403)


def query_register_username(request):
    if request.method == 'GET' :
        getParams = request.GET
        username = getParams.get('username')
        password = getParams.get('password')
        email = getParams.get('email')
        genre = getParams.get('genre')
        if all([username, password, email, genre]):
            genre = genre[:3]
            user = User.objects.create(username=username, genre=genre, email=email)
            user.set_password(password)
            user.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=403)
