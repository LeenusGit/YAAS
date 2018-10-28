
from django import forms

from auctions import currencies


class BidForm(forms.Form):

    bid = forms.DecimalField()
    currency = forms.HiddenInput()

    def __init__(self, min_price, currency_code, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)

        min_bid_increment = round(currencies.convert('EUR', 0.01, currency_code), 2)
        if min_bid_increment == 0:
            min_bid_increment = 0.01
        min_bid_value = min_price + min_bid_increment

        # print('min_bid_value:', min_bid_value)
        # print('min_price: ', min_price)
        # print(min_bid_value == min_price)

        self.fields['bid'] = forms.DecimalField(
            initial=min_bid_value,
            min_value=min_bid_value,
            label='Bid Amount',
            max_digits=8,
            decimal_places=2,
            widget=forms.NumberInput(attrs={'step': str(min_bid_increment)})
        )

        self.fields['currency'] = forms.CharField(
            max_length=3,
            widget=forms.HiddenInput(attrs={'name': 'currency', 'value': str(currency_code)})
        )
