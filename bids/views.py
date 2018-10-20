from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from auctions.models import Auction
from bids.forms import BidForm
from bids.models import Bid


class BidView(View):

    def get(self, request, pk):

        user = request.user

        if not user.is_authenticated:
            return HttpResponseRedirect('/login/')

        auction = get_object_or_404(Auction, pk=pk)
        form = BidForm(auction)
        return render(request, 'bids/new_bid.html', {'auction': auction, 'form': form})

    def post(self, request, pk):

        bidder = request.user
        auction = get_object_or_404(Auction, pk=pk)
        form = BidForm(auction, request.POST)

        if bidder.username == auction.author or bidder.username == auction.leader:
            # Bidder is the seller or has made the highest bid
            # TODO: Handle in a user-friendly way
            return HttpResponse(status=400)

        if form.is_valid():
            data = form.cleaned_data
            bid_amount = data['bid']

            if bid_amount > auction.min_price:

                # TODO: Test that this is working when no leader exist

                # Update the min_price
                auction.min_price = bid_amount

                old_leader = User.objects.get(username=auction.leader)
                creator = User.objects.get(username=auction.author)

                send_beaten_mail(old_leader, auction, bid_amount)
                send_seller_mail(creator, auction, bid_amount)

                auction.leader = bidder.username

                Bid.objects.create(auction_id=auction.id, amount=bid_amount, bidder=bidder.username)
                auction.save()

                return HttpResponseRedirect(reverse('auctions:detail', args=(pk,)))

        return render(request, 'bids/new_bid.html', {'auction': auction, 'form': form})


def send_beaten_mail(old_leader, auction, bid_amount):

    email = old_leader.email
    title = auction.title

    subject = 'New bid on auction: %s' % title
    message = 'A new bid of {} had been registered on auction: {}'.format(bid_amount, title)
    from_address = 'admin@yaas.com'
    to_address_list = [email, ]

    send_mail(subject, message, from_address, to_address_list)


def send_seller_mail(seller, auction, bid_amount):
    pass
