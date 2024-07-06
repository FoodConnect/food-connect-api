from rest_framework import serializers

from users.models import Donor
from users.serializers import DonorDonationsSerializer, DonorSerializer, UserSerializer
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    donor = DonorDonationsSerializer(read_only=True)
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

