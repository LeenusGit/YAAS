import datetime

from django import forms
from django.utils import timezone


class AuctionForm(forms.Form):

    title = forms.CharField(label='Auction title', max_length=50, initial='Test Title')
    description = forms.CharField(label='Description', widget=forms.Textarea, initial='Test description')
    minPrice = forms.DecimalField(label='Starting price', max_digits=8, decimal_places=2, initial=20)

    closeDate = forms.DateTimeField(
        label='Auction close date',
        initial=datetime.date.today() + datetime.timedelta(days=3),
        widget=forms.DateInput,
    )
    closeTime = forms.TimeField(
        label='Auction close time',
        initial=datetime.datetime.today(),
        widget=forms.TimeInput,
    )