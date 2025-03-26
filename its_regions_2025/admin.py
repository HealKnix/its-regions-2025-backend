from django.contrib import admin

import its_regions_2025.models as models

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ObjectAdmin(admin.ModelAdmin):
    list_display = ["name"]


class StatusAdmin(admin.ModelAdmin):
    list_display = ["name"]


class PriorityAdmin(admin.ModelAdmin):
    list_display = ["name"]


class TypeQualityAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Object, ObjectAdmin)
admin.site.register(models.Status, StatusAdmin)
admin.site.register(models.Priority, PriorityAdmin)
admin.site.register(models.TypeQuality, TypeQualityAdmin)
