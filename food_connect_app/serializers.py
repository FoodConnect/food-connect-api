from rest_framework import serializers
from .models import User, Charity, Donor, Donation, Cart, CartedDonation, Order, Category, DonationCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class CharitySerializer(serializers.ModelSerializer):
  class Meta:
      model = Charity
      fields = '__all__'

class DonorSerializer(serializers.ModelSerializer):
  
  class Meta:
      model = Donor
      fields = '__all__'

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class CartedDonationSerializer(serializers.ModelSerializer):
    donation = DonationSerializer() # Nested serializer for Donation
    class Meta:
        model = CartedDonation
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class OrderSerializer(serializers.ModelSerializer):
    donations = DonationSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

    def create(self, validated_data):
        carted_donations_data = validated_data.pop('carted_donations', [])  # Extract carted donations data
        order = Order.objects.create(**validated_data)  # Create the order

        for carted_donation_data in carted_donations_data:
            donation_data = carted_donation_data.pop('donation')  # Extract donation data
            donation = Donation.objects.create(**donation_data)  # Create the associated donation
            CartedDonation.objects.create(order=order, donation=donation, **carted_donation_data)  # Create the CartedDonation

        return order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class DonationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCategory
        fields = '__all__'
