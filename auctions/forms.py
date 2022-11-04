from django import forms
from .models import User, Listing, Comment, Bid, WatchList
from django.utils import timezone
import datetime

class CreateListingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Listing Name', 'class' : 'Creat_Form_Name'}))
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.TextInput(attrs={'placeholder' : '0.00'}))
    image_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder' : 'insert url for the item image'}), required=False)
    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Category'}))
    description = forms.CharField( max_length=400, widget=forms.Textarea(attrs={'placeholder' : 'Discreption of new item.'}))
    owner = forms.HiddenInput()