from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from .forms import UserRegistrationForm


def home(request):
    return render(request, 'base.html', {})


def signup(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            formObj = form.cleaned_data
            username = formObj['username']
            email = formObj['email']
            rawPassword = formObj['password']

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email)):

                User.objects.create_user(username=username, email=email, password=rawPassword)
                user = authenticate(username=username, password=rawPassword)
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                errorMessage = 'User or email already exists.'
                return render(request, 'core/register_error.html', {'form': form, 'error': errorMessage})

    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def loginView(request):

    logout(request)

    if request.method == 'POST':

        form = AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            errorMessage = 'Wrong username or password.'
            return render(request, 'core/login_error.html', {'form': form, 'error': errorMessage})

    else:
        form = AuthenticationForm()
        return render(request, 'core/login.html', {'form': form})


def logoutView(request):
    logout(request)
    return render(request, 'core/logout.html', {})
