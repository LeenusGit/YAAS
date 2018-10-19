from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.views import generic, View
from .models import Auction, Bid
from .forms import AuctionForm


class AuctionIndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'auctionList'

    def get_queryset(self):
        return Auction.objects.all()


def newAuction(request):

    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')
    form = AuctionForm()
    return render(request, 'auctions/create.html', {'form': form})


def editAuction(request, pk):

    auction = get_object_or_404(Auction, pk=pk)
    user = request.user

    if user.username != auction.author:
        return HttpResponseNotAllowed('not_allowed')

    if request.method == 'POST':
        description = request.POST['description']
        auction.description = description
        auction.save()

        return HttpResponseRedirect(reverse('auctions:detail', args=(auction.id,)))

    oldDescription = auction.description

    return render(request, 'auctions/edit_auction.html', {'auction': auction, 'oldDescription': oldDescription})


class AuctionDetailView(View):

    def get(self, request, pk):

        auction = get_object_or_404(Auction, pk=pk)
        user = request.user

        if user.username == auction.author:
            isPermittedtoEdit = True
        else:
            isPermittedtoEdit = False

        return render(request, 'auctions/detail.html', {'auction': auction, 'isPermittedToEdit': isPermittedtoEdit})


class ConfirmAuctionView(View):

    def get(self, request):

        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect('/login/')

        form = AuctionForm(request.GET)
        if form.is_valid():

            # TODO: Rewrite with validateAuction

            title = (form.cleaned_data.get('title'))
            description = (form.cleaned_data.get('description'))
            minPrice = (form.cleaned_data.get('minPrice'))
            closeDate = (form.cleaned_data.get('closeDate'))
            closeTime = (form.cleaned_data.get('closeTime'))

            deadline = datetime.combine(closeDate, closeTime)

            if deadline < datetime.now() + timedelta(hours=72):
                # POSTED auction duration was too short
                errorMessage = 'Auction duration has to be longer than 72 hours.'
                return render(request, 'auctions/create_error.html', {'form': form, 'error': errorMessage})

            awareDeadline = timezone.make_aware(deadline)

            auction = Auction(
                author=user,
                title=title,
                description=description,
                minPrice=minPrice,
                deadline=awareDeadline,
            )
            return render(request, 'auctions/confirm.html', {'auction': auction, 'form': form})

        return render(request, 'auctions/create.html', {'form': form})

    def post(self, request):

        user = request.user
        # TODO: Confirm user is authorized to POST auction

        email = user.email
        data = request.POST
        auction = Auction(
            author=user,
            title=data['title'],
            description=data['description'],
            minPrice=data['minPrice'],
            deadline=data['deadline'],
        )

        error = validateAuction(auction)

        if error is not None:
            print(error)
            print('auction did not pass validation')
            return HttpResponseBadRequest('bad_request')
        else:
            #POST was successful
            # TODO: Send confirmation email
            # send_mail('Test', 'Test Message', 'from@test.com', 'to@test.com')
            auction.save()
            return HttpResponseRedirect('success')


def validateAuction(auction):

    deadline = (parse_datetime(auction.deadline))
    now = timezone.make_aware(datetime.now())
    threeDaysFromNow = timezone.make_aware(datetime.now() + timedelta(hours=72))

    if deadline < threeDaysFromNow:
        # auction duration was too short
        errorMessage = 'Auction duration has to be longer than 72 hours.'
        return errorMessage

    if deadline < now:
        # auction close date was in the past
        errorMessage = 'Auction close time is in the past'
        return errorMessage

    return None


def successfulAuctionPost(request):
    return render(request, 'auctions/success.html', {})


def badRequest(request):
    return render(request, 'auctions/bad_request.html', {})
