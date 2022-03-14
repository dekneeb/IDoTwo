# Generated by Django 4.0.3 on 2022-03-11 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_item_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='name',
        ),
        migrations.AddField(
            model_name='photo',
            name='pic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.item'),
        ),
    ]