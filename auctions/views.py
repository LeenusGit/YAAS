from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views import View

from auctions import currencies
from auctions.resolver import ResolveThread
from core.emails import send_confirm_email, send_ban_email
from .models import Auction
from .forms import AuctionForm, SearchForm

from auctions.currencies import UpdateCurrenciesThread

update_currency_thread = UpdateCurrenciesThread()
update_currency_thread.start()

resolve_thread = ResolveThread()
resolve_thread.start()


class AuctionIndexView(View):

    def get(self, request):

        form = SearchForm(request.GET)
        user = request.user

        if form.is_valid():
            search = form.cleaned_data.get('search')
            auction_list = Auction.objects.filter(title__icontains=search, state='Active')

            return render(request, 'auctions/index.html', {
                'auction_list': auction_list,
                'search_term': search,
                'form': form,
                'is_user_admin': user.is_superuser,
            })

        else:
            form = SearchForm()
            auction_list = Auction.objects.filter(state='Active')
            return render(request, 'auctions/index.html', {'auction_list': auction_list, 'form': form})


def new_auction(request):

    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('core:login'))
    form = AuctionForm()
    return render(request, 'auctions/create.html', {'form': form})


def ban_auction(request, pk):

    # Only allow superusers
    if not request.user.is_superuser:
        return HttpResponse(status=401)

    auction = get_object_or_404(Auction, pk=pk)

    if request.method == 'POST':
        auction.state = 'Banned'
        auction.save()

        creator = User.objects.get(username=auction.author)
        send_ban_email(creator, auction)

    return HttpResponseRedirect('/auctions/')


def edit_auction(request, pk):

    auction = get_object_or_404(Auction, pk=pk)
    user = request.user

    if user.username != auction.author:
        return HttpResponse(status=401, reason='Not the author of the auction')

    if request.method == 'POST':

        description = request.POST['description']
        Auction.new_description(auction.id, description)

        return HttpResponseRedirect(reverse('auctions:detail', args=(auction.id,)))

    old_description = auction.description
    return render(request, 'auctions/edit_auction.html', {'auction': auction, 'old_description': old_description})


class AuctionDetailView(View):

    def get(self, request, pk):

        auction = get_object_or_404(Auction, pk=pk)
        user = request.user

        try:
            currency_code = request.session['currency']
        except KeyError:
            currency_code = 'EUR'

        converted_price = currencies.convert('EUR', float(auction.min_price), currency_code)

        if user.is_superuser:
            is_user_admin = True
        else:
            is_user_admin = False

        if user.username == auction.author:
            is_permitted_to_edit = True
        else:
            is_permitted_to_edit = False

        context = {
            'auction': auction,
            'converted_price': converted_price,
            'is_permitted_to_edit': is_permitted_to_edit,
            'admin': is_user_admin,
            'currency_code': currency_code,
        }

        return render(request, 'auctions/detail.html', context)


class ConfirmAuctionView(View):

    def get(self, request):

        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse('core:login'))

        form = AuctionForm(request.GET)
        if form.is_valid():

            title = (form.cleaned_data.get('title'))
            description = (form.cleaned_data.get('description'))
            min_price = (form.cleaned_data.get('min_price'))
            close_date = (form.cleaned_data.get('close_date'))
            close_time = (form.cleaned_data.get('close_time'))

            deadline = datetime.combine(close_date, close_time)
            aware_deadline = timezone.make_aware(deadline)

            auction = Auction(
                author=user,
                title=title,
                description=description,
                min_price=min_price,
                deadline=aware_deadline,
            )

            error_message = validate_auction(auction)
            if error_message is not None:
                print(error_message)
                return render(request, 'auctions/create_error.html', {'form': form, 'error': error_message})

            # if deadline < datetime.now() + timedelta(hours=72):
            #     # POSTED auction duration was too short
            #     error_message = 'Auction duration has to be longer than 72 hours.'

            return render(request, 'auctions/confirm.html', {'auction': auction, 'form': form})

        return render(request, 'auctions/create.html', {'form': form})

    def post(self, request):

        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('/login/')

        data = request.POST
        deadline = parse_datetime((data['deadline']))
        auction = Auction(
            author=user,
            title=data['title'],
            description=data['description'],
            min_price=data['min_price'],
            deadline=deadline,
        )
        error = validate_auction(auction)
        if error is not None:
            return HttpResponseBadRequest(reverse('auctions:bad_request'), reason=error)
        else:
            # POST was successful
            send_confirm_email(user, auction)
            auction.save()
            return HttpResponseRedirect(reverse('auctions:success'))


def validate_auction(auction):

    deadline = auction.deadline
    now = timezone.make_aware(datetime.now())
    three_days_from_now = timezone.make_aware(datetime.now() + timedelta(hours=72))

    if deadline <= now:
        # auction close date was in the past
        error_message = 'Auction close time is in the past'
        return error_message

    if deadline < three_days_from_now:
        # auction duration was too short
        error_message = 'Auction duration has to be longer than 72 hours.'
        return error_message

    return None


def successful_auction_post(request):
    return render(request, 'auctions/success.html', {})


def bad_request(request):
    return render(request, 'auctions/bad_request.html', {})


def banned_auctions(request):

    form = SearchForm(request.GET)
    auction_list = []

    if form.is_valid():
        print('is valid')
        search = form.cleaned_data.get('search')
        auction_list = Auction.objects.filter(title__icontains=search, state='Active')
        # auction_list = Auction.objects.filter(state='Banned')

        return render(request, 'auctions/index.html', {
            'auction_list': auction_list,
            'search_term': search,
            'form': form
        })

    else:
        form = SearchForm()
        auction_list = Auction.objects.filter(state='Active')
        return render(request, 'auctions/index.html', {'auction_list': auction_list, 'form': form})
