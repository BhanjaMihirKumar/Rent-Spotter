# Generated by Django 4.2.7 on 2023-11-24 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0006_userprofile_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='location',
            new_name='location_info',
        ),
    ]
