from django.db import models
from enum import Enum
from users.models import Charity
from donations.models import Donation

class CartStatus(Enum):
    CARTED = 'carted'
    ORDERED = 'ordered'

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[(status.value, status.name.title()) for status in CartStatus], default=CartStatus.CARTED.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartedDonation(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = ('cart', 'donation')

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    donation_receipt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderedDonation(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='ordered_donations', on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)