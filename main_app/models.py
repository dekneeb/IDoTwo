from time import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class Item(models.Model):

    title = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
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
        return '%s - %s' % (self.post.title, self.name)


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank = True, null = True)
    sender_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='static/message_photos', blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=60, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='static/images', blank=True, default ='static/images/download.png' )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notification(models.Model):
    #1 = DM, 2 = comment, 3=like
    notification_type=models.IntegerField()
    to_user=models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user=models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Item', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    thread=models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user_has_seen=models.BooleanField(default=False)






