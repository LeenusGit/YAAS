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
    deadline = timezone.now() + timedelta(days=3)
    min_price = 10.50

    auction = Auction.objects.create(
        author=author,
        title=title,
        description=description,
        deadline=deadline,
        min_price=min_price
    )
    return auction


def valid_form_data():

    date = datetime.now() + timedelta(days=3)

    data = {
        'title': 'Ford Fiesta',
        'description': 'A car of brand Ford and model Fiesta',
        'min_price': 20.5,
        'close_date': date.date(),
        'close_time': '12:34',
    }
    return data


class AuctionIndexViewTests(TestCase):

    def test_no_auctions(self):
        response = self.client.get(reverse('auctions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['auction_list'], [])

    def test_one_auction(self):
        auction = create_defined_auction()
        context = '<Auction: %s>' % auction.title
        response = self.client.get(reverse('auctions:index'))
        self.assertQuerysetEqual(response.context['auction_list'], [context])


class CreateAuctionTests(TestCase):

    def test_create_valid_formatted_auction(self):
        data = valid_form_data()
        data['close_date'] = '23.11.2018'
        form = AuctionForm(data=data)
        self.assertEqual(form.is_valid(), True)

    def test_new_auction_no_user(self):

        data = valid_form_data()
        response = self.client.get(reverse('auctions:create'), data)
        self.assertRedirects(response, reverse('core:login'))

    def test_confirm_valid_auction(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        date = timezone.now() + timedelta(days=3, minutes=1)
        data = valid_form_data()
        data['deadline'] = date
        response = self.client.post(reverse('auctions:confirm'), data)

        self.assertRedirects(response, reverse('auctions:success'))

    def test_confirm_past_auction(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        past_date = timezone.now() - timedelta(minutes=1)
        data = valid_form_data()
        data['deadline'] = past_date
        response = self.client.post(reverse('auctions:confirm'), data)
        print(response.reason_phrase)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('past' in response.reason_phrase, True)

    def test_confirm_too_short_auction(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        past_date = timezone.now() + timedelta(days=2, minutes=1)
        data = valid_form_data()
        data['deadline'] = past_date
        response = self.client.post(reverse('auctions:confirm'), data)
        print(response.reason_phrase)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('duration' in response.reason_phrase, True)


class AuctionModelTests(TestCase):

    def test_new_auction_state(self):
        auction = create_defined_auction()
        self.assertEqual(auction.state, 'Active')
