from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Donor, Charity, UserRole

# signal handler function 'create-profile'
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == UserRole.DONOR.value:
            Donor.objects.create(user=instance)
        elif instance.role == UserRole.CHARITY.value:
            Charity.objects.create(user=instance)


# @receiver(pre_save, sender=User)
# def create_profile(sender, instance, **kwargs):
#     # Check if the user is being created (new user) or updated (existing user)
#     if instance.pk is None:  # If primary key is None, it's a new user being created
#         if instance.role == UserRole.DONOR.value:
#             Donor.objects.create(user=instance)
#         elif instance.role == UserRole.CHARITY.value:
#             Charity.objects.create(user=instance)
#     else:  # Existing user being updated
#         # Add logic to handle updates if needed
#         pass