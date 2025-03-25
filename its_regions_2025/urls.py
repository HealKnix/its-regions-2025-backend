from django.urls import path, include
from rest_framework.routers import DefaultRouter

import its_regions_2025.views as views

router = DefaultRouter()
router.register(r"type_object", views.TypeObjectViewSet, basename="type_object")
router.register(r"object", views.ObjectViewSet, basename="object")
router.register(r"priority", views.PriorityViewSet, basename="priority")
router.register(r"status", views.StatusViewSet, basename="status")
router.register(r"task", views.TaskViewSet, basename="task")
router.register(r"type_breaking", views.TypeBreakingViewSet, basename="type_breaking")
router.register(r"type_quality", views.TypeQualityViewSet, basename="type_quality")
router.register(r"notifications", views.NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
]
