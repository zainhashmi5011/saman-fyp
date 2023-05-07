from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from common.helper import encode_token , create_response , social_auth_token , decode_token
from rest_framework.response import Response
from common.enums import Message
from .models import (
    User, UserTemplate, Education, Awards, Achievements, AcademicExp, )
from django.utils import timezone
from .serializer import *
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
                    try:
                        user_template = user[0].user_template.all().last().template_type

                    except:
                        user_template = "1"

                    data = serialized_data.data
                    data.pop('password')
                    data['token'] = encode_token(user[0])
                    data['name'] = user[0].first_name

                    data['template_type'] =  user_template

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
    authentication_classes = []
    permission_classes = []
    model = UserTemplate

    def select_template(self, request):
        try:
            if not request.data.get("template_type"):
                return Response(create_response(True, Message.try_with_correct_data.value, []))
            self.model.objects.create(
                user_id = request.data.get("user_id"),
                template_type = request.data.get("template_type")
            )
            return Response(create_response(False, Message.success.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))


class ProfileView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = User
    serializer_class = UserProfileSerializer

    def get_profile(self, request):
        try:
            serialized_data = self.serializer_class(request.user, many=False).data
            serialized_data['template_type'] = request.user.user_template.all().last().template_type
            return Response(create_response(False, Message.success.value, []))
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



class EducationView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Education
    serializer_class = EducationSerializer

    def create_education(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_education(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))



class AwardsView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Awards
    serializer_class = AwardsSerializer

    def create_awards(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_awards(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))



class AcedemicView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = AcademicExp
    serializer_class = AcedemicSerializer

    def create_academic(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_academic(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))


class AchievementView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Achievements
    serializer_class = AchievmentSerializer

    def create_achievement(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_achievement(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))



class BlogView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Blogs
    serializer_class = BlogSerializer

    def create_blog(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_blog(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))


class JobView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Jobs
    serializer_class = JobSerializer

    def create_job(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_job(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

class FundingView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Funding
    serializer_class = FundingSerializer

    def create_funding(self, request):
        try:
            request.data['user'] = request.user.id
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_funding(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True)
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))



class PicturesView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Pictures
    serializer_class = PictureSerializer

    def create_pictures(self, request):
        try:
            serializer = self.serializer_class(data = request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_pictures(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True, context={"request": request})
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))



class CollaborationView(ModelViewSet):
    authentication_classes = [UserAuthentication]
    permission_classes = []
    model = Collaborations
    serializer_class = CollaborationSerializer

    def create_collaboration(self, request):
        try:
            serializer = self.serializer_class(data = request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.try_with_correct_data.value, []))
        except Exception as e:
            return Response(create_response(True, Message.server_error.value, []))

    def get_collaboration(self, request):
        try:
            queryset = self.model.objects.filter(user_id = request.user.id)
            if queryset.exists():
                serializer = self.serializer_class(queryset, many=True, context={"request": request})
                return Response(create_response(False, Message.success.value, serializer.data))
            return Response(create_response(True, Message.record_not_found.value, []))
        except Exception as e:
            print(e)
            return Response(create_response(True, Message.server_error.value, []))