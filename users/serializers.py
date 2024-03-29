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

class CharitySerializer(serializers.ModelSerializer):
  class Meta:
      model = Charity
      fields = '__all__'

class DonorSerializer(serializers.ModelSerializer):
  class Meta:
      model = Donor
      fields = '__all__'