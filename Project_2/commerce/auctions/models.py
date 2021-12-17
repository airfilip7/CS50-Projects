from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError


CATEGORIES = [
    ("Broomsticks", "Broomsticks"),
    ("Category 1", "Category 1"),
    ("Category 2", "Category 2"),
    ("Category 3", "Category 3"),
    ("Category 4", "Category 4"),
    ("Category 5", "Category 5"),
    ("Category 6", "Category 6"),
    ("Category 7", "Category 7"),
    ("Category 8", "Category 8"),
]

class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    watchlist = models.ManyToManyField('Item', blank=True, related_name="items")

class Item(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publisher")
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128, choices=CATEGORIES)
    starting = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=4096, blank=True)
    photo = models.ImageField(upload_to='item_photo')
    is_closed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pk} - {self.name} by {self.publisher}"
    
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bidded_item", default=None)
    
    def __str__(self):
        return f"{self.bid} by {self.bidder} on {self.item}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    description = models.CharField(max_length=4096)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comment")
    date_posted = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user} commented on {self.item}"

