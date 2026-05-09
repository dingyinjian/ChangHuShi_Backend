import logging
from pathlib import Path
from celery import shared_task
from django.conf import settings
from app_sop.models import Sop
from app_sop.services.analyzer import analyze_video

logger = logging.getLogger(__name__)


def _resolve_local_video_path(video_url: str) -> str:
    if not video_url:
        return ""
    # 已是绝对本地路径时直接返回
    path = Path(video_url)
    if path.is_absolute():
        return str(path)
    # 把 /media/xxx 转为 MEDIA_ROOT/xxx
    media_url = settings.MEDIA_URL.rstrip("/") + "/"
    if video_url.startswith(media_url):
        relative = video_url[len(media_url):]
        return str(Path(settings.MEDIA_ROOT) / relative)
    return video_url


@shared_task(bind=True, autoretry_for=(ConnectionError, TimeoutError), retry_backoff=True, retry_kwargs={"max_retries": 2})
def sop_analyze_task(self, sop_id: int):
    sop = Sop.objects.get(id=sop_id)
    sop.analysis_status = "running"
    sop.analysis_error = ""
    sop.save(update_fields=["analysis_status", "analysis_error", "update_datetime"])
    try:
        local_video_path = _resolve_local_video_path(sop.video_url or "")
        result = analyze_video(local_video_path)
        sop.analysis_result = result
        sop.analysis_status = "success"
        sop.analysis_error = ""
        sop.save(update_fields=["analysis_result", "analysis_status", "analysis_error", "update_datetime"])
    except Exception as e:
        logger.exception("SOP analysis failed. sop_id=%s", sop_id)
        sop.analysis_status = "failed"
        sop.analysis_error = str(e)
        sop.save(update_fields=["analysis_status", "analysis_error", "update_datetime"])
        raise


# 兼容旧函数名（避免历史引用失效）
sop_analysis_task = sop_analyze_task
