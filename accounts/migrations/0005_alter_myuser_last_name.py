# Generated by Django 4.2.7 on 2023-12-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_myuser_auth_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
