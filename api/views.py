import json

from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from auctions import currencies
from auctions.forms import SearchForm
from auctions.models import Auction
from bids.forms import BidForm
from bids.models import Bid

fields = ('title', 'author', 'description', 'min_price', 'deadline')


def auctions(request):

    form = SearchForm(request.GET)
    auction_list = []

    if form.is_valid():
        search = form.cleaned_data.get('search')
        auction_list = Auction.objects.filter(title__icontains=search, state='Active')

    data = serializers.serialize('json', auction_list, fields=fields)
    return HttpResponse(content=data, content_type='json', status=200)


def auction_detail(request, pk):

    try:
        auction = Auction.objects.get(pk=pk)
    except Auction.DoesNotExist:
        return JsonResponse(error_dict(status=404, reason='Auction does not exist.'))

    return JsonResponse(auction.to_dict())


def new_bid(request, pk):

    try:
        auction = Auction.objects.get(pk=pk)
    except Auction.DoesNotExist:
        return JsonResponse(error_dict(status=404, reason='Auction does not exist.'))

    if request.method == 'GET':
        return JsonResponse(auction.to_dict())

    if request.method == 'POST':

        try:
            username = request.POST['username']
            password = request.POST['password']
            currency_code = request.POST['currency']
            version = request.POST['version']
            bid_amount = request.POST['bid']
        except KeyError:
            return JsonResponse(error_dict(status=400, reason='Missing keys in body.'))

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse(error_dict(status=401, reason='Wrong username or password.'))
        else:
            bidder = user

        if bidder.username == auction.author \
                or bidder.username == auction.leader \
                or auction.state != 'Active':
            return JsonResponse(error_dict(status=400, reason='user cannot bid on auction.'))

        auction_version = auction.get_version()
        if version != auction_version:
            print(version,  ' != ',  str(auction_version))
            return JsonResponse(error_dict(status=400, reason='Auction was updated.'))

        if not currencies.is_currency_valid(currency_code):
            return JsonResponse(error_dict(status=400, reason='Currency code does not exist.'))

        min_price = auction.min_price
        form = BidForm(min_price, currency_code,  request.POST)

        if form.is_valid():
            data = form.cleaned_data
            bid_amount = data['bid']
            euro_bid_amount = currencies.convert(currency_code, float(bid_amount), 'EUR')

            if euro_bid_amount > min_price:
                try:
                    Auction.bid(auction.id, amount=euro_bid_amount, bidder=bidder)
                    bid = Bid.objects.create(auction_id=auction.id, amount=euro_bid_amount, bidder=bidder.username)
                    bid.save()
                    # Bid was successful
                    return JsonResponse(success_dict(status=201, saved_bid=bid_amount))
                except:
                    # auction is locked while updating
                    return JsonResponse(error_dict(status=400, reason='Auction was updated by somebody else.'))
            else:
                return JsonResponse(error_dict(status=400, reason='Minimum bid is 0.1€'))
        else:
            return JsonResponse(error_dict(status=400, reason='Key values are not in right format'))


def error_dict(status, reason):

    error = {
        'status_code': status,
        'reason': reason,
    }
    resp_dict = {
        'error': error
    }
    return resp_dict


def success_dict(status, saved_bid):

    info = {
        'status_code': status,
        'New bid': saved_bid,
    }
    resp_dict = {
        'success': info
    }
    return resp_dict
