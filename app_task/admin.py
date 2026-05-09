from django.contrib import admin

from app_task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "task_name", "owner", "service_object", "start_time", "end_time", "report_status")
    search_fields = ("task_name",)
