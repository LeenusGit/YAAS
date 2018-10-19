from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .forms import AuctionForm

from .models import Auction


def create_defined_auction():
    author = 'Linus'
    title = 'Ford Focus'
    description = 'A car of brand Ford and model Focus'
    duration_days = 1
    deadline = timezone.now() + timedelta(days=duration_days)
    min_price = 10.50

    return Auction.objects.create(author=author, title=title, description=description,
                                  deadline=deadline, min_price=min_price)


def create_defined_user():

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
        self.assertQuerysetEqual(response.context['auction_list'], [])

    def testOneAuction(self):
        auction = create_defined_auction()
        context = '<Auction: %s>' % auction.title
        response = self.client.get(reverse('auctions:index'))
        self.assertQuerysetEqual(response.context['auction_list'], [context])


class CreateAuctionFormTests(TestCase):

    def testCreateValidFormattedAuction(self):
        form_data = {
            'title': 'Ford Focus',
            'description': 'A car of brand Ford and model Focus',
            'min_price': 12.3,
            'close_date': '12.03.4567',
            'close_time': '12:34',
        }
        form = AuctionForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def testCreatePastAuction(self):
        c = Client()
        past_time = timezone.make_aware(datetime.now() - timedelta(days=1))
        data = {
            'title': 'Ford Fiesta',
            'description': 'A car of brand Ford and model Fiesta',
            'min_price': 12.3,
            'deadline': past_time,
                    }
        response = c.post(reverse('auctions:confirm'), data)
        self.assertEqual(response.status_code, 400)


class AuctionModelTests(TestCase):

    def testNewAuctionState(self):
        auction = create_defined_auction()
        self.assertEqual(auction.state, 'Active')


class UserModelTests(TestCase):

    def testNewUserName(self):
        user = create_defined_user()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Lennon')

    def testAuthenticateUser(self):
        user = create_defined_user()
        username = 'JLennon'
        password = 'johnpassword'
        user2 = authenticate(username=username, password=password)
        self.assertEquals(user, user2)
