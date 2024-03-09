from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, exceptions
from .models import User

class GoogleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None
        
        try:
            id_info = verify_oauth2_token(token, requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)
            user_id = id_info['sub']
            user, created = User.objects.get_or_create(email=id_info['email'], defaults={'email': id_info['email']})
            return (user, None)
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except KeyError:
            raise exceptions.AuthenticationFailed('Invalid payload')