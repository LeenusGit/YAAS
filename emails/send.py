from django.contrib.auth.models import User
from django.core.mail import send_mail


def send_new_bid_mail(user, auction, bid_amount):

    email = user.email
    title = auction.title

    subject = 'New bid on auction: %s' % title
    message = 'A new bid of {} has been registered on auction: {}'.format(bid_amount, title)
    from_address = 'admin@yaas.com'
    to_address_list = [email, ]

    send_mail(subject, message, from_address, to_address_list)


def send_ban_email(user, auction):
    # Should send emails to the creator and the bidders of the banned auction
    email = user.email
    title = auction.title
    from_address = 'admin@yaas.com'

    subject = '%s Ban' % title
    message_to_creator = 'Hi {},\n Your auction {} has been been banned due to violation of ' \
                         'terms of service'.format(user.username, title)
    creator_email_list = [email, ]
    send_mail(subject, message_to_creator, from_address, creator_email_list)

    message_to_bidders = 'We regret to inform you that the auction {} has benn banned ' \
                         'due to violation of terms of service'.format(title)
    bidder_email_list = []
    from bids.models import Bid
    bid_list = Bid.objects.filter(auction_id=auction.id)
    # Fill bid_list with emails of the bidders
    for bid in bid_list:
        bidder = User.objects.get(username=bid.bidder)
        bidder_email_list.append(bidder.email)

    send_mail(subject, message_to_bidders, from_address, bidder_email_list)


def send_confirm_email(user, auction):
    email = user.email
    title = auction.title

    subject = '%s confirmation' % title
    message = 'Hi %s,\n Your auction %s has been submitted to YAAS' % (user.username, title)
    from_address = 'admin@yaas.com'
    to_address_list = [email, ]

    send_mail(subject, message, from_address, to_address_list)
