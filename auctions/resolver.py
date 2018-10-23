import threading
import time
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from .models import Auction
from bids.models import Bid


class ResolveThread(threading.Thread):

    def run(self):

        # FOR TESTING PURPOSES
        # author = 'Linus'
        # title = 'Ford Focus'
        # description = 'A car of brand Ford and model Focus'
        # deadline = timezone.now() + timedelta(minutes=2)
        # min_price = 10.50
        # leader = User.objects.get(username='TestUser')
        #
        # auction = Auction.objects.create(
        #     author=author,
        #     title=title,
        #     description=description,
        #     deadline=deadline,
        #     min_price=min_price,
        #     leader=leader.username,
        # )
        # auction.save()

        while True:
            # Update every second
            time.sleep(1)
            # print(timezone.now())
            active_auction_list = Auction.objects.filter(state='Active')

            for auction in active_auction_list:

                # print(auction.title, ': ', auction.deadline)

                if auction.deadline <= timezone.now():

                    winner = User.objects.get(username=auction.leader)
                    auction.state = 'Adjudicated'
                    auction.save()

                    # Notify winner and bidders
                    notify_winner(winner, auction)
                    notify_bidders(winner, auction)


def notify_bidders(winner, auction):

    title = auction.title
    from_address = 'admin@yaas.com'
    subject = 'Auction {} closed.'.format(title)

    message_to_bidders = 'The auction {} has been resolved, unfortunately your bid was beaten'.format(title)
    bidder_email_list = []
    bid_list = Bid.objects.filter(auction_id=auction.id)
    # Fill bid_list with emails of the bidders
    for bid in bid_list:
        bidder = User.objects.get(username=bid.bidder)

        if bidder.username != winner.username:
            bidder_email_list.append(bidder.email)

    send_mail(subject, message_to_bidders, from_address, bidder_email_list)


def notify_winner(winner, auction):

    email = winner.email
    title = auction.title
    from_address = 'admin@yaas.com'
    subject = 'Winner of {}'.format(title)
    message_to_creator = 'Congratulations {},\n You are the winner of auction {}.'.format(winner.username, title)
    creator_email_list = [email, ]
    send_mail(subject, message_to_creator, from_address, creator_email_list)
