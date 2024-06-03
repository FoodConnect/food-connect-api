from rest_framework import serializers
from .models import Cart, CartedDonation, Order, OrderedDonation

from users.serializers import DonorSerializer, CharitySerializer, UserSerializer
from donations.serializers import DonationSerializer

class CartedDonationSerializer(serializers.ModelSerializer):
    donation = DonationSerializer()

    class Meta:
        model = CartedDonation
        fields = '__all__'

    def get_donor(self, obj):
        donation = obj.donation
        donor_user = donation.get_donor()
        if donor_user:
            return {
                'id': donor_user.id,
                'business_name': donor_user.business_name,
                'city': donor_user.city,
                'email': donor_user.email,
                'image_data': donor_user.image_data,
                'phone_number': donor_user.phone_number,
                'state': donor_user.state
            }
        return None

class CartSerializer(serializers.ModelSerializer):
    carted_donations = CartedDonationSerializer(many=True, source='carteddonation_set')

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

class OrderedDonationSerializer(serializers.ModelSerializer):
    donation = DonationSerializer()
    
    class Meta:
        model = OrderedDonation
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    charity = CharitySerializer()
    ordered_donations = OrderedDonationSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']
