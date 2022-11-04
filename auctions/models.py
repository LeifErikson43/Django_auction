from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    item = models.CharField(max_length=90)
    active = models.BooleanField(default="True")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="current_bidder")
    image_url = models.URLField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=400, default="description")
    category = models.CharField(max_length=100, default="category", blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")


    def __str__(self):
        return f"item: {self.item} ---- owner: {self.owner}"

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="com_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="com_user")
    comment = models.CharField(max_length=400, default="comment")

    def __str__(self):
        return f"{self.item} commented on by: {self.user}"

class Bid(models.Model):

    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user", blank="True", null="True")
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default="0.00")

    def __str__(self):
        return f"{self.item} bid by: {self.bidder} at the amount of: {self.amount}"

class WatchList(models.Model):

    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_user", blank="True", null="True")
    items = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_w", blank="True", null="Ture")

    def __str__(self):
        return f"{self.watcher} is watching: {self.items}"
    