from django.shortcuts import render, get_object_or_404
from django.views import View

from auctions.models import Auction


class BidView(View):

    def get(self, request, pk):

        auction = get_object_or_404(Auction, pk=pk)

        return render(request, 'bids/new_bid.html', {'auction': auction})

    def post(self, request):
        pass
