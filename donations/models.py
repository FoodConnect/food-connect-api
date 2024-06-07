from django.db import models
from users.models import Donor, UserRole
from enum import Enum

class DonationCategory(Enum):
    PRODUCE = 'produce'
    CANNED = 'canned'
    DAIRY = 'dairy'
    DRY = 'dry'
    OTHER = 'other'

class Donation(models.Model):
    id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image_data = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[(category.value, category.name) for category in DonationCategory])
    total_inventory = models.IntegerField()
    claimed_inventory = models.IntegerField(default=0)
    remaining_inventory = models.IntegerField()
    pick_up_deadline = models.DateTimeField()
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_donor(self):
        if self.donor.user.role == UserRole.DONOR.value:
            return self.donor.user
        return None


