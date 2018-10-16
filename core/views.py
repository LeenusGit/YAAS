from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


def home(request):
    return render(request, 'base.html', {})


def signup(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            rawPassword = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=rawPassword)

            login(request, user)
            return HttpResponseRedirect('home')

    else:
        form = UserCreationForm()

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
            return render(request, 'core/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'core/login.html', {'form': form})


def logoutView(request):
    logout(request)
    return render(request, 'core/logout.html', {})
