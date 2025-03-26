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
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "patronymic"]

    def __str__(self):
        return self.email


class TypeObject(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    type = models.ForeignKey(TypeObject, on_delete=models.CASCADE, verbose_name="Тип")
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8, verbose_name="Долгота"
    )
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8, verbose_name="Широта"
    )
    mark_description = models.CharField(
        max_length=255, null=True, verbose_name="Описание"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объекты"
        verbose_name_plural = "Объекты"


class Priority(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Приоритеты"
        verbose_name_plural = "Приоритеты"


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статусы"
        verbose_name_plural = "Статусы"


class TypeQuality(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Качество"
        verbose_name_plural = "Качество"


class TypeBreaking(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, verbose_name="Приоритет"
    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="Объект")
    executor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks_executed",
        verbose_name="Исполнитель",
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks_created",
        verbose_name="Создатель",
    )
    quality_report = models.ForeignKey(
        TypeQuality,
        on_delete=models.CASCADE,
        null=True,
        default=4,
        verbose_name="Качество отчета",
    )
    start_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата начала")
    deadline = models.DateTimeField(
        blank=True, null=True, verbose_name="Срок выполнения", default=None
    )
    text_report = models.TextField(
        blank=True, null=True, verbose_name="Текстовый отчет"
    )
    description = models.TextField(verbose_name="Описание")
    diagnostic_data = models.BooleanField(
        default=False, verbose_name="Диагностические данные"
    )
    result = models.BooleanField(default=False, verbose_name="Результат")
    was_done = models.BooleanField(default=False, verbose_name="Выполнено")
    name_component = models.BooleanField(
        default=False, verbose_name="Название компонента"
    )
    type_breaking = models.ForeignKey(
        TypeBreaking, on_delete=models.CASCADE, verbose_name="Тип поломки"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задачи"
        verbose_name_plural = "Задачи"


class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Задача")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    title = models.CharField(max_length=65, verbose_name="Заголовок")
    message = models.CharField(max_length=255, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")

    def __str__(self):
        return self.title
