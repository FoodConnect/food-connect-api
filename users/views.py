from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView

from .models import User, Charity, Donor

from .serializers import UserSerializer, CharitySerializer, DonorSerializer

from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()

        user_data = response.data.get('user', {})
        user_data['role'] = self.user.role  # Add role attribute to user data

        response.data['user'] = user_data

        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CharityViewSet(viewsets.ModelViewSet):
    queryset = Charity.objects.select_related('user').all()
    serializer_class = CharitySerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.select_related('user').all()
    serializer_class = DonorSerializer