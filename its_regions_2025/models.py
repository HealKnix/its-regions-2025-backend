from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        # Проверка на уникальность email
        if self.model.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        # Проверка на уникальность username
        if self.model.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Почта"), unique=True)
    password = models.CharField(_("Пароль"), max_length=128)
    username = models.CharField(_("Логин"), max_length=150)
    first_name = models.CharField(_("Имя"), max_length=30)
    last_name = models.CharField(_("Фамилия"), max_length=30)
    patronymic = models.CharField(_("Отчество"), max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "patronymic"]

    def __str__(self):
        return self.email


class TypeObject(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Object(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(TypeObject, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)


class Priority(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)


class TypeQuality(models.Model):
    name = models.CharField(max_length=255, unique=True)


class TypeBreaking(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    executor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks_executed"
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks_created"
    )
    quality_report = models.ForeignKey(TypeQuality, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    text_report = models.TextField(blank=True, null=True)
    description = models.TextField()
    diagnostic_data = models.BooleanField(default=False)
    result = models.BooleanField(default=False)
    was_done = models.BooleanField(default=False)
    name_component = models.BooleanField(default=False)
    type_breaking = models.ForeignKey(TypeBreaking, on_delete=models.CASCADE)


class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=65)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
