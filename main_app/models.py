from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Item(models.Model):

    title = models.CharField(max_length=100)
    city = models.CharField(max_length=15)
    description = models.TextField(max_length = 500)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipping = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = models.ImageField(null=True, blank=True, upload_to='static/images/')
   

    def __str__(self):
        return self.title
    
    @property
    def price_display(self):
        return "$%s" % self.price

    class Meta:
        ordering=['title']

class Comment(models.Model):
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    post = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering=['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)




