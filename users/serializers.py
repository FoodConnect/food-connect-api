from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User, Charity, Donor, UserRole

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

## Custom Serializer for User registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, attrs):
        role = attrs.get('role')
        business_name = attrs.get('business_name')
        ein_number = attrs.get('ein_number')

        if role == UserRole.CHARITY.value:
            if business_name:
                attrs['business_name'] = ''
            if ein_number:
                attrs['ein_number'] = ''
        else:
            if not business_name:
                raise serializers.ValidationError("Business name and EIN are required for donors.")
            if not ein_number:
                raise serializers.ValidationError("Business name and EIN are required for donors.")

        return attrs
    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ('role',)

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
      model = Charity
      fields = '__all__'

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
      model = Donor
      fields = '__all__'

    
# Used for the Donations get request to serve up some details about the donor (in DonationsSerializer)
class DonorDonationsSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='user.business_name')
    email = serializers.EmailField(source='user.email')
    city = serializers.CharField(source='user.city')
    state = serializers.CharField(source='user.state')
    image_data = serializers.CharField(source='user.image_data')
    phone_number = serializers.CharField(source='user.phone_number')
    class Meta:
        model = Donor
        fields = ['user_id', 'business_name', 'email', 'city', 'state', 'image_data', 'phone_number']