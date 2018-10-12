from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views import generic
from .models import Auction, Bid
from .forms import AuctionForm


class AuctionIndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'auctionList'

    def get_queryset(self):
        return Auction.objects.all()


def getNewAuction(request):

    if request.method == 'POST':
        form = AuctionForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('success')

    else:
        form = AuctionForm()

    return render(request, 'auctions/create.html', {'form': form})
