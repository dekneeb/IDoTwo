# Generated by Django 4.0.3 on 2022-03-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_alter_comment_options_remove_comment_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='city',
            field=models.CharField(max_length=40),
        ),
    ]
