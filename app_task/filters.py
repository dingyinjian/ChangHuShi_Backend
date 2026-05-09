import django_filters
from django_filters import rest_framework as filters

from app_task.models import Task


class TaskFilter(filters.FilterSet):
    start_time_after = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    start_time_before = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="lte")
    end_time_after = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="gte")
    end_time_before = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["owner", "service_object", "report_status"]
