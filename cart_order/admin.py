from django.contrib import admin

from .models import Cart, CartedDonation, Order

admin.site.register(Cart)
admin.site.register(CartedDonation)
admin.site.register(Order)
