from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Item(models.Model):

    title = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    city = models.CharField(max_length=15)
    description = models.TextField(max_length = 500)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipping = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    @property
    def price_display(self):
        return "$%s" % self.price

    class Meta:
        ordering=['title']


# class Location(models.Model):
#     name = models.CharField(max_length=15)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="location")

#     def __str__(self):
#         return self.name

class Photo(models.Model):
    url = models.CharField(max_length=200)
    pic = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for pic_id: {self.pic_id} @{self.url}"

