from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema_view, extend_schema

import its_regions_2025.serializers as serializers
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
            user = models.User.objects.create_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data.get("first_name", ""),
                last_name=serializer.validated_data.get("last_name", ""),
                patronymic=serializer.validated_data.get("patronymic", ""),
            )
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "patronymic": user.patronymic,
                        "is_staff": user.is_staff,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedAPIView(APIView):
    """API для проверки аутентификации пользователя по токену."""

    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, *args, **kwargs) -> Response:
        token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]

        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "patronymic": user.patronymic,
                        "is_staff": user.is_staff,
                        "email": user.email,
                    }
                },
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

            response = Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "patronymic": user.patronymic,
                        "is_staff": user.is_staff,
                        "email": user.email,
                    },
                },
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
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(**docs.ObjectDocumentation())
class ObjectViewSet(viewsets.ModelViewSet):
    queryset = models.Object.objects.all()
    serializer_class = serializers.ObjectSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(**docs.PriorityDocumentation())
class PriorityViewSet(viewsets.ModelViewSet):
    queryset = models.Priority.objects.all()
    serializer_class = serializers.PrioritySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(**docs.StatusDocumentation())
class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(**docs.TaskDocumentation())
class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(**docs.TypeBreakingDocumentation())
class TypeBreakingViewSet(viewsets.ModelViewSet):
    queryset = models.TypeBreaking.objects.all()
    serializer_class = serializers.TypeBreakingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(**docs.TypeQualityDocumentation())
class TypeQualityViewSet(viewsets.ModelViewSet):
    queryset = models.TypeQuality.objects.all()
    serializer_class = serializers.TypeQualitySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
