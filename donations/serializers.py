from rest_framework import serializers
from .models import Donation, Category, DonationCategory

class DonationSerializer(serializers.ModelSerializer):
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