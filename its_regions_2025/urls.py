from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TypeObjectViewSet,
    ObjectViewSet,
    PriorityViewSet,
    StatusViewSet,
    TaskViewSet,
    TypeBreakingViewSet,
    TypeQualityViewSet,
)

router = DefaultRouter()
router.register(r"type_object", TypeObjectViewSet, basename="type_object")
router.register(r"object", ObjectViewSet, basename="object")
router.register(r"priority", PriorityViewSet, basename="priority")
router.register(r"status", StatusViewSet, basename="status")
router.register(r"task", TaskViewSet, basename="task")
router.register(r"type_breaking", TypeBreakingViewSet, basename="type_breaking")
router.register(r"type_quality", TypeQualityViewSet, basename="type_quality")

urlpatterns = [
    path("", include(router.urls)),
]
