
from rest_framework.authentication import BaseAuthentication
from users.models import User
from rest_framework import exceptions
import jwt

class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        
        if ("Authorization") not in request.headers.keys():
            raise exceptions.AuthenticationFailed("Authorization Required")

        if not request.headers["Authorization"]:
            raise exceptions.AuthenticationFailed("USER TOKEN IS REQUIRED")

        token = request.headers["Authorization"].split(" ")[1]

        if not token:
            raise exceptions.AuthenticationFailed("prefix missing")

        try:
            payload = jwt.decode(token , "cancerclarity" , algorithms="HS256")

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("TOKEN EXPIRED")

        except jwt.InvalidTokenError:
            raise exceptions.NotAcceptable("INVALID TOKEN")

        user = User.objects.filter(email=payload["email"]).first()

        return (user, None)

