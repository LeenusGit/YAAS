from django.core.mail import send_mail
from django.db import models, transaction
from django.contrib.auth.models import User


class Auction(models.Model):

    author = models.CharField(max_length=150)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    min_price = models.DecimalField(max_digits=8, decimal_places=2)
    deadline = models.DateTimeField('Time auction closes')
    leader = models.CharField(max_length=150, default='', blank=True)

    states = (
        (0, 'Active'),
        (1, 'Banned'),
        (2, 'Due'),
        (3, 'Adjudicated'),
    )
    state = models.CharField(max_length=20, choices=states, default='Active')

    def __str__(self):
        return self.title

    @classmethod
    def bid(cls, id, amount, bidder):
        with transaction.atomic():

            # nowait ensure that if the resource is locked the
            auction = cls.objects.select_for_update(nowait=True).get(id=id)
            auction.min_price = amount

            # Ignore the previous leader if there is none
            if auction.leader != '':
                old_leader = User.objects.get(username=auction.leader)
                send_new_bid_mail(old_leader, auction, amount)

            # Inform the auction creator
            creator = User.objects.get(username=auction.author)
            send_new_bid_mail(creator, auction, amount)

            # Update the auction leader
            auction.leader = bidder.username

            auction.save()

        return auction

    @classmethod
    def new_description(cls, id, description):
        with transaction.atomic():

            auction = cls.objects.select_for_update().get(id=id)
            auction.description = description
            auction.save()

            return auction


def send_new_bid_mail(user, auction, bid_amount):

    email = user.email
    title = auction.title

    subject = 'New bid on auction: %s' % title
    message = 'A new bid of {} has been registered on auction: {}'.format(bid_amount, title)
    from_address = 'admin@yaas.com'
    to_address_list = [email, ]

    send_mail(subject, message, from_address, to_address_list)


