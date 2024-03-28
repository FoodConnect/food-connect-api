from django.contrib import admin

from .models import User, Charity, Donor

admin.site.register(User)
admin.site.register(Charity)
admin.site.register(Donor)
