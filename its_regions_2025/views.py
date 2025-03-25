from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema_view, extend_schema

import its_regions_2025.serializers as serializers
import its_regions_2025.permissions as permissions
import its_regions_2025.models as models
import its_regions_2025.docs as docs

# Create your views here.


class RegistrationViewSet(APIView):
    """API для регистрации пользователя."""

    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer

    @extend_schema(
        request=serializers.UserSerializer, responses={201: serializers.UserSerializer}
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.create_user(**serializer.validated_data)
            token, _ = Token.objects.get_or_create(user=user)

            user = serializers.UserSerializer(user).data

            return Response(
                {**user, "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedAPIView(APIView):
    """API для проверки аутентификации пользователя по токену."""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AuthenticatedSerializer

    def post(self, request, *args, **kwargs) -> Response:
        token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]

        try:
            token_obj = Token.objects.get(key=token)
            user = serializers.UserSerializer(token_obj.user).data
            return Response(
                user,
                status=status.HTTP_200_OK,
            )
        except (Token.DoesNotExist, IndexError) as e:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LoginViewSet(APIView):
    """API для аутентификации пользователя."""

    queryset = models.User.objects.all()
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            csrftoken = get_token(request)
            sessionid = request.session.session_key

            user.last_login = datetime.now()

            user = serializers.UserSerializer(user).data

            response = Response(
                {**user, "token": token.key},
                status=status.HTTP_200_OK,
            )

            response.set_cookie("sessionid", sessionid)
            response.set_cookie("csrftoken", csrftoken)

            return response
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutViewSet(APIView):
    """API для выхода пользователя из системы."""

    queryset = models.User.objects.all()
    serializer_class = serializers.LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]
        Token.objects.filter(key=token).delete()
        logout(request)
        return Response(
            {"detail": "Successfully logged out"}, status=status.HTTP_200_OK
        )


@extend_schema_view(**docs.TypeObjectDocumentation())
class TypeObjectViewSet(viewsets.ModelViewSet):
    queryset = models.TypeObject.objects.all()
    serializer_class = serializers.TypeObjectSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@extend_schema_view(**docs.ObjectDocumentation())
class ObjectViewSet(viewsets.ModelViewSet):
    queryset = models.Object.objects.all()
    serializer_class = serializers.ObjectSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@extend_schema_view(**docs.PriorityDocumentation())
class PriorityViewSet(viewsets.ModelViewSet):
    queryset = models.Priority.objects.all()
    serializer_class = serializers.PrioritySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@extend_schema_view(**docs.StatusDocumentation())
class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@extend_schema_view(**docs.TaskDocumentation())
class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]
    http_method_names = ["get", "patch"]


@extend_schema_view(**docs.TypeBreakingDocumentation())
class TypeBreakingViewSet(viewsets.ModelViewSet):
    queryset = models.TypeBreaking.objects.all()
    serializer_class = serializers.TypeBreakingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@extend_schema_view(**docs.TypeQualityDocumentation())
class TypeQualityViewSet(viewsets.ModelViewSet):
    queryset = models.TypeQuality.objects.all()
    serializer_class = serializers.TypeQualitySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@extend_schema_view(**docs.NotificationDocumentation())
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]
    http_method_names = ["get", "post"]
