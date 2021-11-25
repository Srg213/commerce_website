from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 128 )
    starting_bid = models.IntegerField()
    image = models.URLField(blank = True)
    category = models.CharField(max_length=32 ,blank = True)
    creator = models.ForeignKey(User, related_name= 'owner' ,on_delete=models.CASCADE)
    customer = models.ManyToManyField(User, blank =True , related_name= 'watchlist')
    state = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.title} - {self.description} - {self.category}'

class Bid(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE , related_name= "customers" )
    item = models.ForeignKey(Listing, on_delete=models.CASCADE , related_name= "new_bids")
    price= models.IntegerField()
    def __str__(self):
        return f'{self.user} - {self.item} - {self.price}'
        
class Comments(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE , related_name= "users")
    comments= models.ForeignKey(Listing, on_delete=models.CASCADE , related_name = 'reviews')
    text =  models.CharField(max_length = 64)
    def __str__(self):
        return f'{self.customer} - {self.comments} - {self.text}'