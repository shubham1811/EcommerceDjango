# Generated by Django 2.0 on 2018-08-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_total',
            field=models.DecimalField(decimal_places=2, default=5.99, max_digits=100),
        ),
    ]
