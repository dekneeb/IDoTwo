from django.contrib import admin
from .models import Item, Comment, UserProfile, Notification



# Register your models here.
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Notification)








