# Generated by Django 2.0 on 2018-09-10 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GuestForm',
            new_name='GuestEmail',
        ),
    ]
