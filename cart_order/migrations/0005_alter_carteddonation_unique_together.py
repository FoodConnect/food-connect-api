# Generated by Django 5.0.4 on 2024-05-10 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart_order', '0004_alter_order_donation_receipt'),
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carteddonation',
            unique_together={('cart', 'donation')},
        ),
    ]
