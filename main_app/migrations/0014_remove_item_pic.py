# Generated by Django 4.0.3 on 2022-03-11 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_remove_photo_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='pic',
        ),
    ]
