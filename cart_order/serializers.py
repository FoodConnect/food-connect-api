from rest_framework import serializers
from .models import Cart, CartedDonation, Order, OrderedDonation

from users.serializers import DonorSerializer
from donations.serializers import DonationSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class CartedDonationSerializer(serializers.ModelSerializer):
    donation = DonationSerializer()
    donor = serializers.SerializerMethodField()

    class Meta:
        model = CartedDonation
        fields = '__all__'

    def get_donor(self, obj):
        return DonorSerializer(obj.donation.donor).data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class OrderedDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDonation
        fields = '__all__'