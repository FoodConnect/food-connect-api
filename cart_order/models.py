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
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[(status.value, status.name.title()) for status in CartStatus])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartedDonation(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    donation_receipt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
