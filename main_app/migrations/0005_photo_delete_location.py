# Generated by Django 4.0.3 on 2022-03-11 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_item_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('pic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item')),
            ],
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
