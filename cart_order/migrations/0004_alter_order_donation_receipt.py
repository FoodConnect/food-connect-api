# Generated by Django 5.0.4 on 2024-04-08 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_order', '0003_order_donation_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='donation_receipt',
            field=models.TextField(),
        ),
    ]
