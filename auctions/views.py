from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from django.views import generic, View
from .models import Auction, Bid
from .forms import AuctionForm


class AuctionIndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'auctionList'

    def get_queryset(self):
        return Auction.objects.all()


def successfulAuctionPost(request):
    return render(request, 'auctions/success.html', {})


def newAuction(request):

    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')
    form = AuctionForm()
    return render(request, 'auctions/create.html', {'form': form})


class AuctionDetailView(View):

    def get(self, request, pk):

        auction = Auction.objects.get(pk=pk)

        return render(request, 'auctions/detail.html', {'auction': auction})


class ConfirmAuctionView(View):

    def get(self, request):

        user = request.user
        form = AuctionForm(request.GET)
        if form.is_valid():

            title = (form.cleaned_data.get('title'))
            description = (form.cleaned_data.get('description'))
            minPrice = (form.cleaned_data.get('minPrice'))
            closeDate = (form.cleaned_data.get('closeDate'))
            closeTime = (form.cleaned_data.get('closeTime'))

            deadline = datetime.combine(closeDate, closeTime)

            if deadline < datetime.now() + timedelta(hours=72):
                # POSTED auction duration was too short
                errorMessage = 'Auction duration has to be longer than 72 hours.'
                return render(request, 'auctions/create_error.html', {'form': form, 'error': errorMessage})

            awareDeadline = timezone.make_aware(deadline)

            auction = Auction(
                author=user,
                title=title,
                description=description,
                minPrice=minPrice,
                deadline=awareDeadline,
            )
            return render(request, 'auctions/confirm.html', {'auction': auction, 'form': form})

        return render(request, 'auctions/create.html', {'form': form})

    def post(self, request):

        user = request.user
        data = request.POST
        auction = Auction(
            author=user,
            title=data['title'],
            description=data['description'],
            minPrice=data['minPrice'],
            deadline=data['deadline'],
        )
        auction.save()
        return HttpResponseRedirect('success')


# def confirmAuction(request):
#
#     user = request.user
#
#     if request.method == 'GET':
#
#         form = AuctionForm(request.GET)
#         if form.is_valid():
#
#             title = (form.cleaned_data.get('title'))
#             description = (form.cleaned_data.get('description'))
#             minPrice = (form.cleaned_data.get('minPrice'))
#             closeDate = (form.cleaned_data.get('closeDate'))
#             closeTime = (form.cleaned_data.get('closeTime'))
#
#             deadline = datetime.combine(closeDate, closeTime)
#
#             if deadline < datetime.now() + timedelta(hours=72):
#                 # POSTED auction duration was too short
#                 errorMessage = 'Auction duration has to be longer than 72 hours.'
#                 return render(request, 'auctions/create_error.html', {'form': form, 'error': errorMessage})
#
#             awareDeadline = timezone.make_aware(deadline)
#
#             print(awareDeadline)
#
#             auction = Auction(
#                 author=user,
#                 title=title,
#                 description=description,
#                 minPrice=minPrice,
#                 deadline=awareDeadline,
#             )
#             return render(request, 'auctions/confirm.html', {'auction': auction, 'form': form})
#         else:
#             return render(request, 'auctions/create.html', {'form': form})
#
#     if request.method == 'POST':
#         data = request.POST
#
#         auction = Auction(
#             author=user,
#             title=data['title'],
#             description=data['description'],
#             minPrice=data['minPrice'],
#             deadline=data['deadline'],
#         )
#         auction.save()
#
#         return HttpResponseRedirect('success')
#
#     form = AuctionForm()
#     return render(request, 'auctions/create.html', {'form': form})


