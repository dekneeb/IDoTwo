from django.db import models

# Create your models here.

class Item(models.Model):

    title = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    location = models.CharField(max_length=15)
    description = models.TextField(max_length = 500)
    price = models.IntegerField(default=0)
    shipping = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['title']
