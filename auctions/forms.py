from django import forms

from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = "__all__"
        exclude = ['user', 'active_user', 'watchlist', 'current_price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentSection
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={
            "class": "form-control", 
            "rows": 8,
            "placeholder": "Type your comment",
            }),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control',
            }),
        }
        labels = {
            "bid": "Place a Bid higher than the current bid to stand a chance to win auction",

        }
        