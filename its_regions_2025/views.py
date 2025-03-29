from datetime import datetime

import uuid
from django.http import HttpResponse
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

from model.recomendation import demonstrate_model

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

            user_is_admin = models.User.objects.filter(
                email=user["email"], is_superuser=True
            ).exists()

            return Response(
                {**user, "token": token.key, "is_admin": user_is_admin},
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

            user_is_admin = models.User.objects.filter(
                email=user["email"], is_superuser=True
            ).exists()

            return Response(
                {**user, "is_admin": user_is_admin},
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

            user_is_admin = models.User.objects.filter(
                email=user["email"], is_superuser=True
            ).exists()

            response = Response(
                {**user, "token": token.key, "is_admin": user_is_admin},
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


class AllDataViewSet(APIView):
    """API для выхода пользователя из системы."""

    queryset = None
    serializer_class = serializers.LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        user = self.request.user

        # print("==============================")
        # print(request)
        # print("==============================")

        # serializedTasks = serializers.TaskSerializer(request.data, many=True).data

        # # Проверка на коллизии между полученными задачами и задачами в БД
        # db_tasks = models.Task.objects.all()
        # task_collisions = []

        # for task_data in serializedTasks:
        #     task_id = task_data.get("id")
        #     if task_id:
        #         db_task = db_tasks.filter(id=task_id).first()
        #         if db_task:
        #             # Проверяем, есть ли различия между полученной задачей и задачей в БД
        #             serialized_db_task = serializers.TaskSerializer(db_task).data
        #             if serialized_db_task != task_data:
        #                 task_collisions.append(
        #                     {
        #                         "task_id": task_id,
        #                         "client_data": task_data,
        #                         "server_data": serialized_db_task,
        #                     }
        #                 )

        tasks = models.Task.objects.filter(executor=user)

        if user.is_superuser:
            tasks = models.Task.objects.all()

        return Response(
            {
                "users": serializers.UserSerializer(
                    models.User.objects.all(), many=True
                ).data,
                "type_objects": serializers.TypeObjectSerializer(
                    models.TypeObject.objects.all(), many=True
                ).data,
                "objects": serializers.ObjectSerializer(
                    models.Object.objects.all(), many=True
                ).data,
                "priorities": serializers.PrioritySerializer(
                    models.Priority.objects.all(), many=True
                ).data,
                "statuses": serializers.StatusSerializer(
                    models.Status.objects.all(), many=True
                ).data,
                "tasks": serializers.TaskSerializer(tasks, many=True).data,
                "type_breakings": serializers.TypeBreakingSerializer(
                    models.TypeBreaking.objects.all(), many=True
                ).data,
                "type_qualities": serializers.TypeQualitySerializer(
                    models.TypeQuality.objects.all(), many=True
                ).data,
                "notifications": serializers.NotificationSerializer(
                    models.Notification.objects.filter(user=self.request.user),
                    many=True,
                ).data,
            }
        )


@extend_schema_view(**docs.RecommendationDocumentation())
class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        return Response([])

    def retrieve(self, request, *args, **kwargs):
        task = models.Task.objects.filter(id=kwargs["pk"]).first()
        object = task.object
        type_object = object.type
        return Response(
            demonstrate_model(type_object.name, task.description, task.type_breaking)
        )


def index(request):
    return HttpResponse("", status=200)


@extend_schema_view(**docs.UserDocumentation())
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


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
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Task.objects.all()
        else:
            return models.Task.objects.filter(executor=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        arr = []

        for task in serializer.data:
            if task["status"] == 2:
                task_inner = models.Task.objects.filter(status=5).first()
                object = task_inner.object
                type_object = object.type
                task = {
                    **task,
                    "recommendation": demonstrate_model(
                        type_object.name,
                        task_inner.description,
                        task_inner.type_breaking,
                    ),
                }
                arr.append(task)
            else:
                arr.append(task)

        return Response(arr, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        models.Notification.objects.create(
            user=serializer.data.get("executor"),
            task=serializer.data.get("id"),
            title="Новая задача",
            message="Пользователь создал новую задачу",
        )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        instance = self.get_object()
        old_values = {
            field.name: getattr(instance, field.name) for field in instance._meta.fields
        }
        updated_task = self.update(request, *args, **kwargs)
        updated_instance = self.get_object()

        new_values = {
            field.name: getattr(updated_instance, field.name)
            for field in updated_instance._meta.fields
        }

        print(old_values)

        old_uuid = str(uuid.uuid4())
        for key in request.data:
            models.TaskVersion.objects.create(
                version_uuid=old_uuid,
                task=updated_instance,
                user=updated_instance.executor,
                field=key,
                value=old_values[key],
            )

        new_uuid = str(uuid.uuid4())
        for key in request.data:
            models.TaskVersion.objects.create(
                version_uuid=new_uuid,
                task=updated_instance,
                user=updated_instance.executor,
                field=key,
                value=new_values[key],
            )

        return updated_task


@extend_schema_view(**docs.TaskDocumentation())
class TaskVersionViewSet(viewsets.ModelViewSet):
    queryset = models.TaskVersion.objects.all()
    serializer_class = serializers.TaskVersionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


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

    def get_queryset(self):
        return models.Notification.objects.filter(user=self.request.user)
