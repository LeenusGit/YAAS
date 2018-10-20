from django.db import models
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


# class Bid(models.Model):
#
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
