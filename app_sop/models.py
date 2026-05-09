from django.db import models
from utils.models import BaseModel, table_prefix
# Create your models here.
class Sop(BaseModel):
    ANALYSIS_STATUS_CHOICES = (
        ("pending", "待分析"),
        ("running", "分析中"),
        ("success", "成功"),
        ("failed", "失败"),
    )
    title = models.CharField(max_length=255, verbose_name="SOP标题", help_text="SOP标题")
    content_html = models.TextField(verbose_name="SOP内容", help_text="SOP内容",null=True,blank=True,)
    video_url = models.CharField(max_length=512, verbose_name="视频URL", help_text="视频URL",null=True,blank=True,)
    # 分析结果存数据库 JSON 字段
    analysis_result = models.JSONField(verbose_name="分析结果", help_text="分析结果", null=True, blank=True)
    analysis_status = models.CharField(max_length=16, choices=ANALYSIS_STATUS_CHOICES, default="pending", verbose_name="分析状态")
    analysis_error = models.TextField(verbose_name="错误信息", help_text="错误信息",null=True,blank=True,)
    class Meta:
        db_table = "app_sop"
        verbose_name = "SOP管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.title
