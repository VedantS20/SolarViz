# Generated by Django 2.2 on 2020-11-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201128_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
