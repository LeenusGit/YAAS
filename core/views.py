from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserRegistrationForm, UserUpdateForm


def home(request):
    return render(request, 'base.html', {})


def signup(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form_obj = form.cleaned_data
            username = form_obj['username']
            email = form_obj['email']
            raw_password = form_obj['password']

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email)):

                User.objects.create_user(username=username, email=email, password=raw_password)
                user = authenticate(username=username, password=raw_password)
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                error_message = 'User or email already exists.'
                return render(request, 'core/register_error.html', {'form': form, 'error': error_message})

    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):

    # If user is logging in while already logged in as a different user
    logout(request)

    if request.method == 'POST':

        print(request.POST)

        form = AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            error_message = 'Wrong username or password.'
            return render(request, 'core/login_error.html', {'form': form, 'error': error_message})

    else:
        form = AuthenticationForm()
        return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'core/logout.html', {})


def profile(request):

    user = request.user

    if request.method == 'POST':

        for field in request.POST:
            if field == 'email':

                if User.objects.filter(email=request.POST['email']):
                    # Email already exists
                    pass
                else:
                    user.email = request.POST['email']

            if field == 'password':
                user.set_password(request.POST['password'])

        user.save()
        return HttpResponseRedirect('/')

    form = UserUpdateForm({'email': user.email})
    return render(request, 'core/profile.html', {'user': user, 'form': form})
