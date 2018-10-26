from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from auctions import currencies
from auctions.models import Auction
from bids.forms import BidForm
from bids.models import Bid


class BidView(View):

    def get(self, request, pk):

        user = request.user

        if not user.is_authenticated:
            return HttpResponseRedirect('/login/')

        auction = get_object_or_404(Auction, pk=pk)

        try:
            currency_code = request.session['currency']
        except KeyError:
            currency_code = 'EUR'
        converted_price = round(currencies.convert('EUR', float(auction.min_price), currency_code), 2)

        form = BidForm(converted_price, currency_code)

        context = {
            'auction': auction,
            'form': form,
            'converted_price': converted_price,
        }

        return render(request, 'bids/new_bid.html', context)

    def post(self, request, pk):

        print(request.POST)

        bidder = request.user
        auction = get_object_or_404(Auction, pk=pk)
        min_price = auction.min_price
        currency_code = request.POST['currency']

        form = BidForm(min_price, currency_code, request.POST)

        if bidder.username == auction.author \
                or bidder.username == auction.leader \
                or auction.state != 'Active':
            # Bidder is the seller or has made the highest bid or auction is not active
            # TODO: Test that POST request to banned auctions are ignored
            # TODO: Handle in a more user-friendly way
            return HttpResponse(status=400)

        if form.is_valid():
            data = form.cleaned_data
            bid_amount = data['bid']
            currency = data['currency']

            print('Bid_amount = ', bid_amount)
            euro_bid_amount = round(currencies.convert(currency, float(bid_amount), 'EUR'), 2)
            print('Euro bid amount: ', euro_bid_amount)

            if euro_bid_amount > min_price:

                try:
                    auction = Auction.bid(auction.id, amount=euro_bid_amount, bidder=bidder)
                    bid = Bid.objects.create(auction_id=auction.id, amount=euro_bid_amount, bidder=bidder.username)
                    bid.save()
                except:
                    # Someone else has locked the auction
                    return HttpResponseRedirect(reverse('auctions:detail', args=(pk,)))

                return HttpResponseRedirect(reverse('auctions:detail', args=(pk,)))

            else:
                print(euro_bid_amount, ' was lover than ', min_price)
                return HttpResponseRedirect(reverse('auctions:detail', args=(pk,)))

        else:
            # The form is not valid
            return render(request, 'bids/new_bid.html', {'auction': auction, 'form': form})
