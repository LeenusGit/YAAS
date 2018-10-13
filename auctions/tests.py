import datetime

from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import AuctionForm

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

    username = 'JLennon'
    firstname = 'John'
    lastName = 'Lennon'
    email = 'lennon@thebeatles.com'
    password = 'johnpassword'

    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = firstname
    user.last_name = lastName
    return user


class AuctionIndexViewTests(TestCase):

    def testNoAuctions(self):
        response = self.client.get(reverse('auctions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['auctionList'], [])

    def testOneAuction(self):
        auction = createDefinedAuction()
        context = '<Auction: %s>' % auction.title
        response = self.client.get(reverse('auctions:index'))
        self.assertQuerysetEqual(response.context['auctionList'], [context])


class CreateAuctionFormTests(TestCase):

    def testCreateValidAuction(self):
        formData = {'title': 'Ford Focus',
                    'description': 'A car of brand Ford and model Focus',
                    'minPrice': 10.5,
                    'closeDate': '2018-10-16',
                    'closeTime': '19:23:59',
                    }
        form = AuctionForm(data=formData)
        self.assertEqual(form.is_valid(), True)


class AuctionModelTests(TestCase):

    def testNewAuctionState(self):
        auction = createDefinedAuction()
        self.assertEqual(auction.state, 'Active')


class UserModelTests(TestCase):

    def testNewUserName(self):
        user = createDefinedUser()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Lennon')

    def testAuthenticateUser(self):
        user = createDefinedUser()
        username = 'JLennon'
        password = 'johnpassword'
        user2 = authenticate(username=username, password=password)

        self.assertEquals(user, user2)
