from django import forms


class AuctionForm(forms.Form):

    title = forms.CharField(label='Auction Title', max_length=50)
    description = forms.CharField(widget=forms.Textarea)
