from django.contrib.auth import get_user_model, login
from rest_framework import generics as api_generic_views, permissions, status
from rest_framework import views as api_views
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from auth_app.serializers import CreateUserSerializer

UserModel = get_user_model()


class RegisterView(api_generic_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Set token in cookies
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.set_cookie(key='auth_token', value=token.key, httponly=True)  # You can customize cookie options

        # Perform automatic login
        login(request, user)

        return response


class LoginView(views.ObtainAuthToken):
    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_admin': user.is_staff,
        })


class LogoutView(api_views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    @staticmethod
    def __perform_logout(request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'User logged out',
        })

    def get(self, request):
        return self.__perform_logout(request)

    def post(self, request):
        return self.__perform_logout(request)



