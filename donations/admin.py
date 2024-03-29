from django.contrib import admin

from .models import Donation, Category, DonationCategory

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(DonationCategory)
