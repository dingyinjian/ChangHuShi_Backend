from rest_framework.decorators import action
from rest_framework.response import Response

from app_task.filters import TaskFilter
from app_task.models import Task
from app_task.serializers import TaskApplyReportSerializer, TaskSerializer
from utils.json_response import ErrorResponse
from utils.viewset import CustomModelViewSet


class TaskViewSet(CustomModelViewSet):
    queryset = Task.objects.select_related("owner", "service_object").prefetch_related("sop_items").all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    search_fields = ["task_name", "service_report"]
    ordering = ["-update_datetime"]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.report_status == "done":
            return ErrorResponse(msg="报告已生成，不允许修改任务", code=400)
        return super().update(request, *args, **kwargs)

    @action(methods=["post"], detail=True, url_path="apply-report")
    def apply_report(self, request, pk=None):
        """供 YIBAOJUWEB 等外部系统按任务 ID 回写服务报告与分数（JWT 鉴权）。"""
        obj = self.get_object()
        ser = TaskApplyReportSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 400, "msg": str(ser.errors)}, status=400)

        obj.service_report = ser.validated_data["service_report"]
        score = ser.validated_data.get("service_score")
        if score is not None:
            obj.service_score = score
        obj.report_status = "done"
        if request.user and str(request.user) != "AnonymousUser":
            obj.modifier = str(getattr(request.user, "id", "") or "")
        obj.save(
            update_fields=[
                "service_report",
                "service_score",
                "report_status",
                "modifier",
                "update_datetime",
            ]
        )
        return Response({"code": 200, "msg": "保存成功"})
