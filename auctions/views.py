import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
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
    return render(request, 'auctions/success.html')


def getNewAuction(request):

    if request.method == 'POST':
        form = AuctionForm(request.POST)

        if form.is_valid():

            closeDate = (form.cleaned_data.get('closeDate'))
            closeTime = (form.cleaned_data.get('closeTime'))

            deadline = datetime.datetime.combine(closeDate, closeTime)
            now = datetime.datetime.now()

            if deadline < now + datetime.timedelta(hours=72):
                print('Duration less than 72 hours.')
                return render(request, 'auctions/create.html', {'form': form})

            return HttpResponseRedirect('success')

    else:
        form = AuctionForm()

    return render(request, 'auctions/create.html', {'form': form})
