import json
import logging

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.viewset import CustomModelViewSet
from app_sop.models import Sop
from app_sop.serializers import SopSerializer, SopCreateUpdateSerializer
from app_sop.tasks import sop_analyze_task

logger = logging.getLogger(__name__)


def _enqueue_sop_analysis(sop_id: int) -> None:
    """
    优先异步投递 Celery；若 broker 不可用（如 WinError 10061），则同步 apply，避免上传接口失败。
    """
    try:
        sop_analyze_task.delay(sop_id)
    except Exception as exc:  # noqa: BLE001 — 需兜底多种 broker 异常类型
        msg = str(exc).lower()
        winerr = getattr(exc, "winerror", None)
        errno = getattr(exc, "errno", None)
        broker_like = (
            winerr == 10061
            or errno in (61, 111)
            or "10061" in msg
            or "actively refused" in msg
            or "connection refused" in msg
            or "operationalerror" in type(exc).__name__.lower()
        )
        if broker_like:
            logger.warning("Celery broker unavailable, run SOP analysis synchronously: %s", exc)
            sop_analyze_task.apply(args=[sop_id])
        else:
            raise


# Create your views here.
class SopViewSet(CustomModelViewSet):
    queryset = Sop.objects.all()
    serializer_class = SopSerializer
    create_serializer_class = SopCreateUpdateSerializer
    update_serializer_class = SopCreateUpdateSerializer
    search_fields = ["title", "content_html"]
    ordering = ["-create_datetime"]
    @action(methods=["post"],detail=True,url_path="upload-video")
    def upload_video(self, request, pk=None):
        obj = self.get_object()
        f = request.FILES.get("file")
        if not f:
            return Response({"code":400,"msg":"缺少file"},status=400)
        save_path =f"sop_video/{obj.id}/{f.name}"
        path = default_storage.save(save_path,ContentFile(f.read()))
        obj.video_url = default_storage.url(path)
        obj.analysis_status = "pending"
        obj.analysis_error = ""
        obj.save(update_fields=["video_url", "analysis_status", "analysis_error","update_datetime"])

        _enqueue_sop_analysis(obj.id)
        return Response({"code":200,"msg":"上传成功,已开始分析"})
    @action(methods=["post"],detail=True,url_path="apply-analysis")
    def apply_analysis(self, request, pk=None):
        obj = self.get_object()
        raw =request.data.get("analysis_result")
        if raw is None:
            return Response({"code":400,"msg":"缺少analysis_result"},status=400)
        try:
            parsed = json.loads(raw) if isinstance(raw,str) else raw
        except Exception as e:
            return Response({"code":400,"msg":f"analysis_result格式错误: {str(e)}"},status=400)
        obj.analysis_result = parsed
        obj.analysis_status = "success"
        obj.analysis_error = ""
        obj.save(update_fields=["analysis_result", "analysis_status", "analysis_error","update_datetime"])
        return Response({"code":200,"msg":"保存成功"})