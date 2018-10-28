import base64
from datetime import timedelta, datetime

from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone

from core.emails import send_new_bid_mail


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

    def get_version(self):
        version_string = str(self.description) + str(self.min_price)
        version_bytes = bytes(version_string, 'utf-8')
        version_encoded_string = base64.b64encode(version_bytes).decode('utf-8')
        return version_encoded_string

    def to_dict(self):

        fields = {
            'creator': self.author,
            'title': self.title,
            'description': self.description,
            'min_price': str(self.min_price),
            'deadline': str(self.deadline.isoformat()),
        }

        auction_dict = {
            'model': 'Auction',
            'pk': self.pk,
            'version': self.get_version(),
            'fields': fields,
        }
        return auction_dict

    @classmethod
    def bid(cls, id, amount, bidder):
        with transaction.atomic():

            # nowait to ensure that if the resource is locked an error is raised
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

            # Extend deadline if auction closes within 5 minutes
            now = timezone.make_aware(datetime.now())
            five_minutes_from_now = timezone.make_aware(datetime.now() + timedelta(minutes=5))
            if auction.deadline <= five_minutes_from_now:
                auction.deadline = now + timedelta(minutes=5)

            # TODO: Test auction deadline extension

            auction.save()

        return auction

    @classmethod
    def new_description(cls, id, description):
        with transaction.atomic():

            auction = cls.objects.select_for_update().get(id=id)
            auction.description = description
            auction.save()

            return auction
