from django import forms
from .models import *

class CreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name != "photo":
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        exclude = ['publisher', 'current',
                   'watchlist', 'is_closed', 'date_created']
        widgets = {
            'starting': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }
    name = forms.CharField(max_length=128)
    category = forms.CharField(
        max_length=128, widget=forms.Select(choices=CATEGORIES))
    starting = forms.DecimalField(max_digits=9, decimal_places=2)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    photo = forms.ImageField()


class BidForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Bid
        exclude = ['item', 'bidder']
    bid = forms.FloatField(required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'item']
    description = forms.CharField(max_length=4096, widget=forms.Textarea(
        attrs={'placeholder': "Write a comment...", 'class': 'form-control'}))
