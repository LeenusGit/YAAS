from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.views import View
from .models import Auction, Bid
from .forms import AuctionForm, SearchForm


class AuctionIndexView(View):

    def get(self, request):

        form = SearchForm(request.GET)

        if form.is_valid():
            search_term = form.cleaned_data.get('search_term')
            auction_list = Auction.objects.filter(title__icontains=search_term)

            return render(request, 'auctions/index.html', {
                'auction_list': auction_list,
                'search_term': search_term,
                'form': form
            })

        else:
            form = SearchForm()
            auction_list = Auction.objects.all()
            return render(request, 'auctions/index.html', {'auction_list': auction_list, 'form': form})


def new_auction(request):

    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')
    form = AuctionForm()
    return render(request, 'auctions/create.html', {'form': form})


def edit_auction(request, pk):

    auction = get_object_or_404(Auction, pk=pk)
    user = request.user

    if user.username != auction.author:
        return HttpResponseNotAllowed('not_allowed')

    if request.method == 'POST':
        description = request.POST['description']
        auction.description = description
        auction.save()

        return HttpResponseRedirect(reverse('auctions:detail', args=(auction.id,)))

    old_description = auction.description

    return render(request, 'auctions/edit_auction.html', {'auction': auction, 'old_description': old_description})


class AuctionDetailView(View):

    def get(self, request, pk):

        auction = get_object_or_404(Auction, pk=pk)
        user = request.user

        if user.username == auction.author:
            is_permitted_to_edit = True
        else:
            is_permitted_to_edit = False

        return render(request, 'auctions/detail.html', {'auction': auction, 'is_permitted_to_edit': is_permitted_to_edit})


class ConfirmAuctionView(View):

    def get(self, request):

        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('/login/')

        form = AuctionForm(request.GET)
        if form.is_valid():

            # TODO: Rewrite with validate_auction

            title = (form.cleaned_data.get('title'))
            description = (form.cleaned_data.get('description'))
            min_price = (form.cleaned_data.get('min_price'))
            close_date = (form.cleaned_data.get('close_date'))
            close_time = (form.cleaned_data.get('close_time'))

            deadline = datetime.combine(close_date, close_time)

            if deadline < datetime.now() + timedelta(hours=72):
                # POSTED auction duration was too short
                error_message = 'Auction duration has to be longer than 72 hours.'
                return render(request, 'auctions/create_error.html', {'form': form, 'error': error_message})

            aware_deadline = timezone.make_aware(deadline)

            auction = Auction(
                author=user,
                title=title,
                description=description,
                min_price=min_price,
                deadline=aware_deadline,
            )
            return render(request, 'auctions/confirm.html', {'auction': auction, 'form': form})

        return render(request, 'auctions/create.html', {'form': form})

    def post(self, request):

        user = request.user
        # TODO: Confirm user is authorized to POST auction

        # email = user.email
        data = request.POST
        auction = Auction(
            author=user,
            title=data['title'],
            description=data['description'],
            min_price=data['min_price'],
            deadline=data['deadline'],
        )

        error = validate_auction(auction)

        if error is not None:
            return HttpResponseBadRequest('bad_request')
        else:
            # POST was successful
            # TODO: Send confirmation email
            # send_mail('Test', 'Test Message', 'from@test.com', 'to@test.com')
            auction.save()
            return HttpResponseRedirect('success')


def validate_auction(auction):

    deadline = (parse_datetime(auction.deadline))
    now = timezone.make_aware(datetime.now())
    three_days_from_now = timezone.make_aware(datetime.now() + timedelta(hours=72))

    if deadline < three_days_from_now:
        # auction duration was too short
        error_message = 'Auction duration has to be longer than 72 hours.'
        return error_message

    if deadline < now:
        # auction close date was in the past
        error_message = 'Auction close time is in the past'
        return error_message

    return None


def successful_auction_post(request):
    return render(request, 'auctions/success.html', {})


def bad_request(request):
    return render(request, 'auctions/bad_request.html', {})
