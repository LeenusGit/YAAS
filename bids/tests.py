from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from auctions.models import Auction


def create_defined_auction():

    User.objects.create_user(username='TestUser', password='12345')

    author = 'TestUser'
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


class AuctionIndexViewTests(TestCase):

    def test_valid_bid(self):

        auction = create_defined_auction()
        self.user = User.objects.create_user(username='TestUser2', password='12345')
        self.client.login(username='TestUser2', password='12345')

        data = {
            'bid': auction.min_price + 0.01,
            'currency': 'EUR'
        }

        response = self.client.post(reverse('bids:bid', args=(auction.pk, )), data)
        self.assertRedirects(
            response,
            reverse('bids:success', args=(auction.pk, )),
            status_code=302,
            target_status_code=200
        )

    def test_invalid_bid(self):

        auction = create_defined_auction()
        self.user = User.objects.create_user(username='TestUser2', password='12345')
        self.client.login(username='TestUser2', password='12345')

        data = {
            'bid': auction.min_price + 0.00,
            'currency': 'EUR'
        }

        response = self.client.post(reverse('bids:bid', args=(auction.pk, )), data)
        self.assertContains(response, 'greater than or equal to')
