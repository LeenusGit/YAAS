from django.db import models
from auctions.models import Auction


class Bid(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    bidder = models.CharField(max_length=30)

    def __str__(self):
        return self.id.__str__()
