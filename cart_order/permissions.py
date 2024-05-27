from rest_framework import permissions

class IsOrderOwnerOrDonationUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if hasattr(request.user, 'charity') and request.user.charity == obj.charity:
            return True
        
        for ordered_donation in obj.ordered_donations.all():
            if hasattr(ordered_donation.donation.donor, 'user') and request.user == ordered_donation.donation.donor.user:
                return True
        
        return False
