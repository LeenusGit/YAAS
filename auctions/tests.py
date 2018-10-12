import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Auction


def createDefinedAuction():
    author = 'Linus'
    title = 'Ford Focus'
    description = 'A car of brand Ford and model Focus'
    durationDays = 1
    deadline = timezone.now() + datetime.timedelta(days=durationDays)
    minPrice = 10.50

    return Auction.objects.create(author=author, title=title, description=description,
                                  deadline=deadline, minPrice=minPrice)


def createDefinedUser():

    userName = 'JLennon'
    firstname = 'John'
    lastName = 'Lennon'
    email = 'lennon@thebeatles.com'
    password = 'johnpassword'

    user = User.objects.create_user(username=userName, email=email, password=password)
    user.first_name = firstname
    user.last_name = lastName
    return user


class AuctionModelTests(TestCase):

    def testNewAuctionState(self):
        auction = createDefinedAuction()
        self.assertEqual(auction.state, 'Active')


class UserModelTests(TestCase):

    def testNewUserName(self):

        user = createDefinedUser()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Lennon')
