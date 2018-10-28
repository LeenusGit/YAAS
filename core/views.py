import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation

from YAAS.settings import BASE_DIR, LOCALE_PATHS
from auctions import currencies
from .forms import UserRegistrationForm, UserUpdateForm
from .models import UserLangauge


def home(request):
    user = request.user

    print(request.session.items())
    print(LOCALE_PATHS)

    currency_list = currencies.get_currencies()
    try:
        current_currency = request.session['currency']
    except KeyError:
        current_currency = 'EUR'

    if request.method == 'POST':

        lang_code = request.POST['language']

        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

        if user.is_authenticated:

            try:
                user_language = UserLangauge.objects.get(user=user)
                user_language.language = lang_code
            except UserLangauge.DoesNotExist:
                user_language = UserLangauge.objects.create(user=user, language=lang_code)
                user_language.save()

        return HttpResponseRedirect('/')
        # return HttpResponseRedirect(request.POST['next'])

    return render(request, 'base.html', {'currency_list': currency_list, 'current_currency': current_currency})


def signup(request):

    # if request.method == 'GET':
    #     logout(request)

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

            try:
                user_language = UserLangauge.objects.get(user=user)
                lang_code = user_language.language
                request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
            except UserLangauge.DoesNotExist:
                # lang_code = request.session.get['language']
                pass

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


def currency(request):

    if request.method == 'POST':

        currency_code = request.POST['currency']

        request.session['currency'] = currency_code

    return HttpResponseRedirect(reverse('core:home'))


def emails(request):

    user = request.user

    if not user.is_superuser:
        return HttpResponseRedirect(reverse('core:login'))

    path = (BASE_DIR + '/emails/sent/')
    email_list = []

    for file in os.listdir(path):
        print(file)
        file_path = os.path.join(path, file)
        f = open(file_path, 'r')
        email_list.append(f.read())
        f.close()

    for email in email_list:
        print(email)
        print('')

    return render(request, 'core/emails.html', {'email_list': email_list})
