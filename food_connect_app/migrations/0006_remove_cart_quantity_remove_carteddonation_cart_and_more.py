# Generated by Django 5.0.3 on 2024-03-18 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_connect_app', '0005_carteddonation_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='carteddonation',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='donation',
        ),
        migrations.AddField(
            model_name='carteddonation',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food_connect_app.order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='donations',
            field=models.ManyToManyField(through='food_connect_app.CartedDonation', to='food_connect_app.donation'),
        ),
    ]