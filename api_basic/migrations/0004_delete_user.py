# Generated by Django 3.2.8 on 2021-11-04 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_basic', '0003_meal_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
