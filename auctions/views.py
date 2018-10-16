from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone

from django.views import generic
from .models import Auction, Bid
from .forms import AuctionForm


class AuctionIndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'auctionList'

    def get_queryset(self):
        return Auction.objects.all()


def successfulAuctionPost(request):
    return render(request, 'auctions/success.html', {})


def getNewAuction(request):

    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')

    if request.method == 'POST':

        form = AuctionForm(request.POST)
        if form.is_valid():

            title = (form.cleaned_data.get('title'))
            description = (form.cleaned_data.get('description'))
            minPrice = (form.cleaned_data.get('minPrice'))
            closeDate = (form.cleaned_data.get('closeDate'))
            closeTime = (form.cleaned_data.get('closeTime'))

            deadline = datetime.combine(closeDate, closeTime)
            now = datetime.now()

            if deadline < now + timedelta(hours=72):

                # POSTED auction duration was too short
                errorMessage = 'Auction duration has to be longer than 72 hours.'
                return render(request, 'auctions/create_error.html', {'form': form, 'error': errorMessage})

            awareDeadline = timezone.make_aware(deadline)

            auction = Auction.objects.create(
                author=user,
                title=title,
                description=description,
                minPrice=minPrice,
                deadline=awareDeadline,
                state='Active',
            )
            return render(request, 'auctions/success.html', {'auction': auction})

    else:
        form = AuctionForm()

    return render(request, 'auctions/create.html', {'form': form})


def auctionDetailView(request):
    # TODO: list auctions details
    return None
