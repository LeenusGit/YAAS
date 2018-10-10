from django.shortcuts import render

# Create your views here.
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'auctionList'

    def get_queryset(self):
        return
