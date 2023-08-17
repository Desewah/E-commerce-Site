from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Bid(models.Model):
    bid = models.FloatField(default=0)
    bidder =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", blank=True, null=True)
    bid_date = models.DateField(auto_now_add=True)



class Category(models.Model):
    category = models.CharField(max_length=64)
    class Meta:  
        """
        The class name doesn't pluralise by appending 's',
        hence the use of verbose_name_plural to define the plural
        """
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.category}"
    


class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", blank=True, null=True)
    title = models.CharField(max_length=64)
    description =models.TextField(max_length=256)
    current_price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid_price", blank=True, null=True)
    image_url = models.URLField(max_length=350)
    active_user = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.category}: {self.title}"    

class CommentSection(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", blank=True, null=True)
    post = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment", blank=True, null=True)
    email = models.EmailField()
    comment = models.TextField()
    time_created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['time_created']

    def __str__(self):
        return "{} on {} : {}".format(self.author, self.time_created, self.comment)
    
