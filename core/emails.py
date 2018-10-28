from django.contrib.auth.models import User
from django.core.mail import send_mail


def send_new_bid_mail(user, auction, bid_amount):

    user_address = user.email
    title = auction.title

    subject = 'New bid on auction: %s' % title
    message = 'A new bid of {} has been registered on auction: {}'.format(bid_amount, title)
    from_address = 'admin@yaas.com'
    to_address_list = [user_address, ]

    send_mail(subject, message, from_address, to_address_list)


def send_ban_email(user, auction):
    # Should send emails to the creator and the bidders of the banned auction
    user_address = user.email
    title = auction.title
    from_address = 'admin@yaas.com'

    subject = '%s Ban' % title
    message_to_creator = 'Hi {},\n Your auction {} has been been banned due to violation of ' \
                         'terms of service'.format(user.username, title)
    creator_email_list = [user_address, ]
    send_mail(subject, message_to_creator, from_address, creator_email_list)

    message_to_bidders = 'We regret to inform you that the auction {} has benn banned ' \
                         'due to violation of terms of service'.format(title)
    bidder_email_list = []

    # Importing locally because of circular import
    from bids.models import Bid
    bid_list = Bid.objects.filter(auction_id=auction.id)
    # Fill bid_list with emails of the bidders
    for bid in bid_list:
        bidder = User.objects.get(username=bid.bidder)
        bidder_email_list.append(bidder.email)

    send_mail(subject, message_to_bidders, from_address, bidder_email_list)


def send_confirm_email(user, auction):
    user_address = user.email
    title = auction.title

    subject = '%s confirmation' % title
    message = 'Hi %s,\n Your auction %s has been submitted to YAAS' % (user.username, title)
    from_address = 'admin@yaas.com'
    to_address_list = [user_address, ]

    send_mail(subject, message, from_address, to_address_list)


def notify_bidders(winner, auction):

    title = auction.title
    from_address = 'admin@yaas.com'
    subject = 'Auction {} closed.'.format(title)

    message_to_bidders = 'The auction {} has been resolved, unfortunately your bid was beaten'.format(title)
    bidder_email_list = []

    # Importing locally because of circular import
    from bids.models import Bid
    bid_list = Bid.objects.filter(auction_id=auction.id)
    # Fill bid_list with emails of the bidders
    for bid in bid_list:
        bidder = User.objects.get(username=bid.bidder)

        # Add address if bidder is not the winner
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
