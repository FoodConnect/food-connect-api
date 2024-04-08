from rest_framework import serializers
from .models import User, Charity, Donor, UserRole
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'id']

# Custom Serializer for User registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomUserRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=10)
    role = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True, max_length=10)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['name'] = self.validated_data.get('name', '')
        data_dict['role'] = self.validated_data.get('role', '')
        data_dict['phone_number'] = self.validated_data.get('phone_number', '')
        return data_dict

    
class CustomUserDetailsSerializer(UserDetailsSerializer):
   class Meta(UserDetailsSerializer.Meta):
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + \
            ('role',)

class CharitySerializer(serializers.ModelSerializer):
  class Meta:
      model = Charity
      fields = '__all__'

class DonorSerializer(serializers.ModelSerializer):
  class Meta:
      model = Donor
      fields = '__all__'