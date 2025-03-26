from django.urls import path, include
from rest_framework.routers import DefaultRouter

import its_regions_2025.views as views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(r"type_objects", views.TypeObjectViewSet, basename="type_objects")
router.register(r"objects", views.ObjectViewSet, basename="objects")
router.register(r"priorities", views.PriorityViewSet, basename="priorities")
router.register(r"statuses", views.StatusViewSet, basename="statuses")
router.register(r"tasks", views.TaskViewSet, basename="tasks")
router.register(r"type_breakings", views.TypeBreakingViewSet, basename="type_breakings")
router.register(r"type_qualities", views.TypeQualityViewSet, basename="type_qualities")
router.register(r"notifications", views.NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
]
