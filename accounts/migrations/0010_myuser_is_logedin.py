# Generated by Django 4.2.7 on 2024-06-04 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_logedin',
            field=models.BooleanField(default=False),
        ),
    ]
