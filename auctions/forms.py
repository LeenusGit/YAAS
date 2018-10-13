import datetime

from django import forms
from django.utils import timezone


class AuctionForm(forms.Form):

    title = forms.CharField(label='Auction title', max_length=50, initial='Test Title')
    description = forms.CharField(label='Description', widget=forms.Textarea, initial='Test description')
    minPrice = forms.DecimalField(label='Starting price', max_digits=8, decimal_places=2, min_value=0, initial=20)

    closeDate = forms.DateField(
        label='Auction close date (dd.mm.yyyy)',
        input_formats=('%d.%m.%Y',),
        widget=forms.DateInput(format='%d.%m.%Y'),
        initial=datetime.date.today() + datetime.timedelta(days=4),
    )
    closeTime = forms.TimeField(
        label='Auction close time (hh:mm)',
        widget=forms.TimeInput(format='%H:%M'),
        initial=datetime.datetime.today(),
    )
