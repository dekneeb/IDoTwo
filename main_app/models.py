from time import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

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
    post = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering=['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank = True, null = True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='static/message_photos', blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

class Profile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')





