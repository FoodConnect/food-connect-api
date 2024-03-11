# signals.py or apps.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Donor, Charity, UserRole

# signal handler function 'create-profile'
@receiver(post_save, sender=User) #signal called when a user is saved
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == UserRole.DONOR.value:  
            Donor.objects.create(user=instance)
        elif instance.role == UserRole.CHARITY.value:  
            Charity.objects.create(user=instance)
