from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)


class TypeObjectDocumentation:
    def __new__(cls):
        tag = "Типы объекта"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех типов объектов"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор типа объекта",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный тип объекта по идентификатору",
            ),
            "create": extend_schema(
                tags=[tag], description="Создать новый тип объекта"
            ),
            "destroy": extend_schema(
                tags=[tag], description="Удалить тип объекта по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующий тип объекта по идентификатору",
            ),
        }


class ObjectDocumentation:
    def __new__(cls):
        tag = "Объекты"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех объектов"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор объекта",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный объекта по идентификатору",
            ),
            "create": extend_schema(tags=[tag], description="Создать новый объект"),
            "destroy": extend_schema(
                tags=[tag], description="Удалить объект по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующий объект по идентификатору",
            ),
        }


class PriorityDocumentation:
    def __new__(cls):
        tag = "Приоритеты"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех приоритетов"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор приоритета",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный приоритет по идентификатору",
            ),
            "create": extend_schema(tags=[tag], description="Создать новый приоритет"),
            "destroy": extend_schema(
                tags=[tag], description="Удалить приоритет по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующий приоритет по идентификатору",
            ),
        }


class StatusDocumentation:
    def __new__(cls):
        tag = "Статусы"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех статусов"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор статуса",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный статус по идентификатору",
            ),
            "create": extend_schema(tags=[tag], description="Создать новый статус"),
            "destroy": extend_schema(
                tags=[tag], description="Удалить статус по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующий статус по идентификатору",
            ),
        }


class TypeQualityDocumentation:
    def __new__(cls):
        tag = "Типы качества"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех типов качества"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор типа качества",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный тип качества по идентификатору",
            ),
            "create": extend_schema(
                tags=[tag], description="Создать новый тип качества"
            ),
            "destroy": extend_schema(
                tags=[tag], description="Удалить тип качества по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующий тип качества по идентификатору",
            ),
        }


class TypeBreakingDocumentation:
    def __new__(cls):
        tag = "Типы поломки"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех типов поломки"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор типа поломки",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный тип поломки по идентификатору",
            ),
            "create": extend_schema(
                tags=[tag], description="Создать новый тип поломки"
            ),
            "destroy": extend_schema(
                tags=[tag], description="Удалить тип поломки по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующий тип поломки по идентификатору",
            ),
        }


class TaskDocumentation:
    def __new__(cls):
        tag = "Задачи"
        return {
            "list": extend_schema(tags=[tag], description="Получить список всех задач"),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор задачи",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретную задачу по идентификатору",
            ),
            "create": extend_schema(tags=[tag], description="Создать новую задачу"),
            "destroy": extend_schema(
                tags=[tag], description="Удалить задачу по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить существующую задачу по идентификатору",
            ),
        }


class NotificationDocumentation:
    def __new__(cls):
        tag = "Уведомления"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех уведомлений"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор уведомления",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретное уведомление по идентификатору",
            ),
            "create": extend_schema(
                tags=[tag], description="Создать новое уведомление"
            ),
            "destroy": extend_schema(
                tags=[tag], description="Удалить уведомление по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить уведомление по идентификатору",
            ),
        }


class UserDocumentation:
    def __new__(cls):
        tag = "Пользователи"
        return {
            "list": extend_schema(
                tags=[tag], description="Получить список всех пользователей"
            ),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор пользователя",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретное уведомление по идентификатору",
            ),
            "create": extend_schema(
                tags=[tag], description="Создать новое уведомление"
            ),
            "destroy": extend_schema(
                tags=[tag], description="Удалить уведомление по идентификатору"
            ),
            "partial_update": extend_schema(
                tags=[tag],
                description="Частично обновить уведомление по идентификатору",
            ),
        }


class RecommendationDocumentation:
    def __new__(cls):
        tag = "Рекомендации"
        return {
            "list": extend_schema(tags=[tag], description="Получить список всех задач"),
            "retrieve": extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name="id",
                        description="Идентификатор задачи",
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретную задачу по идентификатору",
            ),
        }
