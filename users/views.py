from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from common.helper import encode_token , create_response , social_auth_token , decode_token
from rest_framework.response import Response
from common.enums import Message
from .models import User, UserTemplate
from django.utils import timezone
from .serializer import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer
from common.baselayer.baseAuth import UserAuthentication


class UserAuthView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    model = User

    def login(self, request):
        try:
            serialized_data = UserLoginSerializer(data=request.data)
            if serialized_data.is_valid():
                user = self.model.objects.filter(email=serialized_data.validated_data.get('email'))
                if user:
                    if not user[0].check_password(serialized_data.data.get("password")):
                        return Response(create_response(True, Message.incorrect_password.value, []))
                    data = serialized_data.data
                    data.pop('password')
                    data['token'] = encode_token(user[0])
                    data['name'] = user[0].first_name
                    user[0].last_login = timezone.now()
                    user[0].login_token = data['token']
                    user[0].save()
                    return Response(create_response(False, Message.success.value, data))

            return Response(create_response(True, Message.user_not_exists.value, []))

        except Exception as e:
            print(e)
            return Response(create_response(True, Message.server_error.value, []))

    def signup(self, request):
        try:
            if self.model.objects.filter(email=request.data.get("email")).exists():
                return Response(create_response(True, Message.user_exists.value, []))

            serialized_data = UserSignupSerializer(data=request.data)

            if serialized_data.is_valid():
                user = serialized_data.save()
                return Response(create_response(False, Message.account_created.value, serialized_data.data))
            return Response(create_response(True, Message.try_with_correct_data.value, data=[]))

        except Exception as e:
            print(e)
            return Response(create_response(True, Message.server_error.value, data=[]))


class TemplateView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = UserTemplate

    def select_template(self, request):
        try:
            if not request.data.get("template_type"):
                return Response(create_response(True, Message.try_with_correct_data.value, []))
            self.model.objects.create(
                user = request.user,
                template_type = request.data.get("template_type")
            )

        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))


class ProfileView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = User
    serializer_class = UserProfileSerializer

    def get_profile(self, request):
        try:
            return Response(create_response(False, Message.success.value, self.serializer_class(request.user,
                                                                                               many=True).data))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def update_profile(self, request):
        try:
            serializer = self.serializer_class(request.user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))