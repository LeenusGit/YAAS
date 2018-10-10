from django.db import models
from django.utils import timezone


class Auction(models.Model):

    author = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    minPrice = models.DecimalField(max_digits=8, decimal_places=2)
    deadline = models.DateTimeField('Time auction closes')
    banned = models.BooleanField

    def getState(self):

        if self.banned:
            return "Banned"

        now = timezone.now()

        if self.deadline > now:
            return "Active"
        else:
            return "Due"

    def __str__(self):
        return self.title


class Bid(models.Model):

    amount = models.DecimalField(max_digits=8, decimal_places=2)




