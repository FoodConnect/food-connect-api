from rest_framework import serializers

from users.models import Donor
from users.serializers import DonorDonationsSerializer, DonorSerializer, UserSerializer
from .models import Donation, Category, DonationCategory

class DonationSerializer(serializers.ModelSerializer):
    donor = DonorDonationsSerializer(read_only=True)
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class DonationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCategory
        fields = '__all__'