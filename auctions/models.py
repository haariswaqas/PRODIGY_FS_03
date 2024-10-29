from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length = 100)


    def __str__(self):
        return f'{self.category_name}'




class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = "owner")

    def __str__(self):
        return f'{self.bid}.00'

class Listing(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    image_url = models.CharField(max_length = 1000)
    price = models.ForeignKey(Bid, on_delete = models.CASCADE, blank=True, null=True, related_name="bid_user")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name ="user")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, null=True, related_name="type")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="relatedwatchlist")

    def __str__(self):
        return f'{self.category} {self.title}'

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name ="anotheruser")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, blank=True, null=True, related_name ="relatedlisting")
    message = models.CharField(max_length = 300)

    def __str__(self):
        return f'{self.writer} comment on {self.listing} '
