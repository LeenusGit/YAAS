from decimal import Decimal

from django import forms


class BidForm(forms.Form):

    bid = forms.DecimalField()

    def __init__(self, auction, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)

        min_bid_increment = Decimal('0.01')
        min_bid_value = auction.min_price + min_bid_increment

        self.fields['bid'] = forms.DecimalField(
            initial=min_bid_value,
            min_value=min_bid_value,
            label='Bid Amount',
            max_digits=8,
            decimal_places=2,
        )
