from rest_framework.permissions import BasePermission


# Классы разрешений для проверки владельца
class IsOwner(BasePermission):
    """
    Разрешение, позволяющее только владельцам объекта или администраторам
    выполнять действия над объектом.
    """

    def has_object_permission(self, request, view, obj):
        # Администраторы имеют полный доступ
        if request.user.is_superuser:
            return True

        # Проверяем есть ли у объекта поле user или user_id
        if hasattr(obj, "user_id"):
            return obj.user_id == request.user.id
        elif hasattr(obj, "user"):
            return obj.user == request.user

        # Для случаев, когда нет прямого поля владельца, но есть связь
        # Для задач проверяем создателя
        if hasattr(obj, "creator"):
            return obj.creator == request.user
        if hasattr(obj, "executor"):
            return obj.executor == request.user

        return False
