from django.contrib import admin
from .models import User, Charity, Donor, Donation, Cart, CartedDonation, Order, Category, DonationCategory, ClaimedInventory

admin.site.register(User)
admin.site.register(Charity)
admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Cart)
admin.site.register(CartedDonation)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(DonationCategory)
admin.site.register(ClaimedInventory)