from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Auction, Bid


class AuctionIndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'auctionList'

    def get_queryset(self):
        return Auction.objects.all()
